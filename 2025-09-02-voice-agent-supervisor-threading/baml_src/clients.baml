client<llm> SmallModel {
  provider "openai-generic"
  options {
    base_url "https://api.cerebras.ai/v1"
    api_key env.CEREBRAS_API_KEY
    model "gpt-oss-120b"
  }
}

client<llm> SupervisorModel {
  provider openai
  options {
    model "gpt-5"
  }
}