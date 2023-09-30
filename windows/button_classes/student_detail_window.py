from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog
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
        layout = QGridLayout()
        label_strings = ("Reg id: ", "Smartcard No: ", "Permanent Roll No(PRN): ", "Mobile No: ", "Division: ",
                         "Year of Admission: ", "SAKEC email id: ", "Microsoft Teams ID: ")
        labels = [QLabel(label_string) for label_string in label_strings]
        datas = (QLabel(general_details[0]), QLabel(general_details[1]), QLabel(general_details[8]),
                 QLabel(general_details[6]), QLabel(general_details[7]), QLabel(general_details[3]),
                 QLabel(general_details[4]), QLabel(general_details[5]))
        layout.addWidget(QLabel(f"Details of {self.mentee_name}: "), 0, 0, 1, 2)
        layout.addWidget(QLabel("General Details: "), 1, 0, 1, 2)
        for i, label, data in zip(range(2, len(labels)+2), labels, datas):
            layout.addWidget(label, i, 0)
            layout.addWidget(data, i, 1)
        layout.addWidget(QLabel("Personal Details: "), 10, 0, 1, 2)
        label_strings = ("Date of Birth", "Place of Birth", "Address", "Correspondent's Address", "Blood Group")
        labels = [QLabel(label_string) for label_string in label_strings]
        datas = [QLabel(personal_details[i]) for i in range(5)]
        for i, label, data in zip(range(11, len(labels)+11), labels, datas):
            layout.addWidget(label, i, 0)
            layout.addWidget(data, i, 1)
        self.setLayout(layout)
