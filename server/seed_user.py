
from app import app
# from extensions import db, 
# from models.users import User
from datetime import datetime, time
from extensions import db, bcrypt, Roles, ClassesStatus
from models import User, Student, Teacher, Classes, ClassSchedule
# from models.class_schedules import ClassesStatus  # if you're using Enum for schedule status

with app.app_context():
    """Populate initial users, students, teachers, classes and class schedules."""

    t1 = bcrypt.generate_password_hash("hash1").decode("utf-8")
    t2 = bcrypt.generate_password_hash("hash2").decode("utf-8")
    t3 = bcrypt.generate_password_hash("hash3").decode("utf-8")
    u1 = bcrypt.generate_password_hash("hash4").decode("utf-8")
    u2 = bcrypt.generate_password_hash("hash5").decode("utf-8")
    a1 = bcrypt.generate_password_hash("hash6").decode("utf-8")

    # ---- Users ----
    # Use your real password hasher in your app; these are just placeholders
    users = [
        User(name="Alice Ramos",  email="alice@studio.com",  password_hash=t1, phone="111111111"),
        User(name="Bruno Costa",  email="bruno@studio.com",  password_hash=t2, phone="222222222"),
        User(name="Carla Silva",  email="carla@studio.com", password_hash=t3, phone="933111111"),
        User(name="Diogo Matos",  email="diogo@example.com", password_hash=u1, phone="933222222"),
        User(name="Eva Sousa",    email="eva@example.com",   password_hash=u2, phone="933333333"),
        User(name="Studio Admin", email="admin@studio.com",  password_hash=a1, phone="933444444", role=Roles.ADMIN),
    ]

    # ---- Students ----
    students = [
        Student(user_id="j5HAlHyiKmyx4_RzfDQys"),
        Student(user_id="1cC9IfSChCYEodOE1E_Gz"),
    ]

    # ---- 3 Teachers ----
    teachers = [
        Teacher(user_id="xiys6ps8RxhBPC9lCyJIR", description="Certified Pilates Mat & Reformer."),
        Teacher(user_id="Zo3xbUmUGIKsGswtQY-YE", description="Prenatal & Mobility specialist."),
        Teacher(user_id="_3lcfs2OH56J0EzrO0zEi", description="Certified Pilates Mat & Mobility specialist."),
    ]

    # ---- Classes (Pilates) ----
    pilates_classes = [
        Classes(id=1, slug="pilates-mat",        name="Pilates Mat",        description="Fundamentals on the mat, core & posture."),
        Classes(id=2, slug="pilates-reformer",   name="Pilates Reformer",   description="Reformer work for strength & control."),
        Classes(id=3, slug="prenatal-pilates",   name="Prenatal Pilates",   description="Gentle pilates adapted for pregnancy."),
        Classes(id=4, slug="stretch-mobility",   name="Stretch & Mobility", description="Flexibility, mobility, and recovery."),
    ]

    # Helper to avoid violating (day_of_week, start_time) unique constraint
    def t(hhmm: str) -> time:
        return time.fromisoformat(hhmm)  # "HH:MM"

    # ---- Class Schedules ----
    # NOTE: Your schema enforces UNIQUE(day_of_week, start_time) *globally* across all classes,
    # so on a given day use distinct start times across all schedules below.
    schedules = [
        # Pilates Mat (teacher: Alice, Bruno)
        # ClassSchedule(id=101, class_id=1, teacher_id="xiys6ps8RxhBPC9lCyJIR",
        #               day_of_week=1, start_time=t("09:00"), end_time=t("09:55"),
        #               spots=6, status=ClassesStatus.AVAILABLE),
        # ClassSchedule(id=102, class_id=1, teacher_id="xiys6ps8RxhBPC9lCyJIR",
        #               day_of_week=3, start_time=t("08:00"), end_time=t("08:55"),
        #               spots=6, status=ClassesStatus.AVAILABLE),
        # ClassSchedule(id=103, class_id=1, teacher_id="_3lcfs2OH56J0EzrO0zEi",
        #               day_of_week=1, start_time=t("10:30"), end_time=t("11:20"),
        #               spots=6, status=ClassesStatus.AVAILABLE),
        # ClassSchedule(id=104, class_id=1, teacher_id="_3lcfs2OH56J0EzrO0zEi",
        #               day_of_week=3, start_time=t("17:30"), end_time=t("18:20"),
        #               spots=6, status=ClassesStatus.AVAILABLE),

        # Pilates Reformer (teacher: Alice) – different start times on those days
        ClassSchedule(id=201, class_id=2, teacher_id="xiys6ps8RxhBPC9lCyJIR",
                      day_of_week=1, start_time=t("18:00"), end_time=t("18:55"),
                      spots=6, status=ClassesStatus.AVAILABLE),
        ClassSchedule(id=202, class_id=2, teacher_id="xiys6ps8RxhBPC9lCyJIR",
                      day_of_week=4, start_time=t("19:00"), end_time=t("19:55"),
                      spots=6, status=ClassesStatus.AVAILABLE),

        # Prenatal Pilates (teacher: Bruno)
        ClassSchedule(id=301, class_id=3, teacher_id="Zo3xbUmUGIKsGswtQY-YE",
                      day_of_week=2, start_time=t("10:00"), end_time=t("10:50"),
                      spots=6, status=ClassesStatus.AVAILABLE),
        ClassSchedule(id=302, class_id=3, teacher_id="Zo3xbUmUGIKsGswtQY-YE",
                      day_of_week=5, start_time=t("10:00"), end_time=t("10:50"),
                      spots=6, status=ClassesStatus.AVAILABLE),  # Saturday 10:00 OK (unique with Tue 10:00)

        # Stretch & Mobility (teacher: Bruno)
        ClassSchedule(id=401, class_id=4, teacher_id="Zo3xbUmUGIKsGswtQY-YE",
                      day_of_week=0, start_time=t("07:30"), end_time=t("08:20"),
                      spots=6, status=ClassesStatus.AVAILABLE),
        ClassSchedule(id=402, class_id=4, teacher_id="Zo3xbUmUGIKsGswtQY-YE",
                      day_of_week=4, start_time=t("07:00"), end_time=t("07:50"),
                      spots=6, status=ClassesStatus.AVAILABLE),
        ClassSchedule(id=403, class_id=4, teacher_id="_3lcfs2OH56J0EzrO0zEi",
                      day_of_week=0, start_time=t("12:30"), end_time=t("13:20"),
                      spots=6, status=ClassesStatus.AVAILABLE),
        ClassSchedule(id=404, class_id=4, teacher_id="_3lcfs2OH56J0EzrO0zEi",
                      day_of_week=4, start_time=t("17:30"), end_time=t("18:20"),
                      spots=6, status=ClassesStatus.AVAILABLE),
    ]

    # ---- Save all ----
    # Do it in one transaction
    # db.session.add_all(users)
    db.session.add_all(students)
    # db.session.add_all(teachers)
    # db.session.add_all(pilates_classes)
    # db.session.add_all(schedules)
    db.session.commit()

