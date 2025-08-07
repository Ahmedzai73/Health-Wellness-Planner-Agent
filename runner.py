from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from main_agent import main_agent
import asyncio
from context import UserSessionContext




async def main():
    
    print("""
    ------------------------------------------------------------------
    Welcome to the Health & Wellness Assistant.
    To get started, may I kindly request you to provide your details?
    Your information will help me serve you better and support your wellness journey.
    ------------------------------------------------------------------
    """)
    
    while True:
        input_name = input("Please enter your name: ").strip()
        if input_name.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_goal = input("Please enter your main health or fitness goal: ").strip()
        if input_goal.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_diet_preferences = input("Please enter your diet preferences (e.g., vegetarian, vegan, keto, etc.): ").strip()
        if input_diet_preferences.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_workout_plan = input("Please describe your preferred workout plan or activities: ").strip()
        if input_workout_plan.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_meal_plan = input("Please describe your typical meal plan or any meal planning needs: ").strip()
        if input_meal_plan.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_injury_notes = input("Please mention any injuries or physical limitations: ").strip()
        if input_injury_notes.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_handoff_logs = input("Please provide any handoff notes or relevant logs from previous trainers/coaches (if any): ").strip()
        if input_handoff_logs.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return

        input_progress_logs = input("Please share any progress logs or notes you'd like to include: ").strip()
        if input_progress_logs.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        
        user_record = UserSessionContext(

            name=input_name,
            goal=input_goal,
            diet_preferences=input_diet_preferences,
            workout_plan=input_workout_plan,
            meal_plan=input_meal_plan,
            injury_notes=input_injury_notes,
            handoff_logs=[input_handoff_logs] if input_handoff_logs else [],
            progress_logs=[input_progress_logs] if input_progress_logs else []

        )
        break

    agent = main_agent()
    
    print("\nAssistant is ready. You can now ask to see your details.")
    # Step 5: User interaction loop
    while True:
        user_input_for_agent = input("\nTalk with Assistant: ").strip()
        if user_input_for_agent.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            break
        
        result = Runner.run_streamed(
                agent,
                user_input_for_agent,
                context=user_record
            )
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                event.data.delta
                print(event.data.delta, end="", flush=True)

        


if __name__ == "__main__":
    asyncio.run(main())