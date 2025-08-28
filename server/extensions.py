from flask_sqlalchemy import SQLAlchemy
from nanoid import generate as nanoid_generate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from enum import Enum

# define user roles
class Roles:
    USER = "user"
    ADMIN = "admin"

# define the set of subscription plans
class SubscriptionPlan(Enum):
    TWO_CLASSES = 2
    THREE_CLASSES = 3
    UNLIMITED = 0

# define the set of student payment statuses
class PaymentStatus(Enum):
    NOT_PAYED = 0
    PAYED = 1
    DELAYED = 2

# define the set of teacher statuses
class TeacherStatus(Enum):
    AVAILABLE = 0
    FULLYBOOKED = 1
    HOLIDAYS = 2
    DEACTIVATED = 3

# define the set of class statuses
class ClassesStatus(Enum):
    AVAILABLE = 0
    FULLYBOOKED = 1
    CANCELED = 2

# define the set of schedule statuses
class ScheduleStatus(Enum):
    SCHEDULE = 0
    COMPLETED = 1
    CANCELED = 2
    WAITING = 3


# generate unique opaque id for each new user created
def generate():
    return nanoid_generate()

# create custom exception - global error handler
class EmailAlreadyExistsError(Exception):
    pass

class AuthError(Exception):
    pass

bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()


