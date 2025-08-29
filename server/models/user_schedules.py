from extensions import db, ScheduleStatus

# use composite primary key to ensure the user cannot book the same class occurrence twice 
class UserSchedule(db.Model):
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), primary_key=True)
    class_occurrence_id = db.Column(db.Integer, db.ForeignKey("class_occurrences.id"), primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=ScheduleStatus.SCHEDULE.value)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canceled_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship("User", back_populates="user_schedules")
    class_occurrence = db.relationship("ClassOccurrence", back_populates="user_schedules")