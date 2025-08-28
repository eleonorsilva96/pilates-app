from extensions import db, SubscriptionPlan, PaymentStatus

class Students(db.Model):
    user_id = db.Column(db.String(21), db.ForeignKey("users.id"), primary_key=True)
    subscription_plan = db.Column(db.Integer, nullable=False, default=SubscriptionPlan.TWO_CLASSES.value)
    payment_status = db.Column(db.Integer, nullable=False, default=PaymentStatus.NOT_PAYED.value)
    users = db.relationship("Users", back_populates="students")