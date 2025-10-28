from flask import Blueprint, jsonify, request
from extensions import db
from sqlalchemy import select, text, update, and_, or_
from helpers import convert_days_week_in_dates, order_alphabetically
from models import User, Classes, ClassSchedule, UserSchedule, ClassOccurrence
from models.class_schedules import ClassesStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import UnprocessableEntity, NotFound, Conflict, BadRequest
from sqlalchemy.exc import IntegrityError
from datetime import date

# Creates a blueprint that can be imported
classes_bp = Blueprint("classes_bp", __name__)


# Custom exception
class ClassScheduleSpotsFull(Exception):
    pass


# access classes only with a valid jwt
@classes_bp.route("/classes", methods=["GET"])
@jwt_required()
def classes():
    # create list to store class objects
    class_schedules = []

    # get classes names
    classes_names = db.session.scalars(
        select(Classes.slug).order_by(Classes.name.asc())
    ).all()

    # create one object by class
    for class_name in classes_names:

        class_ = (
            db.session.execute(
                select(
                    Classes.id, Classes.slug, Classes.name, Classes.description
                ).where(Classes.slug == class_name)
            )
            .mappings()
            .one()
        )

        # convert row into dict for JSON to read/serialize
        class_dict = dict(class_)

        schedules = (
            db.session.execute(
                select(
                    ClassSchedule.id,
                    ClassSchedule.day_of_week,
                    ClassSchedule.start_time,
                    ClassSchedule.end_time,
                    ClassSchedule.spots,
                    ClassSchedule.status,
                    User.name.label("teacher_name"),
                )
                .join(Classes, Classes.id == ClassSchedule.class_id)
                .join(User, User.id == ClassSchedule.teacher_id)
                .order_by(
                    ClassSchedule.day_of_week, ClassSchedule.start_time
                )  # first sorts by day of week and then in each day it sorts by start_time
                .where(Classes.slug == class_name)
            )
            .mappings()
            .all()
        )

        # convert each row into dict for JSON to read/serialize
        schedules_dict = [dict(row) for row in schedules]

        # convert time objects created in Python in strings
        for schedule in schedules_dict:
            schedule["start_time"] = schedule["start_time"].strftime("%H:%M")
            schedule["end_time"] = schedule["end_time"].strftime("%H:%M")

        # append class and schedules as a object in a list
        class_schedules.append(
            {
                "class_": class_dict,
                "schedules": schedules_dict,
            }
        )
    # return the list with all classes and their schedules
    return jsonify({"classes": class_schedules}), 200


@classes_bp.route("/classes", methods=["POST"])
@jwt_required()
def book_class():
    # TODO:
    data = request.get_json()
    schedule_id = data.get("scheduleId")
    date_str = data.get("date")
    current_user = get_jwt_identity()

    # Convert into a time object (python)
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    # Extract only the date
    date_obj = dt.date()

    try:
        # Put SQL statements inside a transaction to deal with multiple bookings simultaneously
        # Start a transaction and grab only one write lock (so no other writer can write)
        db.session.execute(text("BEGIN IMMEDIATE"))

        schedule = db.session.scalar(
            select(ClassSchedule).where(ClassSchedule.id == schedule_id)
        )

        # Check if schedule still exists
        if not schedule:
            raise NotFound("schedule not found")

        # Check if date matches with schedule's weekday
        if schedule.day_of_week != date_obj.weekday():
            raise UnprocessableEntity("date does not match the schedule's weekday")

        # Check if a class occurrence exists for that date and class schedule
        class_occurrence = db.session.scalar(
            select(ClassOccurrence).where(
                ClassOccurrence.class_schedule_id == schedule_id,
                ClassOccurrence.date == date_obj,
            )
        )

        # If it does decrement the spots value and creates a user schedule
        if class_occurrence is not None:

            # check if the class occurrence is already FULLYBOOKED
            if class_occurrence.status == ClassesStatus.FULLYBOOKED:
                raise ClassScheduleSpotsFull("this schedule has full spots!")

            update_spots = db.session.execute(
                update(ClassOccurrence)
                .where(
                    ClassOccurrence.id == class_occurrence.id,
                    ClassOccurrence.spots > 0,
                )
                .values(spots=ClassOccurrence.spots - 1)
            )

            # When the spots capability reaches 0 or its the last seat
            if update_spots.rowcount == 0 or class_occurrence.spots == 0:
                # Update the status to FULLYBOOKED
                update_status = db.session.execute(
                    update(ClassOccurrence)
                    .where(
                        ClassOccurrence.id == class_occurrence.id,
                        ClassOccurrence.status != ClassesStatus.FULLYBOOKED,
                    )
                    .values(status=ClassesStatus.FULLYBOOKED)
                )

                # If it updates commit the changes and don't rollback
                if update_status.rowcount > 0:
                    db.session.commit()
                    return jsonify({"error": "this schedule has full spots!"}), 409

                raise ClassScheduleSpotsFull("this schedule has full spots!")

            # Book class
            booking = UserSchedule(
                user_id=current_user,
                class_occurrence_id=class_occurrence.id,
            )
        # If not create the class occurrence, decrement spots and creates a user schedule
        else:
            new_class_occurrence = ClassOccurrence(
                class_schedule_id=schedule_id,
                date=date_obj,
                spots=schedule.spots,  # Select class schedule default capacity
            )

            db.session.add(new_class_occurrence)

            # to access the new occurrence object
            db.session.flush()

            # decrement spots
            update_spots = db.session.execute(
                update(ClassOccurrence)
                .where(
                    ClassOccurrence.id == new_class_occurrence.id,
                    ClassOccurrence.spots > 0,
                )
                .values(spots=ClassOccurrence.spots - 1)
            )

            # Book class
            booking = UserSchedule(
                user_id=current_user,
                class_occurrence_id=new_class_occurrence.id,
            )

        db.session.add(booking)

        db.session.commit()  # atomic commit the update and new booking changes are committed together

        return jsonify({"message": "Class schedule successfully booked!"}), 201
    # Exception to catch db constraint violations
    except IntegrityError as e:
        db.session.rollback()
        msg = str(e.orig)  # DB constraint messages

        if "unique_user_booking" in msg:
            raise Conflict("You are already booked for this class")
        raise Conflict("constraint violation")
    except NotFound as e:
        db.session.rollback()
        raise e
    except UnprocessableEntity as e:
        db.session.rollback()
        raise e
    except ClassScheduleSpotsFull as e:
        db.session.rollback()
        return jsonify({"error": [str(e)]}), 409


