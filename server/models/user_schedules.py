from extensions import db, ScheduleStatus
from datetime import datetime

class UserSchedule(db.Model):
    __tablename__ = "user_schedules"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), nullable=False)
    class_schedule_id = db.Column(db.Integer, db.ForeignKey("class_schedules.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.Integer, nullable=False, default=ScheduleStatus.BOOKED, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canceled_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship("User", back_populates="user_schedules")
    schedule = db.relationship("ClassSchedule", back_populates="user_schedules")

    # unique rule ensures the user cannot book the same class twice at the same day
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "class_schedule_id", "date", 
            name="unique_user_booking"
        ),
    )