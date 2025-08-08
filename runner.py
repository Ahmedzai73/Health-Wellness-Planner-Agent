from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from main_agent import main_agent
import asyncio
from context import UserSessionContext

print(
    """
----------------------------------------------------------------------------------
Welcome to the Health & Wellness Assistant.
To get started, may I kindly request you to provide your details?
Your information will help me serve you better and support your wellness journey.
----------------------------------------------------------------------------------

"""
)


async def main():
    while True:
        input_name = input(
            "🧑 Hi there! What name would you like me to call you by?\n📝 Your answer: "
        ).strip()
        if input_name.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_goal = input(
            "🎯 What's your main health or fitness goal? (e.g., lose weight, build muscle, improve stamina, etc.)\n📝 Your answer: "
        ).strip()
        if input_goal.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_diet_preferences = input(
            "🥗 Do you have any dietary preferences or restrictions? (e.g., vegetarian, vegan, keto, halal, allergies, etc.)\n📝 Your answer (or press Enter to skip): "
        ).strip()
        if input_diet_preferences.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_workout_plan = input(
            "🏋️ What kind of workouts or physical activities do you enjoy or prefer? (e.g., running, yoga, gym, home workouts)\n📝 Your answer (or press Enter to skip): "
        ).strip()
        if input_workout_plan.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_meal_plan = input(
            "🍽️ Can you describe your usual meal routine, or do you have any specific meal planning needs?\n📝 Your answer (or press Enter to skip): "
        ).strip()
        if input_meal_plan.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_injury_notes = input(
            "🩹 Do you have any injuries, physical limitations, or health concerns you'd like me to know about?\n📝 Your answer (or press Enter to skip): "
        ).strip()
        if input_injury_notes.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_handoff_logs = input(
            "🤝 Have you worked with any trainers or coaches before? If yes, please share any notes or feedback you'd like me to consider.\n📝 Your answer (or press Enter to skip): "
        ).strip()
        if input_handoff_logs.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            return
        print(" ")

        input_progress_logs = input(
            "📈 Would you like to share any progress updates or notes about your journey so far?\n📝 Your answer (or press Enter to skip): "
        ).strip()
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
            progress_logs=[input_progress_logs] if input_progress_logs else [],
        )
        break

    agent = main_agent()

    print(
        "\nThank you for sharing your details! \nYou can now chat with your Health & Wellness Assistant. If you ever want to exit, just type 'exit'.\n"
    )
    
    while True:
        user_input_for_agent = input("\n💬 You: ").strip()
        if user_input_for_agent.lower() == "exit":
            print("Exiting the assistant. Goodbye!")
            break
        result = Runner.run_streamed(
            agent,
            user_input_for_agent,
            context=user_record,
        )
        print("🧑 ", end="", flush=True)
        async for event in result.stream_events():
            if (
                event.type == "raw_response_event"
                and isinstance(event.data, ResponseTextDeltaEvent)
            ):
                print(event.data.delta, end="", flush=True)
        print("")

if __name__ == "__main__":
    asyncio.run(main())
