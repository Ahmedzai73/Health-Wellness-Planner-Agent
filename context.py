from typing import Optional, List
from pydantic import BaseModel


class UserSessionContext(BaseModel):
    name: str
    uid: int = 0
    goal: Optional[str] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[str] = None
    meal_plan: Optional[str] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[str] = []
    
