# Import required modules
import os
from dotenv import load_dotenv
from agents.run import RunConfig
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

# Load environment variables from .env file
load_dotenv()

# Get Gemini configuration from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")
gemini_base_url = os.getenv("GEMINI_BASE_URL")


# gemini_api_key = GEMINI_API_KEY="AIzaSyDEplkMs2UsCOgDslqKBTClrq6AFfNCGPE"
# gemini_model_name = GEMINI_MODEL_NAME="gemini 2.0-flash"
# gemini_base_url = GEMINI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai"


# Validate that all required environment variables are set
if not gemini_api_key or not gemini_model_name or not gemini_base_url:
    raise ValueError(
        "Please check the Gemini config file - environment variables not loading properly"
    )


def gemini_configuration():
    """
    Configure and return the Gemini client and model settings.
    
    Returns:
        RunConfig: Configuration object for running Gemini model
    """
    # Initialize the AsyncOpenAI client with Gemini credentials
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url=gemini_base_url
    )

    # Set up the chat completions model with the specified Gemini model
    model = OpenAIChatCompletionsModel(
        model=gemini_model_name,
        openai_client=external_client
    )

    # Create the run configuration with model and client settings
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )

    return config