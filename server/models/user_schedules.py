from extensions import db, ScheduleStatus
from datetime import datetime

# use composite primary key to ensure the user cannot book the same class occurrence twice 
class UserSchedule(db.Model):
    __tablename__ = "user_schedules"
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), primary_key=True)
    class_occurrence_id = db.Column(db.Integer, db.ForeignKey("class_occurrences.id"), primary_key=True, index=True)
    status = db.Column(db.Integer, nullable=False, default=ScheduleStatus.BOOKED, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canceled_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship("User", back_populates="user_schedules")
    class_occurrence = db.relationship("ClassOccurrence", back_populates="user_schedules")

    # unique rule ensures the user cannot book the same class twice at the same day
    # __table_args__ = (
    #     db.UniqueConstraint(
    #         "user_id", "class_schedule_id", "date", 
    #         name="unique_user_booking"
    #     ),
    # )