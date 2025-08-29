from extensions import db, TeacherStatus
from config import DevConfig

class Teacher(db.Model):
    __tablename__ = "teachers"
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), primary_key=True)
    description = db.Column(db.String(200), nullable=True)
    number_of_classes_allowed = db.Column(
        db.Integer, 
        default=lambda: DevConfig.TOTAL_CLASSES // DevConfig.TOTAL_TEACHERS, 
        nullable=False)
    status = db.Column(db.Integer, nullable=False, default=TeacherStatus.AVAILABLE.value)

    user = db.relationship("User", back_populates="teacher")
    schedules = db.relationship("ClassSchedule", back_populates="teacher", cascade="all, delete-orphan")