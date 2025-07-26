from agents import Agent
from gemini_config import gemini_configuration
from context import UserSessionContext

def sub_agents(goal_analyzer, meal_planner, task_scheduler, goal_tracker, workout_recommender):
    config = gemini_configuration()
    model = config.model

    escalation_agent = Agent(
        name="escalation_agent",
        instructions=(
            "Analyze the user's request and determine if it needs to be escalated to a human. "
            "If the request is complex, sensitive, or the AI is unsure how to handle it, engage the handoff tool to transfer "
            "the conversation to a human agent. Provide the human agent with the full context of the user's session, including "
            "their goals, preferences, and interaction history. If the request does not require escalation, break it down into "
            "subtasks and delegate to the appropriate specialized agents or tools."
        ),
        model=model,
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

    injury_support_agent = Agent(
        name="injury_support_agent",
        instructions=(
            "Provide guidance and support for users dealing with injuries. "
            "Analyze the user's injury details, recovery status, and fitness goals. "
            "Offer personalized advice on safe exercises, stretches, and recovery timelines. "
            "Adjust their workout and meal plans as needed to facilitate healing. "
            "Escalate to a medical professional if the injury is severe or worsening. "
            "You have access to two tools that have been handed off to you: "
            "workout_recommender_tool and goal_tracker_tool. Use them as needed to assist in providing support to the user."
        ),
        model=model,
        tools=[
            workout_recommender.as_tool(
                tool_name="workout_recommender",
                tool_description="Recommends safe and personalized workouts for users with injuries.",
            ),
            goal_tracker.as_tool(
                tool_name="goal_tracker",
                tool_description="Tracks user progress and recovery towards health and fitness goals.",
            ),
        ],
    )

    nutrition_expert_agent = Agent(
        name="nutrition_expert_agent",
        instructions=(
            "Analyze the user's nutritional needs and provide tailored dietary recommendations. "
            "Consider factors like age, weight, activity level, and health goals. Suggest meal plans and nutritional strategies "
            "to optimize health and well-being. Utilize the goal_analyzer_tool to break down the user's health goals, the "
            "meal_planner_tool to generate personalized meal plans, and the goal_tracker_tool to monitor progress. Escalate to "
            "a medical professional if needed for complex cases or medical conditions."
        ),
        model=model,
        tools=[
            goal_analyzer.as_tool(
                tool_name="goal_analyzer",
                tool_description="Analyzes user goals and structures them into key components for clarity and implementation.",
            ),
            meal_planner.as_tool(
                tool_name="meal_planner",
                tool_description="Generates personalized meal plans based on user preferences and nutritional needs.",
            ),
            goal_tracker.as_tool(
                tool_name="goal_tracker",
                tool_description="Tracks user progress towards health and fitness goals.",
            ),
        ],
    )

    return escalation_agent, injury_support_agent, nutrition_expert_agent