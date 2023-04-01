import pandas as pd
import random
from datetime import date, timedelta, time, datetime
from workalendar.europe import Germany


def generate_dates(username, month, year, count):
    cal = Germany()
    days_in_month = pd.to_datetime(f"{year}-{month}", format="%Y-%m").days_in_month
    chosen_dates = set()

    while len(chosen_dates) < count:
        day = random.randint(1, days_in_month)
        date_obj = date(year, month, day)

        if not (cal.is_holiday(date_obj) or date_obj.weekday() == 6) and date_obj not in chosen_dates:
            chosen_dates.add(date_obj)

    return sorted(list(chosen_dates))


def generate_times(dates):
    times = []

    for date_obj in dates:
        if date_obj.weekday() < 5:
            hour = random.randint(18, 20)
        else:
            hour = random.randint(15, 17)

        times.append(time(hour, 0))

    return times


def generate_end_times(times):
    end_times = []

    for start_time in times:
        end_hour = (start_time.hour + 3) % 24
        end_times.append(time(end_hour, 0))

    return end_times


def calculate_working_hours(start_times, end_times):
    working_hours = []

    for start_time, end_time in zip(start_times, end_times):
        start_dt = datetime.combine(date.min, start_time)
        end_dt = datetime.combine(date.min, end_time)
        duration = (end_dt - start_dt).seconds // 3600
        working_hours.append(duration)

    return working_hours


def create_csv(username, month, year, count):
    dates = generate_dates(username, month, year, count)
    start_times = generate_times(dates)
    end_times = generate_end_times(start_times)
    working_hours = calculate_working_hours(start_times, end_times)
    weekdays = [d.strftime("%A") for d in dates]

    data = {
        "Nutzername": [username] * count,
        "Tag": weekdays,
        "Datum": [d.strftime("%Y-%m-%d") for d in dates],
        "Uhrzeit": [t.strftime("%H:%M") for t in start_times],
        "Uhrzeit Ende": [t.strftime("%H:%M") for t in end_times],
        "Arbeitszeit": working_hours
    }

    df = pd.DataFrame(data)
    df.to_csv(f"{username}_{year}_{month}.csv", index=False)
    print(df)



# Beispiel: Erstellen Sie eine CSV-Datei mit dem Nutzernamen 'Nutzer1', dem Monat 1, dem Jahr 2020 und der Anzahl 15
create_csv("Nutzer1", 1, 2020, 15)