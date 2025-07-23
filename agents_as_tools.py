from agents import Agent, AgentOutputSchema
from configuration_files.gemini_config import gemini_configuration
from context import UserSessionContext


def agents_as_tools():
    """
    This function returns a list of agents that can be used as tools.
    """
    config = gemini_configuration()
    model = config.model

    goal_analyzer = Agent(
        name="goal_analyzer",
        instructions=(
            "Convert the user's goal into a structured format. Break down the goal into key components: "
            "objective, success criteria, required resources, timeline, and potential risks. Organize the "
            "information in a clear, standardized template for easy understanding and implementation."
        ),
        handoff_description=(
            "Analyzes user goals and structures them into key components for clarity and implementation."
        ),
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        model=model,
    )

    meal_planner = Agent(
        name="meal_planner",
        instructions=(
            "Generate a comprehensive 7-day meal plan that strictly adheres to the user's dietary preferences "
            "and restrictions. For each day, provide breakfast, lunch, dinner, and snack options. Include detailed "
            "recipes, ingredient lists, nutritional information, and preparation instructions. Ensure the plan is "
            "balanced, healthy, and meets the user's specific nutritional requirements."
        ),
        handoff_description=(
            "Creates a detailed 7-day meal plan with recipes, nutritional info, and preparation steps based on user preferences and restrictions."
        ),
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        model=model,
    )

    task_scheduler = Agent(
        name="task_scheduler",
        instructions=(
            "Analyze the tasks and create an optimized schedule. Break down tasks into manageable steps, assign priorities, "
            "and allocate time slots. Consider dependencies between tasks, resource availability, and deadlines. Create a "
            "timeline that maximizes productivity while maintaining flexibility. Additionally, schedule recurring weekly "
            "progress checks to review task completion, assess progress against goals, and make necessary adjustments to the schedule."
        ),
        handoff_description=(
            "Schedules tasks, assigns priorities, allocates time, and sets up recurring progress checks for optimal productivity."
        ),
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        model=model,
    )

    goal_tracker = Agent(
        name="goal_tracker",
        instructions=(
            "Track the progress of user's goals and tasks. Monitor completion status, identify delays or bottlenecks, and provide "
            "regular updates. Suggest adjustments to timelines or resources as needed to keep goals on track."
        ),
        handoff_description=(
            "Monitors goal and task progress, identifies issues, and suggests adjustments to maintain momentum."
        ),
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        model=model,
    )

    workout_recommender = Agent(
        name="workout_recommender",
        instructions=(
            "Analyze the user's fitness goals, current fitness level, and preferences to recommend personalized workout plans. "
            "Consider factors like available equipment, time constraints, and any physical limitations. Provide clear, structured "
            "workout routines with proper exercise descriptions, sets, reps, and rest periods."
        ),
        handoff_description=(
            "Recommends personalized workout plans based on user goals, fitness level, and preferences."
        ),
        output_type=AgentOutputSchema(UserSessionContext, strict_json_schema=False),
        model=model,
    )

    return (
        goal_analyzer,
        meal_planner,
        task_scheduler,
        goal_tracker,
        workout_recommender,
    )