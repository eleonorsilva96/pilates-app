from extensions import db

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    schedules = db.relationship("ClassSchedule", back_populates="class_", cascade="all, delete-orphan")