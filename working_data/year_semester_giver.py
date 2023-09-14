from datetime import datetime


def give_academic_year():
    current_month = datetime.now().month
    return (str(datetime.now().year) + '-' + str((datetime.now().year - 2000 + 1))) if current_month \
        in [7, 8, 9, 10, 11, 12] else (str(datetime.now().year - 1) + '-' + str((datetime.now().year - 2000)))


def give_year_and_semester(admitted_ay: str):
    year_no = int(give_academic_year()[0:4]) - int(admitted_ay[0:4])
    current_month = datetime.now().month
    match year_no:
        case 0:
            year_local = "FE"
            if current_month in [7, 8, 9, 10, 11, 12]:
                semester_local = 'I'
            else:
                semester_local = 'II'
        case 1:
            year_local = "SE"
            if current_month in [7, 8, 9, 10, 11, 12]:
                semester_local = 'III'
            else:
                semester_local = 'IV'
        case 2:
            year_local = "TE"
            if current_month in [7, 8, 9, 10, 11, 12]:
                semester_local = 'V'
            else:
                semester_local = 'VI'
        case 3:
            year_local = "BE"
            if current_month in [7, 8, 9, 10, 11, 12]:
                semester_local = 'VII'
            else:
                semester_local = 'VIII'
        case _:
            year_local = "Error Case"
            semester_local = "Error Case"
    return [year_local, semester_local]
