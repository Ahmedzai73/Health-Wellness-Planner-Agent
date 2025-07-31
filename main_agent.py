from agents import Agent, AgentOutputSchema, AgentOutputSchemaBase
from openai_config import OPENAI_MODEL
from agents_as_tools import agents_as_tools
from sub_agents import sub_agents
from context import UserSessionContext

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

    main_agent_instance = Agent(
        name="main_agent",
        instructions=(
            "Your role is 'Main Agent', the primary interface responsible for expertly and empathetically routing user requests to the appropriate specialist agent. Your communication must be consistently respectful, professional, and human-like.\n\n"
            "Your core mission is to analyze the user's initial query and handoff the conversation to the most suitable specialist. Always address the user by their name (if provided) and demonstrate courteous professionalism.\n\n"
        ),
        model=model,
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        handoffs=[escalation_agent, injury_support_agent, nutrition_expert_agent],
        tools=[],
    )

    return main_agent_instance