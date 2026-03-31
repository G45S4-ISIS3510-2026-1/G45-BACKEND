from datetime import datetime, timedelta, timezone

dayNumber = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

def getColombiaTimezone():
    return timezone(timedelta(hours=-5))

def getStartWeekColombia():
    # Configurar el huso horario para Colombia (UTC-5)
    colombia_tz = getColombiaTimezone()
    # Obtener la fecha actual en el huso horario de Colombia
    today = datetime.now(colombia_tz).date()
    start_of_week = today - timedelta(days=today.weekday())      # Domingo
    return start_of_week

def getColombiaWeekDate(week_day: str):
    start_of_week = getStartWeekColombia()
    return start_of_week + timedelta(days=dayNumber.get(week_day, 0))

def refactorTimezone(date: datetime):
    colombia_tz = getColombiaTimezone()
    return date.astimezone(colombia_tz)