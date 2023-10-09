import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog, \
    QVBoxLayout, QScrollArea, QWidget
from functions import table_options as tb_opt


class StudentDetail(QDialog):
    def __init__(self, db_name, mentee_name):
        super().__init__()
        self.db_name = db_name
        self.mentee_name = mentee_name
        self.setWindowTitle("Student Details")
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
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll_area)
        layout_grid1 = QGridLayout()
        layout_grid2 = QGridLayout()
        layout_grid3 = QGridLayout()
        layout_grid4 = QGridLayout()
        layout_grid5 = QGridLayout()
        layout_grid6 = QGridLayout()
        layout_grid7 = QGridLayout()
        label_strings = ("Reg id: ", "Smartcard No: ", "Permanent Roll No(PRN): ", "Mobile No: ", "Division: ",
                         "Year of Admission: ", "SAKEC email id: ", "Microsoft Teams ID: ")
        labels = [QLabel(label_string) for label_string in label_strings]
        datas = (QLabel(general_details[0]), QLabel(general_details[1]), QLabel(general_details[8]),
                 QLabel(general_details[6]), QLabel(general_details[7]), QLabel(general_details[3]),
                 QLabel(general_details[4]), QLabel(general_details[5]))
        layout_grid1.addWidget(QLabel(f"Details of {self.mentee_name}: "), 0, 0, 1, 2)
        layout_grid1.addWidget(QLabel("General Details: "), 1, 0, 1, 2)
        for i, label, leaves in zip(range(2, len(labels)+2), labels, datas):
            layout_grid1.addWidget(label, i, 0)
            layout_grid1.addWidget(leaves, i, 1)
        layout_grid1.addWidget(QLabel("Personal Details: "), 10, 0, 1, 2)
        label_strings = ("Date of Birth", "Place of Birth", "Address", "Correspondent's Address", "Blood Group")
        labels = [QLabel(label_string) for label_string in label_strings]
        datas = [QLabel(personal_details[i]) for i in range(5)]
        for i, label, leaves in zip(range(11, len(labels)+11), labels, datas):
            layout_grid1.addWidget(label, i, 0)
            layout_grid1.addWidget(leaves, i, 1)
        layout_grid2.addWidget(QLabel("Parent/Guardian Details: "), 0, 0, 1, 4)
        layout_grid2.addWidget(QLabel("Mother"), 1, 1)
        layout_grid2.addWidget(QLabel("Father"), 1, 2)
        layout_grid2.addWidget(QLabel("Guardia"), 1, 3)
        layout_grid2.addWidget(QLabel("Name"), 2, 0)
        layout_grid2.addWidget(QLabel("Contact"), 3, 0)
        layout_grid2.addWidget(QLabel("e-mail"), 4, 0)
        datas = [QLabel(personal_details[i]) for i in range(5, 14)]
        for index, leaves in enumerate(datas[:9]):
            row = 2 + (index // 3)
            col = 1 + (index % 3)
            layout_grid2.addWidget(leaves, row, col)
        layout_grid3.addWidget(QLabel("Pre-Admission Details: "), 0, 0, 1, 4)
        layout_grid3.addWidget(QLabel("10th Details: "), 1, 0, 2, 1)
        labels = (QLabel("Institute Name: "), QLabel("Institute Board: "), QLabel("10th Percentage: "))
        for i, label in zip(range(1, 4), labels):
            layout_grid3.addWidget(label, 1, i)
        for i in range(3):
            layout_grid3.addWidget(QLabel(pre_admission_details[i]), 2, i+1)
        if not is_diploma:
            layout_grid3.addWidget(QLabel("12th Details: "), 3, 0, 2, 1)
            labels = (QLabel("Institute Name: "), QLabel("Institute Board: "), QLabel("12th Percentage: "),
                      QLabel("CET Score"), QLabel("JEE Score"))
            for i, label in zip(range(1, 6), labels):
                layout_grid3.addWidget(label, 3, i)
            for i in range(5):
                layout_grid3.addWidget(QLabel(pre_admission_details[i+3]), 4, i+1)
        else:
            layout_grid3.addWidget(QLabel("Diploma Details: "), 3, 0, 2, 1)
            labels = (QLabel("Institute Name: "), QLabel("Institute Board: "), QLabel("Diploma Percentage: "))
            for i, label in zip(range(1, 4), labels):
                layout_grid3.addWidget(label, 3, i)
            for i in range(3):
                layout_grid3.addWidget(QLabel(pre_admission_details[i + 8]), 4, i + 1)
        layout_grid4.addWidget(QLabel("College Academic Details: "), 0, 0, 1, 8)
        labels = tuple([QLabel(f"Semester {i}") for i in range(1, 9)])
        for label, leaves, col in zip(labels, academic_details, range(8)):
            layout_grid4.addWidget(label, 1, col)
            layout_grid4.addWidget(QLabel(leaves), 2, col)
        layout_grid5.addWidget(QLabel("College Activity Details: "), 0, 0, 1, 4)
        labels = ("Courses Done", "Internship Status", "Publication Details", "Copyright Details", "Products Developed",
                  "Professional Bodies", "Project Competitions Attended")
        for i, label, leaves in zip(range(7), labels, college_activity_details):
            layout_grid5.addWidget(QLabel(label), 1, i)
            layout_grid5.addWidget(QLabel(leaves), 2, i)
        layout_grid6.addWidget(QLabel("College Activity Details: "), 0, 0, 1, 3)
        labels = ("Placement Status", "Higher Studies Status", "Entrepreneurship Status")
        for i, label, leaves in zip(range(3), labels, outcome_details):
            layout_grid6.addWidget(QLabel(label), 1, i)
            layout_grid6.addWidget(QLabel(leaves), 2, i)
        leaves = tb_opt.fetch_leave_details(self.db_name, self.mentee_name)
        if len(leaves) == 0:
            layout_grid7.addWidget(QLabel("Leaves Taken: No major/permitted leaves taken"), 0, 0)
        else:
            layout_grid7.addWidget(QLabel("Leave Details: "), 0, 0, 1, 7)
            labels = ("Start Date", "End Date", "Duration", "reason", "description", "document given")
            for index, label in enumerate(labels):
                layout_grid7.addWidget(QLabel(label), 1, index+1)
            counter = 1
            for i in range(len(leaves)):
                leave_name = f'Leave {counter}'
                start_date = leaves[i][1].strftime('%d/%m/%Y')
                end_date = leaves[i][2].strftime('%d/%m/%Y')
                duration = f"{leaves[i][3]} Days"
                reason = leaves[i][4]
                description = leaves[i][5]
                leaves[i] = (leave_name, start_date, end_date, duration, reason, description, "Submitted")
                counter += 1
            for index, leave in enumerate(leaves):
                for position, text in enumerate(leave):
                    layout_grid7.addWidget(QLabel(text), index+2, position)
        layout_main.addLayout(layout_grid1)
        layout_main.addLayout(layout_grid2)
        layout_main.addLayout(layout_grid3)
        layout_main.addLayout(layout_grid4)
        layout_main.addLayout(layout_grid5)
        layout_main.addLayout(layout_grid6)
        layout_main.addLayout(layout_grid7)
        self.setLayout(layout_main)
