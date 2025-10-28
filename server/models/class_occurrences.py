from extensions import db, ClassesStatus

class ClassOccurrence(db.Model):
    __tablename__ = "class_occurrences"
    id = db.Column(db.Integer, primary_key=True)
    class_schedule_id = db.Column(db.Integer, db.ForeignKey("class_schedules.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    spots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=ClassesStatus.AVAILABLE, index=True)
    
    schedule = db.relationship("ClassSchedule", back_populates="class_occurrences")
    user_schedules = db.relationship("UserSchedule", back_populates="class_occurrence")

    # avoids bookings for the same date and same class schedule
    __table_args__ = (
        db.UniqueConstraint(
            "class_schedule_id", "date", 
            name="unique_class_occurrence"
        ),
    )