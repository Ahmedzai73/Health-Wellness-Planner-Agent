from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[Dict[str, Any]] = None  
    diet_preferences: Optional[str] = None
    workout_plan: Optional[Dict[str, Any]] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = [] 
