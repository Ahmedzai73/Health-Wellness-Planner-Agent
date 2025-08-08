from agents import RunContextWrapper, function_tool
from context import UserSessionContext


@function_tool
async def Get_username(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's name from the session context."""
    try:
        user_name = wrapper.context.name
        return f"User Name: {user_name}" if user_name else "User Name: Not provided"
    except Exception as e:
        return f"Error retrieving username: {str(e)}"

@function_tool
async def Get_user_goal(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's health and wellness goal from the session context."""
    try:
        user_goal = wrapper.context.goal
        return f"User Goal: {user_goal}" if user_goal else "User Goal: Not specified"
    except Exception as e:
        return f"Error retrieving user goal: {str(e)}"

@function_tool
async def Get_user_diet_preferences(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's dietary preferences and restrictions from the session context."""
    try:
        user_diet_preferences = wrapper.context.diet_preferences
        return f"Diet Preferences: {user_diet_preferences}" if user_diet_preferences else "Diet Preferences: Not specified"
    except Exception as e:
        return f"Error retrieving diet preferences: {str(e)}"

@function_tool
async def Get_user_workout_plan(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's current workout plan from the session context."""
    try:
        user_workout_plan = wrapper.context.workout_plan
        return f"Current Workout Plan: {user_workout_plan}" if user_workout_plan else "Workout Plan: Not available"
    except Exception as e:
        return f"Error retrieving workout plan: {str(e)}"

@function_tool
async def Get_user_meal_plan(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's current meal plan from the session context."""
    try:
        user_meal_plan = wrapper.context.meal_plan
        return f"Current Meal Plan: {user_meal_plan}" if user_meal_plan else "Meal Plan: Not available"
    except Exception as e:
        return f"Error retrieving meal plan: {str(e)}"

@function_tool
async def Get_user_injury_notes(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's injury notes and health concerns from the session context."""
    try:
        user_injury_notes = wrapper.context.injury_notes
        return f"Injury Notes: {user_injury_notes}" if user_injury_notes else "Injury Notes: None reported"
    except Exception as e:
        return f"Error retrieving injury notes: {str(e)}"

@function_tool
async def Get_user_handoff_logs(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the history of agent handoffs and interactions from the session context."""
    try:
        user_handoff_logs = wrapper.context.handoff_logs
        if user_handoff_logs:
            return f"Handoff History: {' | '.join(user_handoff_logs)}"
        else:
            return "Handoff History: No previous handoffs recorded"
    except Exception as e:
        return f"Error retrieving handoff logs: {str(e)}"

@function_tool
async def Get_user_progress_logs(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves the user's progress tracking logs from the session context."""
    try:
        user_progress_logs = wrapper.context.progress_logs
        if user_progress_logs:
            return f"Progress Logs: {' | '.join(user_progress_logs)}"
        else:
            return "Progress Logs: No progress data available"
    except Exception as e:
        return f"Error retrieving progress logs: {str(e)}"

@function_tool
async def Get_user_session_summary(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves a comprehensive summary of the user's current session data."""
    try:
        context = wrapper.context
        summary_parts = []
        
        if context.name:
            summary_parts.append(f"Name: {context.name}")
        if context.goal:
            summary_parts.append(f"Goal: {context.goal}")
        if context.diet_preferences:
            summary_parts.append(f"Diet Preferences: {context.diet_preferences}")
        if context.workout_plan:
            summary_parts.append(f"Workout Plan: Available")
        if context.meal_plan:
            summary_parts.append(f"Meal Plan: Available")
        if context.injury_notes:
            summary_parts.append(f"Injury Notes: {context.injury_notes}")
        
        summary_parts.append(f"Handoff Logs: {len(context.handoff_logs)} entries")
        summary_parts.append(f"Progress Logs: {len(context.progress_logs)} entries")
        
        return "Session Summary: " + " | ".join(summary_parts) if summary_parts else "Session Summary: No data available"
    except Exception as e:
        return f"Error retrieving session summary: {str(e)}"

@function_tool
async def Get_user_health_profile(wrapper: RunContextWrapper[UserSessionContext]) -> str:
    """Retrieves a comprehensive health profile summary for the user."""
    try:
        context = wrapper.context
        profile_parts = []
        
        if context.name:
            profile_parts.append(f"User: {context.name}")
        if context.goal:
            profile_parts.append(f"Primary Goal: {context.goal}")
        if context.diet_preferences:
            profile_parts.append(f"Dietary Profile: {context.diet_preferences}")
        if context.injury_notes:
            profile_parts.append(f"Health Considerations: {context.injury_notes}")
        
        # Add status indicators
        workout_status = "Active" if context.workout_plan else "Not Set"
        meal_status = "Active" if context.meal_plan else "Not Set"
        
        profile_parts.append(f"Workout Status: {workout_status}")
        profile_parts.append(f"Meal Plan Status: {meal_status}")
        profile_parts.append(f"Progress Tracking: {len(context.progress_logs)} entries")
        
        return "Health Profile: " + " | ".join(profile_parts) if profile_parts else "Health Profile: Incomplete"
    except Exception as e:
        return f"Error retrieving health profile: {str(e)}"