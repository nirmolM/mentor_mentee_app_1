from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog
from working_data import password_giver as pg
from document_generators import defaulter_document_generator as doc_gen


class DefaulterDocumentGenerator(QDialog):
    def __init__(self, db_name: str, mentee_name: str, father_name: str, address: str, roll_no: str, division: str):
        super().__init__()
        self.roll_no = roll_no
        self.division = division
        self.attendance_percentage = None
        self.father_name = father_name
        self.address = address
        self.mentee_name = mentee_name
        self.db_name = db_name
        self.setWindowTitle('Defaulters Document Generator')
        mentee_name_label = QLabel(f"Defaulter Documentation of {mentee_name}")
        mentor_name_label = QLabel(f"Mentor - {pg.get_username()}")
        attendance_label = QLabel("Select Attendance Label")
        self.attendance_box = QComboBox()
        attendance_percent = ['<75%', '<50%', '0%', 'Select Percentage']
        self.attendance_box.addItems(attendance_percent)
        self.attendance_box.currentTextChanged.connect(self.attendance_giver)
        self.generate_defaulter_documentation_button = QPushButton("Generate Letter to Parent\nGenerate Undertaking")
        self.generate_defaulter_documentation_button.setDisabled(True)
        self.generate_defaulter_documentation_button.clicked.connect(self.generate_defaulter_document)
        layout = QGridLayout()
        layout.addWidget(mentee_name_label, 0, 0, 1, 2)
        layout.addWidget(mentor_name_label, 1, 0, 1, 2)
        layout.addWidget(attendance_label, 2, 0)
        layout.addWidget(self.attendance_box, 2, 1)
        layout.addWidget(self.generate_defaulter_documentation_button, 3, 1)
        self.setLayout(layout)

    def attendance_giver(self):
        self.attendance_box.removeItem(3)
        self.attendance_percentage = self.attendance_box.currentText()
        self.generate_defaulter_documentation_button.setDisabled(False)

    def generate_defaulter_document(self):
        defaulter_details = {
            'name': self.mentee_name,
            'attendance': self.attendance_percentage,
            'father_name': self.father_name,
            'address': self.address,
            'roll_no': self.roll_no,
            'division': self.division
        }
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.parent_letter_generator(defaulter_details, filepath, pg.get_username())
        doc_gen.undertaking_student(defaulter_details, filepath, pg.get_username())
