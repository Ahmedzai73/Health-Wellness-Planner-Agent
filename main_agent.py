from agents import Agent
from openai_config import OPENAI_MODEL
from agents_as_tools import agents_as_tools
from sub_agents import sub_agents
from context import UserSessionContext
from context_tools import(
            Get_username,
            Get_user_goal,
            Get_user_diet_preferences,
            Get_user_workout_plan,
            Get_user_meal_plan,
            Get_user_injury_notes,
            Get_user_handoff_logs,
            Get_user_progress_logs
       )

def main_agent():   
    """
    Initializes and configures the entire agent architecture.
    The output of this agent will be in a structured format (JSON-like).
    """
    model = OPENAI_MODEL
    

    # Get tool agents
    goal_analyzer, meal_planner, task_scheduler, goal_tracker, workout_recommender = agents_as_tools()
    # Get sub agents
    escalation_agent, injury_support_agent, nutrition_expert_agent = sub_agents(
        goal_analyzer,
        meal_planner,
        task_scheduler,
        goal_tracker,
        workout_recommender,
    )

    main_agent_instance = Agent[UserSessionContext](
        name="main_agent",
        instructions=(
            "You are the 'Main Agent'. Whenever you receive new information or updates from the user, you must update the context accordingly. Always update the context. Your job is to analyze the user's initial query and route the conversation to the most suitable specialist agent. Address the user by their name if available, and always communicate in a respectful, professional, and human-like manner."
        ),
        model=model,
        handoffs=[escalation_agent, injury_support_agent, nutrition_expert_agent],
        tools=[
            Get_username,
            Get_user_goal,
            Get_user_diet_preferences,
            Get_user_workout_plan,
            Get_user_meal_plan,
            Get_user_injury_notes,
            Get_user_handoff_logs,
            Get_user_progress_logs
        ],
    )

    return main_agent_instance