from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)
    user_type = Column(String, default="dentist")  # "admin" or "dentist"
    openai_api_key = Column(String, nullable=True)
    analyses = relationship("Analysis", back_populates="user")

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_name = Column(String)
    patient_age = Column(Integer)
    patient_gender = Column(String)
    patient_complaint = Column(String)
    patient_medical_history = Column(String)
    uploaded_filename = Column(String)
    analysis_result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="analyses")