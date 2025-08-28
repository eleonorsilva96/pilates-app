from extensions import db, ClassesStatus

# ClassSchedule constraint ensures each occurrence has a unique start time
class ClassOccurrence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_schedule_id = db.Column(db.Integer, db.ForeignKey("class_schedules.id"), nullable=False)
    date = db.Column(db.Date, nullable=False) 
    spots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    schedules = db.relationship("ClassSchedule", back_populates="class_occurrences")
    user_schedules = db.relationship("UserSchedule", back_populates="class_occurrences")