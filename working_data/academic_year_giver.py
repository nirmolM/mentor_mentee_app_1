from datetime import datetime


def give_academic_year():
    current_month = datetime.now().month
    return (str(datetime.now().year) + '-' + str((datetime.now().year - 2000 + 1))) if current_month \
        in [7, 8, 9, 10, 11, 12] else (str(datetime.now().year - 1) + '-' + str((datetime.now().year - 2000)))