@classes_bp.route("/classes/<slug>", methods=["GET"])
@jwt_required()
def class_detail(slug):
    # TODO: review the type of select maybe here makes sense to use scalars
    # get class info and schedules specific from slug
    new_schedules = []
    current_user = get_jwt_identity()

    class_ = (
        db.session.execute(
            select(Classes.id, Classes.slug, Classes.name, Classes.description).where(
                Classes.slug == slug
            )
        )
        .mappings()
        .one()
    )

    # print(class_)

    # convert row into dict for JSON to read/serialize
    class_dict = dict(class_)

    # TODO: show user schedule status for each schedule and set to NOT_BOOKED if not exists
    schedules = (
        db.session.execute(
            select(
                ClassSchedule.id,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time,
                ClassSchedule.end_time,
                ClassSchedule.spots,
                User.name.label("teacher_name"),  # access teacher's name
                ClassOccurrence.id.label("occ_id"),
                ClassOccurrence.date,
                ClassOccurrence.spots.label("occ_spots"),
                ClassOccurrence.status.label("occ_status"),
                UserSchedule.class_occurrence_id.label("booking_id"),
                UserSchedule.status.label("booking_status"),
            )
            .join(Classes, Classes.id == ClassSchedule.class_id)
            .join(User, User.id == ClassSchedule.teacher_id)
            .outerjoin(
                ClassOccurrence,
                and_(
                    ClassOccurrence.class_schedule_id == ClassSchedule.id,
                    or_(ClassOccurrence.date == None, ClassOccurrence.date >= date.today()),
                ),  # outer join class occurrences to not hide the class schedules with no occurrences and show the booked schedules
            )
            .outerjoin(
                UserSchedule,  # outer join user schedules to know which schedules are booked or not by the current user
                and_(
                    UserSchedule.class_occurrence_id == ClassOccurrence.id,
                    UserSchedule.user_id == current_user,
                ),
            )
            .order_by(
                ClassSchedule.day_of_week,
                ClassSchedule.start_time,
                # ClassOccurrence.date,
            )  # first sorts by day of week and then in each day it sorts by start_time
            .where(Classes.slug == slug)
        )
        .mappings()
        .all()
    )

    # convert each row into dict to manipulate the values
    schedules_dict = [dict(row) for row in schedules]

    # avoid a list of repeated schedules - group the occurrences by schedule  
    for schedule in schedules_dict:

        # convert python time and date objects into string format
        schedule["start_time"] = schedule["start_time"].strftime("%H:%M")
        schedule["end_time"] = schedule["end_time"].strftime("%H:%M")
        if schedule["date"] is not None:
            schedule["date"] = schedule["date"].strftime("%Y-%m-%d")

        # check if a schedule with the same id doesn't already exist in the list
        # to ensure each schedule is added only once
        if not any(schedule["id"] == s["id"] for s in new_schedules):
            new_schedules.append({
                "id": schedule["id"],
                "day_of_week": schedule["day_of_week"],
                "start_time": schedule["start_time"],
                "end_time": schedule["end_time"],
                "teacher_name": schedule["teacher_name"],
                "occurrences": [],
            })

        # inside each schedule add the corresponded occurrences 
        for s in new_schedules:
            if s["id"] == schedule["id"]:
                s["occurrences"].append(
                    {
                        "occ_id": schedule["occ_id"],
                        "date": schedule["date"],
                        "occ_spots": schedule["occ_spots"],
                        "occ_status": schedule["occ_status"],
                        "booking": { # for each occ add the user booking information
                            "booking_id": schedule["booking_id"],
                            "booking_status": schedule["booking_status"],
                        },
                    }
                )

    # convert each row into dict for JSON to read/serialize
    new_schedules_dict = [dict(row) for row in new_schedules]

    print(new_schedules_dict)

    return (
        jsonify(
            {
                "class_details": {
                    "class_": class_dict,
                    "schedules": new_schedules_dict,
                    "dates": convert_days_week_in_dates(slug),
                }
            }
        ),
        200,
    )
