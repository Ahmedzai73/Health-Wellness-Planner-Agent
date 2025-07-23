from agents import Agent, AgentOutputSchema
from configuration_files.gemini_config import gemini_configuration
from context import UserSessionContext
from agents_as_tools import agents_as_tools
from sub_agents import sub_agents 


def main_agent():
    escalation_agent, injury_support_agent, nutrition_expert_agent = sub_agents()
    config = gemini_configuration()
    model = config.model

    goal_analyzer, meal_planner, task_scheduler, goal_tracker, workout_recommender = agents_as_tools()
    escalation_agent, injury_support_agent, nutrition_expert_agent = sub_agents()
    
    main_agent = Agent(
        name="main_agent",
        instructions="This is the primary agent that coordinates between various sub-agents and tools. It handles user requests, delegates tasks to specialized agents, and ensures that the user's goals are met efficiently. If a request is complex or requires human intervention, it escalates appropriately.",
        model=model,
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        handoffs=[escalation_agent, injury_support_agent, nutrition_expert_agent],
        tools=[
            goal_analyzer.as_tool(
                tool_name="goal_analyzer",
                tool_description="Analyzes user goals and structures them into key components for clarity and implementation.",
            ),
            meal_planner.as_tool(
                tool_name="meal_planner",
                tool_description="Generates personalized meal plans based on user preferences and nutritional needs.",
            ),
            task_scheduler.as_tool(
                tool_name="task_scheduler",
                tool_description="Schedules and manages user tasks related to health and wellness.",
            ),
            goal_tracker.as_tool(
                tool_name="goal_tracker",
                tool_description="Tracks user progress towards health and fitness goals.",
            ),
            workout_recommender.as_tool(
                tool_name="workout_recommender",
                tool_description="Recommends personalized workouts based on user profile and goals.",
            ),
        ],
    )
    
    
    
    return main_agent, config