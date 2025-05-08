from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional
from datetime import datetime

class Participant(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the participant")
    email: str = Field(..., description="Email address of the participant")
    nic: Optional[str] = Field(None, description="National Identity Card number of the participant")
    firstName: str = Field(..., description="First name of the participant")
    lastName: Optional[str] = Field(None, description="Last name of the participant")
    phone: str = Field(..., description="Phone number of the participant")
    studentId: Optional[str] = Field(None, description="Student ID of the participant")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL of the participant")
    attended: bool = Field(default=False, description="Attendance status of the participant")
    ticketId: UUID4 = Field(..., description="Unique ticket ID for the participant")
    eventId: int = Field(..., description="ID of the event the participant is attending")
    ticket_link: Optional[str] = Field(None, description="Link to the participant's ticket")
