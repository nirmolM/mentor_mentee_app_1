import mysql.connector
from working_data import password_giver as pg

"""
Possible Errors:
1. localhost login error 10061, MEANS SERVICE not running
-> To remove error, go to start, search for services, search for MySQL and then enable it, or run it
"""


# todo -> Make common function to get reg_id

def make_connection():
    """This will make a connection for a selected database
    This is used to Make, Show and Remove tables in a given database"""
    connection = mysql.connector.connect(user='root', password=pg.give_password(), host='localhost', buffered=True)
    return connection


def create_table(database_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")  # Will select Database that is passed as argument in the function
    create_main_table_command = 'CREATE TABLE mentee_details (reg_id char(5) PRIMARY KEY, ' \
                                'Smart_card_no varchar(20), Name varchar(150), Admitted_year varchar(10), ' \
                                'sakec_email varchar(100), microsoft_email varchar(100), mobile varchar(15),' \
                                'current_division varchar(4), current_roll_no varchar(15),' \
                                'date_of_birth varchar(11), place_of_birth varchar(11), ' \
                                'Residential_Address varchar(255), Correspondent_Address varchar(255), ' \
                                'Blood_group varchar(4),' \
                                'Mother_name varchar(20), mother_mobile varchar(15), ' \
                                'Father_name varchar(20), father_mobile varchar(15), ' \
                                'Guardian_name varchar(20), guardian_mobile varchar(15), ' \
                                '10th_percent varchar(5), 10th_institute varchar(50), 10th_board varchar(10), ' \
                                '12th_percent varchar(5), 12th_institute varchar(50), 12th_board varchar(10), ' \
                                'CET_marks varchar(3), JEE_marks varchar(3), Diploma_percent varchar(4), ' \
                                'sem1ptr varchar(4), sem2ptr varchar(4), sem3ptr varchar(4), sem4ptr varchar(4),' \
                                'sem5ptr varchar(4), sem6ptr varchar(4), sem7ptr varchar(4), sem8ptr varchar(4),' \
                                'courses_done varchar(20), Internship_status varchar(20), ' \
                                'publication_details varchar(20), copyright_details varchar(20), ' \
                                'products_developed varchar(20), professional_bodies varchar(20), ' \
                                'project_competitions varchar(20), ' \
                                'Placement_status varchar(20), higher_studies_status varchar(20), ' \
                                'entrepreneurship_status varchar(20))'
    cursor_local.execute(create_main_table_command)
    create_name_index_command = 'CREATE INDEX idx_mentee_details_name ON mentee_details(Name)'
    cursor_local.execute(create_name_index_command)
    create_leave_table_command = 'CREATE TABLE leaves(leave_id SERIAL PRIMARY KEY, ' \
                                 'reg_id char(5), ' \
                                 'leave_date_start DATE, leave_date_end DATE, leave_duration INT, ' \
                                 'reason VARCHAR(255), description varchar(255), document_given BOOLEAN, ' \
                                 'FOREIGN KEY (reg_id) REFERENCES mentee_details(reg_id))'
    cursor_local.execute(create_leave_table_command)
    create_academic_achievement_table_command = 'CREATE TABLE academic_achievements (aa_id SERIAL PRIMARY KEY, ' \
                                                'reg_id char(5), achievement_type varchar(20), ' \
                                                'achievement_rank varchar(15), ' \
                                                'subject varchar(50), semester varchar(15), year varchar(25), ' \
                                                'academic_year varchar(20), ' \
                                                'FOREIGN KEY (reg_id) REFERENCES mentee_details(reg_id))'
    cursor_local.execute(create_academic_achievement_table_command)
    create_lor_loa_record_table_command = 'CREATE TABLE lor_loa (letter_id SERIAL PRIMARY KEY, reg_id char(5), ' \
                                          'letter_type varchar(25), issuing_faculty_name varchar(35), ' \
                                          'reason varchar(35), FOREIGN KEY (reg_id) REFERENCES mentee_details(reg_id))'
    cursor_local.execute(create_lor_loa_record_table_command)
    cursor_local.close()
    connection_local.close()


def show_tables(database_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    select_db_command = f"USE {database_name}"
    cursor_local.execute(select_db_command)
    show_tb_command = "SHOW TABLES"
    cursor_local.execute(show_tb_command)
    table_list = cursor_local.fetchall()
    table_names = [tables[0] for tables in table_list]
    cursor_local.close()
    connection_local.close()
    return table_names


def del_table(database_name: str, tb_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    select_db_command = f"USE {database_name}"
    cursor_local.execute(select_db_command)
    delete_table_command = f"DROP TABLE {tb_name}"
    cursor_local.execute(delete_table_command)
    cursor_local.close()
    connection_local.close()


def write_data_in_table(database_name: str, rows: list):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    cursor_local.execute("SELECT * FROM mentee_details")
    header_str = "reg_id, Smart_card_no, Name, Admitted_year, sakec_email, microsoft_email, mobile, " \
                 "current_division, current_roll_no, " \
                 "date_of_birth, place_of_birth, Residential_Address, Correspondent_Address, Blood_group, " \
                 "Mother_name, mother_mobile, Father_name, father_mobile, Guardian_name, guardian_mobile, " \
                 "10th_percent, 10th_institute, 10th_board, " \
                 "12th_percent, 12th_institute, 12th_board, " \
                 "CET_marks, JEE_marks, Diploma_percent, " \
                 "sem1ptr, sem2ptr, sem3ptr, sem4ptr, sem5ptr, sem6ptr, sem7ptr, sem8ptr, " \
                 "courses_done, Internship_status, publication_details, " \
                 "copyright_details, products_developed, professional_bodies, project_competitions, " \
                 "Placement_status, higher_studies_status, entrepreneurship_status"
    for record in rows:
        values = tuple([str(e) for e in record])
        cursor_local.execute(f"INSERT INTO mentee_details({header_str}) VALUES({', '.join(['%s'] * len(values))})",
                             values)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()


def update_data_in_table(database_name: str, rows: list):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    cursor_local.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor_local.execute("TRUNCATE TABLE mentee_details")
    header_str = "reg_id, Smart_card_no, Name, Admitted_year, sakec_email, microsoft_email, mobile, " \
                 "current_division, current_roll_no, " \
                 "date_of_birth, place_of_birth, Residential_Address, Correspondent_Address, Blood_group, " \
                 "Mother_name, mother_mobile, Father_name, father_mobile, Guardian_name, guardian_mobile, " \
                 "10th_percent, 10th_institute, 10th_board, " \
                 "12th_percent, 12th_institute, 12th_board, " \
                 "CET_marks, JEE_marks, Diploma_percent, " \
                 "sem1ptr, sem2ptr, sem3ptr, sem4ptr, sem5ptr, sem6ptr, sem7ptr, sem8ptr, " \
                 "courses_done, Internship_status, publication_details, " \
                 "copyright_details, products_developed, professional_bodies, project_competitions, " \
                 "Placement_status, higher_studies_status, entrepreneurship_status"
    for record in rows:
        values = tuple([str(e) for e in record])
        cursor_local.execute(f"INSERT INTO mentee_details({header_str}) VALUES({', '.join(['%s'] * len(values))})",
                             values)
    connection_local.commit()
    cursor_local.execute("SET FOREIGN_KEY_CHECKS = 1")
    cursor_local.close()
    connection_local.close()


def get_data_from_database(database_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    cursor_local.execute("SELECT * FROM mentee_details")
    result = cursor_local.fetchall()
    return result


def write_leave_table(database_name: str, leave_details: dict):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    reg_id_query = "SELECT reg_id FROM mentee_details WHERE Name = %s"
    name_value = leave_details['name']
    cursor_local.execute(reg_id_query, (name_value,))
    reg_id = cursor_local.fetchone()[0]
    cursor_local.execute("SELECT * FROM leaves")
    header_str = 'reg_id, leave_date_start, leave_date_end, leave_duration, reason, description, document_given'
    values = (reg_id, leave_details['start_date'], leave_details['end_date'], leave_details['duration'],
              leave_details['reason'], leave_details['description'], leave_details['document'])
    cursor_local.execute(f"INSERT INTO leaves({header_str}) VALUES({', '.join(['%s'] * len(values))})",
                         values)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()


def fetch_leave_details(database_name: str, mentee_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    student_name_for_query = mentee_name
    leave_detail_query = "SELECT md.Name, l.leave_date_start, l.leave_date_end, l.leave_duration, " \
                         "l.reason, l.description, l.document_given FROM mentee_details md JOIN leaves l " \
                         "ON md.reg_id = l.reg_id WHERE md.Name = %s AND l.reason = %s"
    cursor_local.execute(leave_detail_query, (student_name_for_query, 'Medical'))
    result = cursor_local.fetchall()
    return result


def write_academic_achievements_table(database_name: str, academic_achievement_details: dict):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    reg_id_query = "SELECT reg_id FROM mentee_details WHERE Name = %s"
    name_value = academic_achievement_details['name']
    cursor_local.execute(reg_id_query, (name_value,))
    reg_id = cursor_local.fetchone()[0]
    cursor_local.execute("SELECT * FROM academic_achievements")
    header_str = 'reg_id, achievement_type, achievement_rank, subject, semester, year, academic_year'
    values = (reg_id, academic_achievement_details['achievement_type'], academic_achievement_details['rank'],
              academic_achievement_details['subject'], academic_achievement_details['semester'],
              academic_achievement_details['year'], academic_achievement_details['academic_year'])
    cursor_local.execute(f"INSERT INTO academic_achievements({header_str}) VALUES({', '.join(['%s'] * len(values))})",
                         values)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()


def fetch_academic_achievements(database_name: str, mentee_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    student_name_for_query = mentee_name
    academic_achievement_detail_query = "SELECT md.Name, aa.achievement_type, aa.achievement_rank, " \
                                        "aa.subject, aa.semester, " \
                                        "aa.year, aa.academic_year FROM mentee_details md " \
                                        "JOIN academic_achievements aa ON md.reg_id = aa.reg_id WHERE md.Name = %s"
    cursor_local.execute(academic_achievement_detail_query, (student_name_for_query, ))
    result = cursor_local.fetchall()
    return result


def write_lor_loa_table(database_name: str, lor_loa_details: dict):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    reg_id_query = "SELECT reg_id FROM mentee_details WHERE Name = %s"
    name_value = lor_loa_details['name']
    cursor_local.execute(reg_id_query, (name_value,))
    reg_id = cursor_local.fetchone()[0]
    cursor_local.execute("SELECT * FROM lor_loa")
    header_str = 'reg_id, letter_type, issuing_faculty_name, reason'
    values = (reg_id, lor_loa_details['letter_type'], lor_loa_details['issuing_faculty'], lor_loa_details['reason'])
    cursor_local.execute(f"INSERT INTO lor_loa({header_str}) VALUES({', '.join(['%s'] * len(values))})",
                         values)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()


def fetch_lor_loa_details(database_name: str, mentee_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    student_name_for_query = mentee_name
    lor_loa_detail_query = "SELECT md.Name, ll.letter_type, ll.issuing_faculty_name, ll.reason " \
                           "FROM mentee_details md JOIN lor_loa ll ON md.reg_id = ll.reg_id WHERE md.Name = %s"
    cursor_local.execute(lor_loa_detail_query, (student_name_for_query,))
    result = cursor_local.fetchall()
    return result


def fetch_roll_no_div(database_name: str, mentee_names: list):
    details_to_return = []
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    roll_no_division_query = "SELECT md.current_roll_no, md.current_division FROM mentee_details md WHERE md.Name = %s"
    for name in mentee_names:
        cursor_local.execute(roll_no_division_query, (name,))
        result = cursor_local.fetchall()
        details_to_return.append(result)
    return details_to_return
