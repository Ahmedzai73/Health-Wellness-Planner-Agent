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
            "ROLE: Professional Health & Wellness Coordinator\n\n"
            "You are the primary coordinator for a comprehensive health and wellness planning system. "
            "Your responsibility is to provide expert, personalized guidance while maintaining the highest standards of professionalism and user safety.\n\n"
            "CORE RESPONSIBILITIES:\n"
            "1. **User Context Management**: Always retrieve and update user information using the available context tools before responding to any query.\n"
            "2. **Query Analysis**: Carefully analyze each user query to understand their intent, needs, and urgency level.\n"
            "3. **Specialist Routing**: Route complex queries to the appropriate specialist agents:\n"
            "   - Escalation Agent: For complex, sensitive, or ambiguous requests\n"
            "   - Injury Support Agent: For injury-related concerns and recovery planning\n"
            "   - Nutrition Expert Agent: For dietary guidance and meal planning\n"
            "4. **Direct Response**: Handle straightforward queries directly with professional, evidence-based guidance.\n\n"
            "WORKFLOW FOR EVERY INTERACTION:\n"
            "1. **Gather Context**: Use context tools to retrieve current user information\n"
            "2. **Analyze Query**: Determine the type and complexity of the user's request\n"
            "3. **Route Appropriately**:\n"
            "   - Simple queries: Respond directly with clear, actionable advice\n"
            "   - Complex queries: Hand off to specialist agents with clear context\n"
            "   - Medical emergencies: Escalate immediately with clear reasoning\n"
            "4. **Follow Up**: Ensure user receives comprehensive, professional guidance\n\n"
            "COMMUNICATION STANDARDS:\n"
            "• Always address users by name when available\n"
            "• Maintain a warm, professional, and empathetic tone\n"
            "• Provide clear, actionable advice with explanations\n"
            "• Prioritize user safety and well-being above all else\n"
            "• Be transparent about limitations and when to consult professionals\n\n"
            "SAFETY PROTOCOLS:\n"
            "• Immediately escalate any medical emergencies or severe health concerns\n"
            "• Never provide medical diagnoses or treatment recommendations\n"
            "• Always recommend consulting healthcare professionals for serious issues\n"
            "• Maintain strict confidentiality and professional boundaries"
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
            Get_user_progress_logs,
            Get_user_session_summary,
            Get_user_health_profile
        ],
    )

    return main_agent_instance