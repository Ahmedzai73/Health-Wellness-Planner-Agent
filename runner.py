from agents import Runner, SQLiteSession
from openai.types.responses import ResponseTextDeltaEvent
from main_agent import main_agent
import asyncio
from context import UserSessionContext
import json

SHOW_HELP_MESSAGE = """
------------------------------------------------------------
            Welcome to Your AI Health Assistant
------------------------------------------------------------

Type your question or instruction below.

Available commands:
- "exit"               → Quit the assistant
- "delete all history" → Clear all saved conversation
- "Undo"               → Remove the last message
- "help"               → Show this help message again
------------------------------------------------------------
"""

async def main():
    agent = main_agent()
    session = SQLiteSession("User_001", "conversation_history.db")

    print(SHOW_HELP_MESSAGE)

    while True:
        userinput = input("You: ").strip()

        if userinput.lower() == "exit":
            print("Exiting the assistant. Stay healthy!")
            break

        elif userinput.lower() == "help":
            print(SHOW_HELP_MESSAGE)
            continue

        elif userinput.lower() == "delete all history":
            removed_history = await session.clear_session()
            print("All conversation history has been cleared.")
            continue

        elif userinput.lower() == "undo":
            undo = await session.pop_item()
            print("Last message removed from history.")
            continue

        result = Runner.run_streamed(
            agent,
            userinput,
            session=session,
            context=UserSessionContext
        )

        json_string = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta or ""
                print(delta, end="", flush=True)
                json_string += delta
                
        try:
            # Parse the JSON response from agent
            response = json.loads(json_string)
            print("\nBot:", response)
           
        except json.JSONDecodeError:
            print("\nBot: Sorry, I couldn't understand the response.")
            


if __name__ == "__main__":
    asyncio.run(main())
