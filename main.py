from agents import Runner, SQLiteSession
from main_agent import main_agent
import asyncio


session = SQLiteSession("conversation_123")
async def main():
    # Initialize the main agent and configuration
    agent, config = main_agent()

    while True:
        userinput = input("You: ")
        if userinput.strip().lower() == "exit":
            print("Exiting...")
            break

        result = await Runner.run(
            agent,
            userinput,
            run_config=config,
            session=session
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
