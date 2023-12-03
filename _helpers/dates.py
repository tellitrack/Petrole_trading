import datetime as dt


def to_date(from_date, app_source):
    """
    Convertit une chaîne de date en un objet datetime. Date selon la source de l'application.

    :param from_date: La chaîne de date à convertir.
    :param app_source: La source de l'application (par exemple, 'WealthSimple').
    :return: Un objet datetime.date.
    """
    try:
        if app_source == 'WealthSimple':
            return dt.datetime.strptime(from_date, '%Y-%m-%d').date()
    except ValueError as e:
        print(f"Erreur lors de la conversion de la date : {e}")
        return None


def yesterday(today, dayoffs=None):
    """
    Calculate the previous date before 'today' that is not a day off.

    :param today: The reference date from which to calculate yesterday.
    :param dayoffs: A list of dates that are days off.
    :return: A date object representing the calculated 'yesterday'.
    """
    # Calculate the date for previous_day initially
    if dayoffs is None:
        dayoffs = []

    previous_day = today - dt.timedelta(days=1)

    # Adjust for weekends if needed by checking if yesterday is a Monday (weekday 0)
    # If so, subtract two more days to go back to Friday, assuming Saturday and Sunday are day offs.
    if previous_day.weekday() == 0:
        previous_day -= dt.timedelta(days=2)

    # If yesterday falls on a day off, keep going back a day until it's not a day off
    while previous_day in dayoffs or previous_day.weekday() >= 5:  # Assuming Saturday (5) and Sunday (6) are day offs
        previous_day -= dt.timedelta(days=1)

    return previous_day
