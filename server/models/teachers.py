from extensions import db, TeacherStatus
from config import DevConfig

class Teacher(db.Model):
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), primary_key=True)
    description = db.Column(db.String(200), nullable=True)
    number_of_classes_allowed = db.Column(
        db.Integer, 
        default=lambda: DevConfig.TOTAL_CLASSES // DevConfig.TOTAL_TEACHERS, 
        nullable=False)
    status = db.Column(db.Integer, nullable=False, default=TeacherStatus.AVAILABLE.value)

    users = db.relationship("Users", back_populates="teachers")
    schedules = db.relationship("ClassSchedule", back_populates="teachers", cascade="all, delete-orphan")