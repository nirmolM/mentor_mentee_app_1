from datetime import datetime


def give_academic_year():
    current_month = datetime.now().month
    return (str(datetime.now().year) + '-' + str((datetime.now().year - 2000 + 1))) if current_month \
        in [7, 8, 9, 10, 11, 12] else (str(datetime.now().year - 1) + '-' + str((datetime.now().year - 2000)))


def give_year_and_semester(admitted_ay: str):  # todo -> $BUG$ -> This will not account for dropped students
    year_no = int(give_academic_year()[0:4]) - int(admitted_ay[0:4])
    current_month = datetime.now().month
    year_local = ["FE", "SE", "TE", "BE"][year_no]
    if current_month > 6:
        semester_local = ["I", "III", "V", "VII"][year_no]
    else:
        semester_local = ["II", "IV", "VI", "VIII"][year_no]
    return [year_local, semester_local]
