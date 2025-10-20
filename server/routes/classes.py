from flask import Blueprint, jsonify, request
from extensions import db
from sqlalchemy import select, text, update
from helpers import convert_days_week_in_dates, order_alphabetically
from models import User, Classes, ClassSchedule, UserSchedule
from models.class_schedules import ClassesStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import UnprocessableEntity, NotFound, Conflict, BadRequest
from sqlalchemy.exc import IntegrityError
from datetime import datetime

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
                    User.name,
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

        # sort alphabetically teacher names
        # sorted_names = order_alphabetically(schedules_dict)

        # append class and schedules in a object
        class_schedules.append(
            {
                "class_": class_dict,
                "schedules_info": {
                    "schedules": schedules_dict,
                    # "sorted_names": sorted_names,
                },
            }
        )

    # print(f"class_schedules: ${class_schedules}")

    return jsonify({"classes": class_schedules}), 200

@classes_bp.route("/classes", methods=["POST"])
@jwt_required()
def book_class():
    # TODO:  
    data = request.get_json()
    schedule_id = data.get('scheduleId')
    date_str = data.get('date')
    current_user = get_jwt_identity()

    # Convert into a time object (iso)
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    # Extract only the date
    date_obj = dt.date()

    try:
        # Put SQL statements inside a transaction to deal with multiple bookings simultaneously
        # Start a transaction and grab only one write lock (so no other writer can write)
        db.session.execute(text("BEGIN IMMEDIATE"))

        schedule = (db.session.scalar(select(ClassSchedule).where(ClassSchedule.id == schedule_id)))

        # Check if schedule still exists
        if not schedule:
            raise NotFound("schedule not found")
        
        # Check if date matches with schedule's weekday 
        if schedule.day_of_week != date_obj.weekday():
            raise UnprocessableEntity("date does not match the schedule's weekday")

        # Update class schedule spots
        update_schedule = db.session.execute(
            update(ClassSchedule)
            .where(ClassSchedule.id == schedule_id, ClassSchedule.spots > 0)
            .values(
                spots=ClassSchedule.spots - 1
            )
        )

        # When class schedule capability reaches to 0
        if update_schedule.rowcount == 0:
            update_status = db.session.execute(
                update(ClassSchedule)
                .where(ClassSchedule.id == schedule_id, ClassSchedule.status != ClassesStatus.FULLYBOOKED)
                .values(
                    status=ClassesStatus.FULLYBOOKED
                )
            )

            if update_status.rowcount > 0:
                # avoid rollback when committing changes
                db.session.commit()
                return jsonify({"error": "this schedule has full spots!"}), 409

            raise ClassScheduleSpotsFull("this schedule has full spots!")

        # Book class
        booking = UserSchedule(
            user_id=current_user,
            class_schedule_id=schedule_id,
            date=date_obj,
        )

        db.session.add(booking)

        db.session.commit() # atomic commit the update and new booking changes are committed together

        return jsonify({
            "message": "Class schedule successfully booked!"
        }), 201
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
    class_ = (
        db.session.execute(
            select(Classes.id, Classes.slug, Classes.name, Classes.description).where(
                Classes.slug == slug
            )
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
                User.name,
            )
            .join(Classes, Classes.id == ClassSchedule.class_id)
            .join(User, User.id == ClassSchedule.teacher_id)
            .order_by(
                ClassSchedule.day_of_week, ClassSchedule.start_time
            )  # first sorts by day of week and then in each day it sorts by start_time
            .where(Classes.slug == slug)
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

    # sort alphabetically teacher names
    sorted_names = order_alphabetically(schedules_dict)

    return (
        jsonify(
            {
                "class_details": {
                    "class_": class_dict,
                    "schedules_info": {
                        "schedules": schedules_dict,
                        "sorted_names": sorted_names,
                    },
                    "dates": convert_days_week_in_dates(slug),
                }
            }
        ),
        200,
    )
