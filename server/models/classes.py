from extensions import db

class Classes(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)    
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    schedules = db.relationship("ClassSchedule", back_populates="class_", cascade="all, delete-orphan")