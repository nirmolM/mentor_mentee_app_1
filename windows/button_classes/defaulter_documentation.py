from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog, \
    QCalendarWidget
from functions import table_options as tb_opt
from working_data import username_password_giver as upg
from document_generators import defaulter_document_generator as doc_gen


class DefaulterDocumentGenerator(QDialog):
    def __init__(self, db_name: str, mentee_name: str, father_name: str, address: str, roll_no: str, division: str,
                 admitted_year: str):
        super().__init__()
        self.date = None
        self.admitted_year = admitted_year
        self.roll_no = roll_no
        self.division = division
        self.attendance_percentage = None
        self.father_name = father_name
        self.address = address
        self.mentee_name = mentee_name
        self.db_name = db_name
        self.setWindowTitle('Defaulters Document Generator')
        mentee_name_label = QLabel(f"Defaulter Documentation of {mentee_name}")
        mentor_name_label = QLabel(f"Mentor - {upg.get_username()}")
        attendance_label = QLabel("Select Attendance Label")
        self.attendance_box = QComboBox()
        attendance_percent = ['<75%', '<50%', '0%', 'Select Percentage']
        self.attendance_box.addItems(attendance_percent)
        self.attendance_box.setCurrentIndex(3)
        self.attendance_box.currentTextChanged.connect(self.attendance_giver)
        self.attendance_box.setDisabled(True)
        self.generate_defaulter_documentation_button = QPushButton("Generate Letter to Parent\nGenerate Undertaking")
        self.generate_defaulter_documentation_button.setDisabled(True)
        self.generate_defaulter_documentation_button.clicked.connect(self.generate_defaulter_document)
        date_label = QLabel('Select Date of w.e.f')
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.on_date_selected)
        layout = QGridLayout()
        layout.addWidget(mentee_name_label, 0, 0, 1, 2)
        layout.addWidget(mentor_name_label, 1, 0, 1, 2)
        layout.addWidget(date_label, 2, 0)
        layout.addWidget(self.calendar, 3, 0)
        layout.addWidget(attendance_label, 4, 0)
        layout.addWidget(self.attendance_box, 4, 1)
        layout.addWidget(self.generate_defaulter_documentation_button, 5, 1)
        self.setLayout(layout)

    def on_date_selected(self):
        selected_date = self.calendar.selectedDate()
        self.date = selected_date.toString("yyyy-MM-dd")
        self.attendance_box.setDisabled(False)

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
            'division': self.division,
            'date': self.date,
            'admitted_year': self.admitted_year
        }
        tb_opt.write_defaulters_table(self.db_name, defaulter_details=defaulter_details)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.parent_letter_generator(defaulter_details, filepath, upg.get_username())
        doc_gen.undertaking_student(defaulter_details, filepath, upg.get_username())
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Data was written to Database successfully!\n"
                                    "Defaulters Documents:\n"
                                    "(Letter to Parent and Undertaking)\n"
                                    "were generated successfully!")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()
