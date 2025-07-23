from agents import Agent, Runner 
from main_agent import main_agent
from typing import cast
import chainlit as cl
from agents.run import RunConfig

@cl.on_chat_start
async def start():
    # Initialize main agent
    agent_instance, config = main_agent()
    
    # Store in session
    cl.user_session.set("main_agent", agent_instance)
    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])
    
    await cl.Message(content="Health Agent is ready! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    # Create a new message object for streaming
    msg = cl.Message(content="")
    await msg.send()

    agent_instance = cast(Agent, cl.user_session.get("main_agent"))
    config = cast(RunConfig, cl.user_session.get("config"))

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        # Run the agent with streaming enabled
        result = Runner.run_streamed(
            agent_instance, 
            history, 
            run_config=config,
        )

        # Stream the response token by token
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)

        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": msg.content})

        # Update the session with the new history.
        cl.user_session.set("chat_history", history)

    except Exception as e:
        error_content = f"Error: {str(e)}"
        await msg.stream_token(error_content)
        await msg.update()
        print(f"Error: {str(e)}")