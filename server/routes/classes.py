from flask import Blueprint, jsonify
from extensions import db
from sqlalchemy import select
from helpers import convert_days_week_in_dates, order_alphabetically
from models import User, Classes, ClassSchedule
from flask_jwt_extended import jwt_required

# Creates a blueprint that can be imported
classes_bp = Blueprint("classes_bp", __name__)


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
        sorted_names = order_alphabetically(schedules_dict)

        # append objects
        class_schedules.append(
            {
                "class_": class_dict,
                "schedules_info": {
                    "schedules": schedules_dict,
                    "sorted_names": sorted_names,
                },
            }
        )

    # print(f"class_schedules: ${class_schedules}")

    return jsonify({"classes": class_schedules}), 200


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
