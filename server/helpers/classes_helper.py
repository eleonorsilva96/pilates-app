from extensions import db
from sqlalchemy import select
from models import User, Classes, ClassSchedule
from datetime import time, date

def convert_days_week_in_dates(slug):
    unique_schedule_days_week = []
    schedule_dates = []

    today_day = date.today().day
    today_month = date.today().month
    today_year = date.today().year
    week_day = date.today().weekday()
    
    # return the list of week days from the class
    schedule_days_week = db.session.scalars(
        select(ClassSchedule.day_of_week)
        .where(ClassSchedule.class_.has(Classes.slug == slug))
    ).all()

    # store only single week days
    for day in schedule_days_week:
        if day not in unique_schedule_days_week:
            unique_schedule_days_week.append(day) 

    # print(f"unique_schedule_days_week: ${unique_schedule_days_week}")

    def is_valid_date(year, month, day):
        try:
            date(year, month, day)
            return True
        except ValueError:
            return False

    # loop through the calendar by year
    for i, _ in enumerate(range(today_month, 13)):
        if i > 0:
            # reset day for each month
            today_day = 1
        for _ in range(today_day, 32):
            # get only valid dates
            if (is_valid_date(today_year, today_month, today_day)):
                # reset week day - if the limit of days of the week is exceeded
                if (week_day > 6):
                    week_day = 0

                # check if the current week day is the same as the schedule week day
                for day in unique_schedule_days_week:
                    if (week_day == day):
                            schedule_dates.append(date(today_year, today_month, today_day))

                week_day += 1

            # increment day
            today_day += 1

        today_month += 1

    # print(f"schedule_dates: ${schedule_dates}")

    # convert date objects created in Python in strings
    schedule_dates = [d.strftime("%Y-%m-%d") for d in schedule_dates]

    return schedule_dates

def order_alphabetically(schedules):
    teacher_names = []

    for schedule in schedules:
        teacher_names.append(schedule["name"])
    
    teacher_names.sort()
    
    print(teacher_names)

    return teacher_names
        
