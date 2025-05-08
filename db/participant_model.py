from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True)
    nic = Column(String, nullable=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    studentId = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    attended = Column(Boolean, default=False)
    ticketId = Column(UUID(as_uuid=True), nullable=False, default=uuid4)
    eventId = Column(Integer, nullable=False)
    ticket_link = Column(String, nullable=True, default="")

