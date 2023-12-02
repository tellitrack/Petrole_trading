from datetime import datetime


def to_date(from_date, app_source):
    """
    Convertit une chaîne de date en un objet datetime. Date selon la source de l'application.

    :param from_date: La chaîne de date à convertir.
    :param app_source: La source de l'application (par exemple, 'WealthSimple').
    :return: Un objet datetime.date.
    """
    try:
        if app_source == 'WealthSimple':
            return datetime.strptime(from_date, '%Y-%m-%d').date()
    except ValueError as e:
        print(f"Erreur lors de la conversion de la date : {e}")
        return None
