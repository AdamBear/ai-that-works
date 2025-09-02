## Running the project

    uv run voice_agent.py

or for no voice

    DEMO_MODE=true uv run voice_agent.py

## Adding dependencies

    uv add DEPENDENCY_NAME

## BAML Commands

After chaning baml sources:

    uv run baml-cli generate


## BAML Tests

When iterating on the BAML prompts/models:

    uv run baml-cli test
