from extensions import db, generate, Roles

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(21), primary_key=True, default=generate)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    img_path = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), nullable=False, default=Roles.USER)

    student = db.relationship("Student", back_populates="user", uselist=False)
    teacher = db.relationship("Teacher", back_populates="user", uselist=False)
    user_schedules = db.relationship("UserSchedule", back_populates="user")
    schedule_events = db.relationship("ScheduleEvent", back_populates="user")