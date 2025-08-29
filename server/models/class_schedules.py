from extensions import db, ClassesStatus

class ClassSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    teacher_id = db.Column(db.String(21), db.ForeignKey("teachers.user_id"), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False) # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    spots = db.Column(db.Integer, default=6, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=ClassesStatus.AVAILABLE.value)
    
    class_ = db.relationship("Classes", back_populates="schedules")
    teacher = db.relationship("Teacher", back_populates="schedules")
    class_occurrences = db.relationship("ClassOccurrence", back_populates="schedule")

    # the teacher can only have one class type per day and ensure it is always enforced
    # classes (same or different) don't start at the same time on the same day
    __table_args__ = (
        db.UniqueConstraint(
            "teacher_id", "day_of_week", "class_id",
            name="one_teacher_day_class"
        ),
        db.UniqueConstraint(
            "day_of_week", "start_time",
            name="unique_start_time_per_day"
        ),
    )