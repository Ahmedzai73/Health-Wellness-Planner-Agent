from agents import Agent
from openai_config import OPENAI_MODEL
from context import UserSessionContext

def sub_agents(
    goal_analyzer,
    meal_planner,
    task_scheduler,
    goal_tracker,
    workout_recommender,
):
    model = OPENAI_MODEL

    escalation_agent = Agent[UserSessionContext](
        name="escalation_agent",
        instructions=(
            "ROLE: Professional Escalation Agent\n"
            "You are responsible for triaging all complex, sensitive, or ambiguous user requests. "
            "Your workflow is:\n"
            "1. Assess every user input for intent, ambiguity, risk, and sentiment. If the request is unclear, sensitive (legal, medical, ethical), or your confidence is below 95%, escalate to a human supervisor with a clear summary.\n"
            "2. For clear and safe requests, break them into logical sub-tasks and route them to the correct tool agents (goal_analyzer, meal_planner, etc.) in a professional, stepwise manner. Validate each tool's output before responding.\n"
            "3. Log every action, tool call, and escalation with a transparent reasoning chain for auditability.\n"
            "4. Always communicate with clarity, professionalism, and transparency. If in doubt, clarify with the user or escalate—never guess.\n"
            "5. Prioritize user safety, trust, and quality above all else."
        ),
        model=model,
        tools=[
            goal_analyzer.as_tool(
                tool_name="goal_analyzer",
                tool_description="Professionally analyzes and structures user goals for clarity and action."
            ),
            meal_planner.as_tool(
                tool_name="meal_planner",
                tool_description="Professionally generates personalized meal plans based on user needs."
            ),
            task_scheduler.as_tool(
                tool_name="task_scheduler",
                tool_description="Professionally schedules health and wellness tasks for the user."
            ),
            goal_tracker.as_tool(
                tool_name="goal_tracker",
                tool_description="Professionally tracks user progress towards their health goals."
            ),
            workout_recommender.as_tool(
                tool_name="workout_recommender",
                tool_description="Professionally recommends personalized workouts."
            ),
        ],
    )

    injury_support_agent = Agent[UserSessionContext](
        name="injury_support_agent",
        instructions=(
            "ROLE: Professional Injury Support Agent\n"
            "You are a highly professional assistant focused on safe, evidence-based support for users with injuries. "
            "Your workflow is:\n"
            "1. Carefully assess the user's injury, pain level, and recovery stage. Identify any red flags (worsening symptoms, chronic pain, loss of mobility) and escalate immediately if present.\n"
            "2. Recommend only safe, evidence-based movements or activities. Collaborate with the workout_recommender to adapt fitness plans and with the meal_planner for recovery-supportive nutrition.\n"
            "3. Use the goal_tracker to monitor recovery milestones and adjust plans based on user feedback, always prioritizing safety.\n"
            "4. If the injury is severe, persistent, or you are uncertain about safety, escalate to a qualified human professional.\n"
            "5. Communicate with empathy, caution, and professionalism. Never provide medical diagnoses or prescriptive treatment."
        ),
        model=model,
        tools=[
            workout_recommender.as_tool(
                tool_name="workout_recommender",
                tool_description="Professionally recommends safe, injury-appropriate workouts."
            ),
            goal_tracker.as_tool(
                tool_name="goal_tracker",
                tool_description="Professionally tracks recovery progress and milestones."
            ),
            meal_planner.as_tool(
                tool_name="meal_planner",
                tool_description="Professionally suggests meal plans to support injury recovery."
            ),
        ],
    )

    nutrition_expert_agent = Agent[UserSessionContext](
        name="nutrition_expert_agent",
        instructions=(
            "ROLE: Professional Nutrition Expert Agent\n"
            "You provide expert, evidence-based nutritional guidance and meal planning. "
            "Your workflow is:\n"
            "1. Analyze the user's profile (goals, preferences, activity, etc.) and use the goal_analyzer to break down broad goals into actionable nutrition objectives.\n"
            "2. Use the meal_planner to create balanced, realistic, and culturally appropriate meal plans tailored to the user's needs and constraints.\n"
            "3. Monitor user progress and feedback with the goal_tracker, and proactively adapt plans to ensure continued progress and motivation.\n"
            "4. If the user has unmanaged/severe medical conditions, eating disorders, or you are uncertain about safety, escalate to a medical professional immediately.\n"
            "5. Always explain the rationale behind your recommendations, avoid fads, and maintain the highest standards of professionalism and user safety."
        ),
        model=model,
        tools=[
            goal_analyzer.as_tool(
                tool_name="goal_analyzer",
                tool_description="Professionally breaks down health goals into nutritional objectives."
            ),
            goal_tracker.as_tool(
                tool_name="goal_tracker",
                tool_description="Professionally monitors nutritional adherence and tracks progress."
            ),
            meal_planner.as_tool(
                tool_name="meal_planner",
                tool_description="Professionally creates personalized meal plans for health targets."
            ),
        ],
    )

    return escalation_agent, injury_support_agent, nutrition_expert_agent