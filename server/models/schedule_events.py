from extensions import db
from datetime import datetime
from sqlalchemy import Enum as SAEnum
from enum import Enum

class EventType(str, Enum):
    CANCEL = "CANCEL"
    RESCHEDULE = "RESCHEDULE"

# ClassSchedule constraint ensures each event has a unique start time
class ScheduleEvent(db.Model):
    __tablename__ = "schedule_events"
    id = db.Column(db.Integer, primary_key=True)
    class_schedule_id = db.Column(db.Integer, db.ForeignKey("class_schedules.id"), nullable=False, index=True)
    updated_by_user_id = db.Column(db.String(21), db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    type = db.Column(SAEnum(EventType, name="schedule_event_type"), nullable=False) 
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reason = db.Column(db.Text, nullable=True)

    schedule = db.relationship("ClassSchedule", back_populates="schedule_events")
    user = db.relationship("User", back_populates="schedule_events")

    __table_args__ = (
        db.CheckConstraint(
            "(type = 'CANCEL' AND start_time is NULL AND end_time is NULL)"
            " OR "
            "(type = 'RESCHEDULE' AND start_time is NOT NULL AND end_time is NOT NULL AND start_time < end_time)",
            name="check_schedule_type"
        ),
    )