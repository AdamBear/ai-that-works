// class FinalizeAppointment {
//   intent "finalize_appointment"
//   start_date string
//   end_date string
//   human_name string
//   human_email string
//   human_phone string?

//   dog_size "small" | "large"
//   dog_name string
//   vaccines string[]
// }

// class MessageToUser {
//   intent "send_message_to_user"
//   message string
// }

function SmallTalk(conversation: string) -> string {
  client SmallModel
  prompt #"
    {{ _.role("system") }}
    You are a Tony, the friendly assistant at Happy Paws Dog Daycare. 
    
    You help customers with questions about dog boarding and daycare services.

    Be conversational and helpful. Keep responses brief and natural.

    {{ _.role("user") }}
    Continue this conversation naturally:
    {{ conversation }}
    
    Respond as the assistant with your next message only (do not include "Assistant:" prefix).
  "#
}

class CompliancePass {
  status "ON_TRACK"
}

class ComplianceFail {
  status "NEEDS_ADJUSTMENT"
  message string @description("Correction message starting with 'Oh wait, actually,' if adjustment needed")
}

type ComplianceReview = CompliancePass | ComplianceFail

function CheckCompliance(conversation: string) -> ComplianceReview {
  // client SmallModel
  client SupervisorModel
  prompt #"
    {{ _.role("system") }}
    You are an AI supervisor monitoring your employee Tony, 
    who picks up the phones at Happy Paws dog daycare.
    
     You must ensure Tony follows these rules strictly:
    
    RULES:
    1. Only discuss dogs (no other pets like cats, birds, snails, etc.)
    2. Always get the user's email address before confirming any booking
    3. If asked about required vaccines, answer must be exactly: "Rabies and Distemper"
    4. Do not provide medical or legal advice
    5. Stay focused on dog daycare/boarding services only
    6. Do not discuss pricing without first knowing the dates and dog size
    7. Always be professional and friendly
    8. If user mentions other animals, redirect to dogs immediately
    9. Collect dog's name before finalizing any booking
    10. Operating hours are 7 AM to 7 PM Monday-Saturday, closed Sundays
    
    Review the conversation below and check if the LAST assistant message violates any rule or goes off track.
    
    {{ _.role("user") }}

    <conversation>
    {{ conversation }}
    </conversation>
    
    <instructions>

    Analyze the last assistant response carefully.
    
    If the assistant's last message follows all rules: respond with status ON_TRACK
    
    If the assistant's last message violates any rule: respond with status NEEDS_ADJUSTMENT and provide a brief correction message (one sentence) that starts with "Oh wait, actually," to redirect the conversation properly.

    </instructions>
    
    {{ ctx.output_format }}
  "#
}

test CheckCompliance_CatViolation {
  functions [CheckCompliance]
  args {
    conversation #"
      User: Hi, I need to board my cat
      Assistant: Sure! I'd be happy to help you board your cat. What dates are you looking for?
    "#
  }
  @@assert({{ this.status == "NEEDS_ADJUSTMENT" }})
  @@assert({{ "actually" in this.message }})
}

test CheckCompliance_OnTrack {
  functions [CheckCompliance]
  args {
    conversation #"
      User: What are your hours?
      Assistant: We're open from 7 AM to 7 PM Monday through Saturday, and closed on Sundays.
    "#
  }
  @@assert({{ this.status == "ON_TRACK" }})
}

test CheckCompliance_MissingEmail {
  functions [CheckCompliance]
  args {
    conversation #"
      User: I need to board my dog Gordo from Jan 1-10
      Assistant: Perfect! I've got Gordo booked for January 1st through 10th. Your confirmation is all set!
    "#
  }
  @@assert({{ this.status == "NEEDS_ADJUSTMENT" }})
  @@assert({{ "email" in this.message }})
}

test CheckCompliance_WrongVaccines {
  functions [CheckCompliance]
  args {
    conversation #"
      User: What vaccines does my dog need?
      Assistant: Your dog needs to be up to date on Rabies, Distemper, and Bordetella vaccines.
    "#
  }
  @@assert({{ this.status == "NEEDS_ADJUSTMENT" }})
  @@assert({{ "Rabies and Distemper" in this.message }})
}

test CheckCompliance_MultiplePets {
  functions [CheckCompliance]
  args {
    conversation #"
      User: I have a dog named Gordo and a cat named Winky, can you board both?
      Assistant: We'd be happy to help with both Gordo and Winky! What dates are you looking for?
    "#
  }
  @@assert({{ this.status == "NEEDS_ADJUSTMENT" }})
  @@assert({{ "dogs" in this.message }})
}

test CheckCompliance_CigarettesSafety {
  functions [CheckCompliance]  
  args {
    conversation #"
      User: My dog loves to eat cigarettes
      Assistant: Thanks for letting me know! We'll make sure Gordo has plenty of his favorite treats during his stay.
    "#
  }
  @@assert({{ this.status == "NEEDS_ADJUSTMENT" }})
  @@assert({{ "safety" in this.message or "tobacco" in this.message }})
}
