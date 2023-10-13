from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QVBoxLayout, QScrollArea, QWidget
from functions import table_options as tb_opt


class StudentDetail(QDialog):
    def __init__(self, db_name, mentee_name):
        super().__init__()
        self.db_name = db_name
        self.mentee_name = mentee_name
        self.setWindowTitle("Student Details")
        # self.showFullScreen()
        mentee_details = tb_opt.get_data_for_singular_mentee(self.db_name, self.mentee_name)
        general_details = mentee_details[0:9]
        personal_details = list(mentee_details[9:23])
        personal_details = tuple("Not Applicable" if item == "nan" else item for item in personal_details)
        pre_admission_details = list(mentee_details[23:34])
        pre_admission_details = tuple("Not Applicable" if item == "nan" else item for item in pre_admission_details)
        is_diploma = all(x == "Not Applicable" for x in pre_admission_details[3:8])
        academic_details = list(mentee_details[34:42])
        academic_details = tuple("Not Applicable" if item == "nan" else item for item in academic_details)
        college_activity_details = list(mentee_details[42:49])
        college_activity_details = \
            tuple("Not Applicable" if item == "nan" else item for item in college_activity_details)
        outcome_details = list(mentee_details[49:52])
        outcome_details = tuple("Not Applicable" if item == "nan" else item for item in outcome_details)
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        layout_main = QVBoxLayout(content_widget)
        close_window_button = QPushButton("Exit")
        close_window_button.clicked.connect(self.close_window)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(QLabel(f"Details of {self.mentee_name}: "))
        dialog_layout.addWidget(scroll_area)
        dialog_layout.addWidget(close_window_button)
        layout_grid01 = QGridLayout()
        layout_grid02 = QGridLayout()
        layout_grid03 = QGridLayout()
        layout_grid04 = QGridLayout()
        layout_grid05 = QGridLayout()
        layout_grid06 = QGridLayout()
        layout_grid07 = QGridLayout()
        layout_grid08 = QGridLayout()
        layout_grid09 = QGridLayout()
        layout_grid10 = QGridLayout()
        layout_grid11 = QGridLayout()
        layout_grid12 = QGridLayout()
        layout_grid13 = QGridLayout()
        layouts = (layout_grid01, layout_grid02, layout_grid03, layout_grid04, layout_grid05, layout_grid06,
                   layout_grid07, layout_grid08, layout_grid09, layout_grid10, layout_grid11, layout_grid12,
                   layout_grid13)
        for layout in layouts:
            layout.setVerticalSpacing(0)
        label_strings = ("Reg id: ", "Smartcard No: ", "Permanent Roll No(PRN): ", "Mobile No: ", "Division: ",
                         "Year of Admission: ", "SAKEC email id: ", "Microsoft Teams ID: ")
        labels = [QLabel(label_string) for label_string in label_strings]
        datas = (QLabel(general_details[0]), QLabel(general_details[1]), QLabel(general_details[8]),
                 QLabel(general_details[6]), QLabel(general_details[7]), QLabel(general_details[3]),
                 QLabel(general_details[4]), QLabel(general_details[5]))
        layout_grid01.setHorizontalSpacing(0)
        layout_grid01.addWidget(QLabel("<b>General Details: </b>"), 1, 0, 1, 2)
        for i, label, leaves in zip(range(2, len(labels) + 2), labels, datas):
            layout_grid01.addWidget(label, i, 0)
            layout_grid01.addWidget(leaves, i, 1)
        layout_grid01.addWidget(QLabel("<b>Personal Details: </b>"), 10, 0, 1, 2)
        label_strings = ("Date of Birth", "Place of Birth", "Address", "Correspondent's Address", "Blood Group")
        labels = [QLabel(label_string) for label_string in label_strings]
        datas = [QLabel(personal_details[i]) for i in range(5)]
        for i, label, leaves in zip(range(11, len(labels) + 11), labels, datas):
            layout_grid01.addWidget(label, i, 0)
            layout_grid01.addWidget(leaves, i, 1)
        layout_grid02.addWidget(QLabel("<b>Parent/Guardian Details: </b>"), 0, 0, 1, 4)
        layout_grid02.addWidget(QLabel("Mother"), 1, 1)
        layout_grid02.addWidget(QLabel("Father"), 1, 2)
        layout_grid02.addWidget(QLabel("Guardia"), 1, 3)
        layout_grid02.addWidget(QLabel("Name"), 2, 0)
        layout_grid02.addWidget(QLabel("Contact"), 3, 0)
        layout_grid02.addWidget(QLabel("e-mail"), 4, 0)
        datas = [QLabel(personal_details[i]) for i in range(5, 14)]
        for index, leaves in enumerate(datas[:9]):
            row = 2 + (index // 3)
            col = 1 + (index % 3)
            layout_grid02.addWidget(leaves, row, col)
        layout_grid03.addWidget(QLabel("<b>Pre-Admission Details: </b>"), 0, 0, 1, 4)
        layout_grid03.addWidget(QLabel("10th Details: "), 1, 0, 2, 1)
        labels = (QLabel("Institute Name: "), QLabel("Institute Board: "), QLabel("10th Percentage: "))
        for i, label in zip(range(1, 4), labels):
            layout_grid03.addWidget(label, 1, i)
        for i in range(3):
            layout_grid03.addWidget(QLabel(pre_admission_details[i]), 2, i + 1)
        if not is_diploma:
            layout_grid03.addWidget(QLabel("12th Details: "), 3, 0, 2, 1)
            labels = (QLabel("Institute Name: "), QLabel("Institute Board: "), QLabel("12th Percentage: "),
                      QLabel("CET Score"), QLabel("JEE Score"))
            for i, label in zip(range(1, 6), labels):
                layout_grid03.addWidget(label, 3, i)
            for i in range(5):
                layout_grid03.addWidget(QLabel(pre_admission_details[i + 3]), 4, i + 1)
        else:
            layout_grid03.addWidget(QLabel("Diploma Details: "), 3, 0, 2, 1)
            labels = (QLabel("Institute Name: "), QLabel("Institute Board: "), QLabel("Diploma Percentage: "))
            for i, label in zip(range(1, 4), labels):
                layout_grid03.addWidget(label, 3, i)
            for i in range(3):
                layout_grid03.addWidget(QLabel(pre_admission_details[i + 8]), 4, i + 1)
        layout_grid04.addWidget(QLabel("<b>College Academic Details: </b>"), 0, 0, 1, 8)
        labels = tuple([QLabel(f"Semester {i}") for i in range(1, 9)])
        for label, leaves, col in zip(labels, academic_details, range(8)):
            layout_grid04.addWidget(label, 1, col)
            layout_grid04.addWidget(QLabel(leaves), 2, col)
        layout_grid05.addWidget(QLabel("<b>College Activity Details: </b>"), 0, 0, 1, 4)
        labels = ("Courses Done", "Internship Status", "Publication Details", "Copyright Details", "Products Developed",
                  "Professional Bodies", "Project Competitions Attended")
        for i, label, leaves in zip(range(7), labels, college_activity_details):
            layout_grid05.addWidget(QLabel(label), 1, i)
            layout_grid05.addWidget(QLabel(leaves), 2, i)
        layout_grid06.addWidget(QLabel("<b>Outcome Details: </b>"), 0, 0, 1, 3)
        labels = ("Placement Status", "Higher Studies Status", "Entrepreneurship Status")
        for i, label, leaves in zip(range(3), labels, outcome_details):
            layout_grid06.addWidget(QLabel(label), 1, i)
            layout_grid06.addWidget(QLabel(leaves), 2, i)
        leaves = tb_opt.fetch_leave_details(self.db_name, self.mentee_name)
        if len(leaves) == 0:
            layout_grid07.addWidget(QLabel("<b>Leaves Taken: </b>No major/permitted leaves taken"), 0, 0)
        else:
            layout_grid07.addWidget(QLabel("<b>Leave Details: </b>"), 0, 0, 1, 7)
            labels = ("Start Date", "End Date", "Duration", "reason", "description", "document given")
            for index, label in enumerate(labels):
                layout_grid07.addWidget(QLabel(label), 1, index + 1)
            counter = 1
            for i in range(len(leaves)):
                leaves[i] = (f'Leave {counter}', leaves[i][1].strftime('%d/%m/%Y'), leaves[i][2].strftime('%d/%m/%Y'),
                             f"{leaves[i][3]} Days", leaves[i][4], leaves[i][5], "Submitted")
                counter += 1
            for index, leave in enumerate(leaves):
                for position, text in enumerate(leave):
                    layout_grid07.addWidget(QLabel(text), index + 2, position)
        academic_achievements = tb_opt.fetch_academic_achievements(self.db_name, self.mentee_name)
        if len(academic_achievements) == 0:
            layout_grid08.addWidget(QLabel("<b>Academic Achievements: </b>No Outstanding Academic Achievements"), 0, 0)
        else:
            layout_grid08.addWidget(QLabel("<b>Academic Achievement Details: </b>"), 0, 0, 1, 7)
            labels = ("Achievement Type", "Achievement Rank", "Subject", "Semester", "Year", "Academic Year")
            for index, label in enumerate(labels):
                layout_grid08.addWidget((QLabel(label)), 1, index + 1)
            counter = 1
            for i in range(len(academic_achievements)):
                academic_achievements[i] = (f'Achievement {counter}', academic_achievements[i][1],
                                            academic_achievements[i][2], academic_achievements[i][3],
                                            academic_achievements[i][4], academic_achievements[i][5],
                                            academic_achievements[i][6])
                counter += 1
                for index, achievement in enumerate(academic_achievements):
                    for position, text in enumerate(achievement):
                        layout_grid08.addWidget(QLabel(text), index + 2, position)
        lor_loa_record = tb_opt.fetch_lor_loa_details(self.db_name, self.mentee_name)
        if len(lor_loa_record) == 0:
            layout_grid09.addWidget(QLabel("<b>LOR/LOA Record: </b>No LOR/LOA Issued"), 0, 0)
        else:
            layout_grid09.addWidget(QLabel("<b>LOR/LOA Record: </b>"), 0, 0, 1, 3)
            labels = ("Letter Type", "Issuing Faculty Name", "Reason")
            for index, label in enumerate(labels):
                layout_grid09.addWidget((QLabel(label)), 1, index + 1)
            counter = 1
            for i in range(len(lor_loa_record)):
                lor_loa_record[i] = (f'Letter {counter}', lor_loa_record[i][1], lor_loa_record[i][2],
                                     lor_loa_record[i][3])
                counter += 1
                for index, letter in enumerate(lor_loa_record):
                    for position, text in enumerate(letter):
                        layout_grid09.addWidget(QLabel(text), index + 2, position)
        defaulter_record = tb_opt.fetch_defaulters_details(self.db_name, self.mentee_name)
        if len(defaulter_record) == 0:
            layout_grid10.addWidget(QLabel("<b>Defaulter Record: </b>Student has never been in defaulters"), 0, 0)
        else:
            layout_grid10.addWidget(QLabel("<b>Defaulter Record: </b>"), 0, 0, 1, 2)
            labels = ("Date", "Attendance")
            for index, label in enumerate(labels):
                layout_grid10.addWidget((QLabel(label)), 1, index + 1)
            counter = 1
            for i in range(len(defaulter_record)):
                defaulter_record[i] = (f'Defaulter {counter}', defaulter_record[i][1], defaulter_record[i][2])
                counter += 1
                for index, record in enumerate(defaulter_record):
                    for position, text in enumerate(record):
                        layout_grid10.addWidget(QLabel(text), index + 2, position)
        special_record = tb_opt.fetch_special_action_details(self.db_name, self.mentee_name)
        if len(special_record) == 0:
            layout_grid11.addWidget(QLabel("<b>Special Action Record: </b>No Special action done for mentee"), 0, 0)
        else:
            layout_grid11.addWidget(QLabel("<b>Special Action Record: </b>"), 0, 0, 1, 4)
            labels = ("Issue", "Description", "Action", "Outcome")
            for index, label in enumerate(labels):
                layout_grid11.addWidget((QLabel(label)), 1, index + 1)
            counter = 1
            for i in range(len(special_record)):
                special_record[i] = (f'Special Action {counter}', special_record[i][1], special_record[i][2],
                                     special_record[i][3], special_record[i][4])
                counter += 1
                for index, record in enumerate(special_record):
                    for position, text in enumerate(record):
                        layout_grid11.addWidget(QLabel(text), index + 2, position)
        ec_activity_record = tb_opt.fetch_college_activity_details(self.db_name, self.mentee_name)
        if len(ec_activity_record) == 0:
            layout_grid12.addWidget(QLabel("<b>Extra Curricular Record: </b>No Extra Curricular Participated"), 0, 0)
        else:
            layout_grid12.addWidget(QLabel("<b>Extra Curricular Record: </b>"), 0, 0, 1, 6)
            labels = ("Activity Type", "Role", "Role Description", "Start Date", "End Date", "Certificate Submitted")
            for index, label in enumerate(labels):
                layout_grid12.addWidget((QLabel(label)), 1, index + 1)
            counter = 1
            for i in range(len(ec_activity_record)):
                ec_activity_record[i] = (f'Activity {counter}', ec_activity_record[i][1], ec_activity_record[i][2],
                                         ec_activity_record[i][3], ec_activity_record[i][3].strftime('%d/%m/%Y'),
                                         ec_activity_record[i][4].strftime('%d/%m/%Y'), "Submitted",)
                counter += 1
            for index, activity in enumerate(ec_activity_record):
                for position, text in enumerate(activity):
                    layout_grid12.addWidget(QLabel(text), index + 2, position)
        cc_activity_record = tb_opt.fetch_co_curricular_activity_details(self.db_name, self.mentee_name)
        if len(cc_activity_record) == 0:
            layout_grid13.addWidget(QLabel("<b>Co-Curricular Record: </b>No Co-Curricular Participated"), 0, 0)
        else:
            layout_grid12.addWidget(QLabel("<b>Co-Curricular Record: </b>"), 0, 0, 1, 6)
            labels = ("Activity Type", "Particulars", "Description", "Start Date", "End Date", "Certificate Submitted")
            for index, label in enumerate(labels):
                layout_grid13.addWidget((QLabel(label)), 1, index + 1)
            counter = 1
            for i in range(len(cc_activity_record)):
                cc_activity_record[i] = (f'Activity {counter}', ec_activity_record[i][1],
                                         ec_activity_record[i][2], ec_activity_record[i][3],
                                         ec_activity_record[i][4].strftime('%d/%m/%Y'),
                                         ec_activity_record[i][5].strftime('%d/%m/%Y'), "Submitted")
                counter += 1
            for index, activity in enumerate(cc_activity_record):
                for position, text in enumerate(activity):
                    layout_grid13.addWidget(QLabel(text), index + 2, position)
        layout_main.addLayout(layout_grid01)
        layout_main.addLayout(layout_grid02)
        layout_main.addLayout(layout_grid03)
        layout_main.addLayout(layout_grid04)
        layout_main.addLayout(layout_grid05)
        layout_main.addLayout(layout_grid06)
        layout_main.addLayout(layout_grid07)
        layout_main.addLayout(layout_grid08)
        layout_main.addLayout(layout_grid09)
        layout_main.addLayout(layout_grid10)
        layout_main.addLayout(layout_grid11)
        layout_main.addLayout(layout_grid12)
        layout_main.addLayout(layout_grid13)
        self.setLayout(layout_main)

    def close_window(self):
        self.close()
