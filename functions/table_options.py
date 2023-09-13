import mysql.connector
from working_data import username_password_giver as upg


def make_connection():
    connection = mysql.connector.connect(user='root', password=upg.give_password(), host='localhost', buffered=True)
    return connection


def give_reg_id(database_name: str, mentee_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    cursor_local.execute("SELECT reg_id FROM mentee_details WHERE Name = %s", (mentee_name,))
    return cursor_local.fetchone()[0]


def generalised_fetch_function(database_name: str, mentee_name: str, query: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    cursor_local.execute(query, (mentee_name,))
    return cursor_local.fetchall()


def generalised_write_function(database_name: str, tb_name: str, header_str: str, values):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    cursor_local.execute(f"SELECT * FROM {tb_name}")
    cursor_local.execute(f"INSERT INTO {tb_name}({header_str}) VALUES({', '.join(['%s'] * len(values))})",
                         values)
    connection_local.commit()
    cursor_local.close()
    connection_local.close()


def create_table(database_name: str):
    connection_local = make_connection()
    cursor_local = connection_local.cursor()
    cursor_local.execute(f"USE {database_name}")
    create_main_table_command = 'CREATE TABLE mentee_details (reg_id char(5) PRIMARY KEY, ' \
                                'Smart_card_no varchar(20), Name varchar(150), Admitted_year varchar(10), ' \
                                'sakec_email varchar(100), microsoft_email varchar(100), mobile varchar(15),' \
                                'current_division varchar(4), current_roll_no varchar(15),' \
                                'date_of_birth varchar(11), place_of_birth varchar(11), ' \
                                'Residential_Address varchar(255), Correspondent_Address varchar(255), ' \
                                'Blood_group varchar(4),' \
                                'Mother_name varchar(20), mother_mobile varchar(15), mother_email varchar(25), ' \
                                'Father_name varchar(20), father_mobile varchar(15), father_email varchar(25), ' \
                                'Guardian_name varchar(20), guardian_mobile varchar(15), guardian_email varchar(25), ' \
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
    create_defaulters_details_table_command = 'CREATE TABLE defaulters (defaulter_id SERIAL PRIMARY KEY, ' \
                                              'reg_id char(5), wef_date DATE, attendance_percentage varchar(6), ' \
                                              'FOREIGN KEY (reg_id) REFERENCES mentee_details(reg_id))'
    cursor_local.execute(create_defaulters_details_table_command)
    create_special_action_details_table_command = 'CREATE TABLE special_action (action_id SERIAL PRIMARY KEY, ' \
                                                  'reg_id char(5), issue varchar(100), description varchar(255), ' \
                                                  'action varchar(255), outcome varchar(255), ' \
                                                  'FOREIGN KEY (reg_id) REFERENCES mentee_details(reg_id))'
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
                 "Mother_name, mother_mobile, mother_email, " \
                 "Father_name, father_mobile, father_email, " \
                 "Guardian_name, guardian_mobile, guardian_email, " \
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
                 "Mother_name, mother_mobile, mother_email, " \
                 "Father_name, father_mobile, father_email, " \
                 "Guardian_name, guardian_mobile, guardian_email, " \
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
    header_str = 'reg_id, leave_date_start, leave_date_end, leave_duration, reason, description, document_given'
    values = (give_reg_id(database_name, leave_details['name']), leave_details['start_date'], leave_details['end_date'],
              leave_details['duration'], leave_details['reason'], leave_details['description'],
              leave_details['document'])
    generalised_write_function(database_name, 'leaves', header_str, values)


def fetch_leave_details(database_name: str, mentee_name: str):
    leave_detail_query = "SELECT md.Name, l.leave_date_start, l.leave_date_end, l.leave_duration, " \
                         "l.reason, l.description, l.document_given FROM mentee_details md JOIN leaves l " \
                         "ON md.reg_id = l.reg_id WHERE md.Name = %s"
    return generalised_fetch_function(database_name, mentee_name, leave_detail_query)


def write_academic_achievements_table(database_name: str, academic_achievement_details: dict):
    header_str = 'reg_id, achievement_type, achievement_rank, subject, semester, year, academic_year'
    values = (give_reg_id(database_name, academic_achievement_details['name']),
              academic_achievement_details['achievement_type'], academic_achievement_details['rank'],
              academic_achievement_details['subject'], academic_achievement_details['semester'],
              academic_achievement_details['year'], academic_achievement_details['academic_year'])
    generalised_write_function(database_name, 'academic_achievements', header_str, values)


def fetch_academic_achievements(database_name: str, mentee_name: str):
    academic_achievement_detail_query = "SELECT md.Name, aa.achievement_type, aa.achievement_rank, " \
                                        "aa.subject, aa.semester, " \
                                        "aa.year, aa.academic_year FROM mentee_details md " \
                                        "JOIN academic_achievements aa ON md.reg_id = aa.reg_id WHERE md.Name = %s"
    return generalised_fetch_function(database_name, mentee_name, academic_achievement_detail_query)


def write_lor_loa_table(database_name: str, lor_loa_details: dict):
    header_str = 'reg_id, letter_type, issuing_faculty_name, reason'
    values = (give_reg_id(database_name, lor_loa_details['name']), lor_loa_details['letter_type'],
              lor_loa_details['issuing_faculty'], lor_loa_details['reason'])
    generalised_write_function(database_name, 'lor_loa', header_str, values)


def fetch_lor_loa_details(database_name: str, mentee_name: str):
    lor_loa_detail_query = "SELECT md.Name, ll.letter_type, ll.issuing_faculty_name, ll.reason " \
                           "FROM mentee_details md JOIN lor_loa ll ON md.reg_id = ll.reg_id WHERE md.Name = %s"
    return generalised_fetch_function(database_name, mentee_name, lor_loa_detail_query)


def write_defaulters_table(database_name: str, defaulter_details: dict):
    header_str = 'reg_id, wef_date, attendance_percentage'
    values = (give_reg_id(database_name, defaulter_details['name']),
              defaulter_details['date'], defaulter_details['attendance'])
    generalised_write_function(database_name, 'defaulters', header_str, values)


def fetch_defaulters_details(database_name: str, mentee_name: str):
    defaulters_query = "SELECT md.Name, d.wef_date, d.attendance_percentage " \
                       "FROM mentee_details md JOIN defaulters d ON md.reg_id = d.reg_id WHERE md.Name = %s"
    return generalised_fetch_function(database_name, mentee_name, defaulters_query)


def write_special_action_table(database_name: str, issue_details: dict):
    header_str = 'reg_id, issue, description, action, outcome'
    values = (give_reg_id(database_name, issue_details['name']),
              issue_details['issue'], issue_details['issue_description'],
              issue_details['action'], issue_details['outcome'])
    generalised_write_function(database_name, 'special_action', header_str, values)


def fetch_special_action_details(database_name: str, mentee_name: str):
    special_action_query = "SELECT md.Name, sa.issue, sa.description, sa.action, sa.outcome " \
                       "FROM mentee_details md JOIN special_action sa ON md.reg_id = sa.reg_id WHERE md.Name = %s"
    return generalised_fetch_function(database_name, mentee_name, special_action_query)
