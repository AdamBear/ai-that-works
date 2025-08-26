---
summary: Two-phase daily review process - READ to gather context, then WRITE to update systems

last_updated: 2025-08-25
last_updated_by: dex
last_update: Added instruction to exclude spam/pitch emails from email review summary
sop__frequency: daily
---

# Daily Review SOP - Read/Write Split

## Purpose
Comprehensive daily review process split into two phases for better checkpointing and incremental progress.

**THE MAIN OUTPUT:**
1) A comprehensive daily review file in `company/dailies/YYYY-MM-DD-daily-review.md` with all gathered context
2) Updates to files in crm/ and gtd/ and other places based on the gathered context
3) A prioritized task list for the day

## Schedule
Daily - ideally first thing in the morning. Progress is incremental and resumable.

## Process Overview

This is a **TWO-PHASE PROCESS**:
1. **PHASE 1: READ** - Gather all relevant information and dump it into the daily review file
2. **PHASE 2: WRITE** - Process the gathered information and update all relevant systems

**IMPORTANT**: The daily review file is your checkpoint. You can pause after Phase 1 and return later to complete Phase 2. This makes the process incremental and resumable.



---

## PHASE 1: READ (Gather Context)

**Goal**: Collect all relevant information into `dailies/YYYY-MM-DD-daily-review.md`

All outputs from commands and user input should be saved to the daily review file as you go.

### Step 0: Initialize Daily Review File
- READ [daily-review-example.md](daily-review-example.md) to understand the expected format
- `touch company/dailies/YYYY-MM-DD-daily-review.md` with today's date
- Check for the most recent daily review in company/dailies/ and note the last review date
- Adjust time ranges for fetching data accordingly (e.g., if last review was 3 days ago, fetch 3 days of data)
- Add frontmatter with metadata about the review period

### Step 1: Brain Dump (REQUIRES USER INPUT)
- **STOP HERE - Ask user for their brain dump:**
  - Freeform reflection on how yesterday went
  - Anything on their mind
  - Overnight thoughts or insights
- **SAVE to daily review file under section "## Brain Dump"**


### Step 2: Review Yesterday's Work
#### 2a. Journal Review
- `head -n 200 journal.md` for recent changes and decisions
- **SAVE relevant entries to daily review file under "## Yesterday's Journal"**

### Step 5: Metrics Review
- run the metrics collection tool to get the latest metrics (tools/pull-metrics.ts)
- **SAVE metrics data to daily review file under "## Key Metrics"**
  - Focus on: Two-week goals progress and Waitlist growth only
  - Use the tools/loops/process-loops-csv.ts tool to process the latest waitlist data
  - Use the tools/loops/process-loops-csv.ts tool to process the latest waitlist data

### Step 6: SOP Review
- Use context from SOP frontmatter to determine if any SOPs need action today
- Examples: weekly update, monthly investor update, bi-weekly all hands prep
- **SAVE any SOPs needing action to daily review file under "## SOPs Due"**

### Phase 1 Complete
- **CHECKPOINT**: All context is now gathered in the daily review file
- write your first journal.md entry with what was done, - keep it to one bullet point summary about the file you wrote
- **STOP AND ASK THE USER** - here is the plan for the write phase - review and confirm - output a list of everything you plan to do in the write phase based on the data you collected


**IMPORTANT**: TO execute Phase 1 as quickly as possible, use parallel subagents to do the work. Ensure you prompt the subagents like so:

Don't use subagents for any task that relies solely on human input like the omnifocus inbox or the braindump.

```
You are tasked with executing a portion of the daily review SOP.

Begin by reading the SOP at company/sops/daily-review-rw.md, then your job is to execute the portion of the SOP that is assigned to you. 

Your section is: #### 2c. GTD Review
Your target file is: company/dailies/YYYY-MM-DD-daily-review.md

Ensure you ONLY perform your assigned task and nothing else. 

Other subagents are also executing portions of the SOP in parallel. If you get an error writing the daily review file, you should use `sleep 5` and then re-read the file, and try the Edit() again.

When you have finished editing the daily review file, respond with a short summary of what you did.
```


---

## PHASE 2: WRITE (Update Systems)

**Goal**: Process the gathered information from the daily review file and update all relevant systems

**Prerequisites**: Phase 1 must be complete with all data saved to the daily review file


### Step 1: Process GTD Updates
Based on the daily review file, update:
- company/gtd/next_actions.md with new actions identified
- company/gtd/today_plan.md with the day's priorities
- company/gtd/deferred.md with items to defer
- company/gtd/waiting.md with new waiting items
- company/gtd/finished_items.md with completed tasks

From here, as you go, you may check off items from today_plan.md as they are completed, and make other changes to GTD as well.

### Step 2: Update CRM
- Read company/crm/CLAUDE.md for CRM guidelines
- Based on the daily review file, update CRM with:
  - New accounts (use WebSearch and WebFetch to get full context)
  - Updated interactions and next steps for existing accounts
  - New contacts with full context
  - Events based on interactions noted during review

### Step 3: Create Linear Tickets
Based on the daily review file, create any needed Linear tickets for:
- Customer feedback items
- Bug reports
- Feature requests
- Technical debt identified

### Step 4: Send Follow-up Emails
Based on the daily review file, draft and send:
- use tools/gmail and company/communcations workflow (see sops/send-email.md)
- Thank you notes from yesterday's meetings
- Meeting confirmations for today
- Follow-up emails identified during review

### Step 5: Update Project Files
Based on the daily review file, update project files with:
- New next actions (especially for projects marked as needing them)
- Completed milestones
- Updated definitions of done

### Step 6: Update Metrics Files
- Update company/metrics/all.md with waitlist data from the daily review

### Step 7: Create Today's Plan
- Based on all gathered context, create a prioritized plan in company/gtd/today_plan.md
- Include both time-bound meetings and flexible tasks
- **Present the plan to the user for approval**

### Step 8: Team Communication
- Prepare a Slack message for #engineering with:
  - Yesterday's accomplishments (from daily review file)
  - Today's priorities (from today_plan.md)
  - Any blockers or important context

### Step 9: Update Journal
- Add an entry to company/journal.md documenting:
  - Completion of daily review
  - Key decisions made
  - Major updates performed

### Step 10: Update Weekly Updates
- these weekly updates will be sent to the team and will be used to build the monthly investor update
- check if there's a header for the UPCOMING Friday in company/weekly-updates.md, if not create a header for the upcoming friday with (DRAFT) in the title
- Add any high level updates to company/weekly-updates.md, including customer highlights, big product features, etc.


## Benefits of the Two-Phase Approach

1. **Incremental Progress**: Can complete Phase 1 and take a break before Phase 2
2. **Checkpointing**: Daily review file serves as a checkpoint for all gathered context
3. **Clear Separation**: READ operations don't modify systems, WRITE operations don't gather new data
4. **Flexibility**: Can delegate Phase 2 to another agent or person if needed
5. **Resumability**: If interrupted, can easily resume from the daily review file

## Notes
- 2025-08-15 - Initial creation with read/write split for better checkpointing (dex)
- The daily review file is the source of truth for Phase 2
- Phase 1 can be done quickly in the morning, Phase 2 when you have more time
- This approach reduces cognitive load by separating information gathering from decision making
