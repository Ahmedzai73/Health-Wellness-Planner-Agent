from agents import RunContextWrapper, function_tool
from context import UserSessionContext


@function_tool
async def Get_username(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_name = wrapper.context
    return f"Name: {user_name.name}"

@function_tool
async def Get_user_goal(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_goal = wrapper.context
    return f"Goal: {user_goal.goal}"

@function_tool
async def Get_user_diet_preferences(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_diet_preferences = wrapper.context
    return f"Diet preferences: {user_diet_preferences.diet_preferences}"

@function_tool
async def Get_user_workout_plan(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_workout_plan = wrapper.context
    return f"Workout Plan: {user_workout_plan.workout_plan}"

@function_tool
async def Get_user_meal_plan(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_meal_plan = wrapper.context
    return f"Meal Plan: {user_meal_plan.meal_plan}"

@function_tool
async def Get_user_injury_notes(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_injury_notes = wrapper.context
    return f"Injury Notes: {user_injury_notes.injury_notes}"

@function_tool
async def Get_user_handoff_logs(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_handoff_logs = wrapper.context
    return f"Handoff Logs: {user_handoff_logs.handoff_logs}"

@function_tool
async def Get_user_progress_logs(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    user_progress_logs = wrapper.context
    return f"Progress Logs: {user_progress_logs.progress_logs}"