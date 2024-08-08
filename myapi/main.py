from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    caller_name = Column(String)
    caller_email = Column(String)
    subject = Column(String)
    description = Column(Text)
    status = Column(String)
    priority = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/incidents")
def read_incidents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    incidents = db.query(Incident).offset(skip).limit(limit).all()
    return incidents

@app.get("/incidents/{incident_id}")
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@app.post("/incidents")
def create_incident(incident: dict, db: Session = Depends(get_db)):
    db_incident = Incident(**incident)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.put("/incidents/{incident_id}")
def update_incident(incident_id: int, incident: dict, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    for key, value in incident.items():
        setattr(db_incident, key, value)
    db.commit()
    db.refresh(db_incident)
    return db_incident