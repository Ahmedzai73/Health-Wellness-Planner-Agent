from agents import Agent, InputGuardrail, OutputGuardrail, ModelSettings
from openai_config import OPENAI_MODEL
from agents_as_tools import agents_as_tools
from sub_agents import sub_agents
from context import UserSessionContext
from guardrails import Health_and_Wellness_input_relevance_guardrail, Health_and_Wellness_output_relevance_guardrail
from context_tools import(
            Get_username,
            Get_user_goal,
            Get_user_diet_preferences,
            Get_user_workout_plan,
            Get_user_meal_plan,
            Get_user_injury_notes,
            Get_user_handoff_logs,
            Get_user_progress_logs,
            Get_user_session_summary,
            Get_user_health_profile
    )

def main_agent():   
    """
    Initializes and configures the entire agent architecture.
    The output of this agent will be in a structured format (JSON-like).
    """
    model = OPENAI_MODEL
    
    goal_analyzer, meal_planner, task_scheduler, goal_tracker, workout_recommender = agents_as_tools()

    escalation_agent, injury_support_agent, nutrition_expert_agent = sub_agents(
        goal_analyzer,
        meal_planner,
        task_scheduler,
        goal_tracker,
        workout_recommender,
    )

    main_agent_instance = Agent[UserSessionContext](
        name="Main Agent",
        instructions=(
            "ROLE: Health & Wellness Query Router\n\n"
            "You are an automated query routing system for health and wellness. "
            "Your sole function is to analyze incoming queries and route them to the appropriate specialist agent without direct user interaction.\n\n"
            "ROUTING RULES:\n"
            "1. Complex, sensitive, or ambiguous queries → Escalation Agent\n"
            "2. Injury, pain, or recovery queries → Injury Support Agent\n"
            "3. Diet, nutrition, or meal planning queries → Nutrition Expert Agent\n"
            "4. All other queries → Handle directly\n\n"
            "PROCESS:\n"
            "1. Analyze query content and context\n"
            "2. Route to appropriate agent based on rules\n"
            "3. Include relevant context with routed queries\n"
            "4. No direct communication with users\n\n"
            "SAFETY:\n"
            "• Route medical emergencies to Escalation Agent immediately\n"
            "• Never provide medical advice or diagnoses\n"
            "• Maintain strict confidentiality"
        ),
        model=model,
        handoffs=[escalation_agent, injury_support_agent, nutrition_expert_agent],
        input_guardrails=[InputGuardrail(guardrail_function=Health_and_Wellness_input_relevance_guardrail)],
        output_guardrails=[OutputGuardrail(guardrail_function=Health_and_Wellness_output_relevance_guardrail)],
        tools=[
            Get_user_session_summary,
            Get_user_health_profile
        ],
        model_settings=ModelSettings(
            temperature=0.1,
            )
    )

    return main_agent_instance