from extensions import db, SubscriptionPlan, PaymentStatus

class Student(db.Model):
    __tablename__ = "students"
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), primary_key=True)
    subscription_plan = db.Column(db.Integer, nullable=False, default=SubscriptionPlan.TWO_CLASSES)
    payment_status = db.Column(db.Integer, nullable=False, default=PaymentStatus.NOT_PAYED)
    
    user = db.relationship("User", back_populates="student")