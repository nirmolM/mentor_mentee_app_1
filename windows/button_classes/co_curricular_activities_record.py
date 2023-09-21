from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog, \
    QCalendarWidget, QLineEdit, QRadioButton
from functions import table_options as tb_opt
from document_generators import co_curricular_activity_record_generator as doc_gen
from working_data import username_password_giver as upg


class CoCurricularActivityRecord(QDialog):
    def __init__(self, db_name: str, mentee_name: str):
        super().__init__()
        self.description = None
        self.particulars = None
        self.certificate_status = None
        self.selected_end_date = None
        self.end_date = None
        self.start_date = None
        self.selected_start_date = None
        self.cc_activity = None
        self.db_name = db_name
        self.mentee_name = mentee_name
        self.setWindowTitle("Mentee Co-Curricular Activity Record")
        layout = QGridLayout()
        mentee_label = QLabel(f"Record for {self.mentee_name}")
        cc_activity_label = QLabel("Select Co-Curricular Activity Type")
        cc_activity_list = ['Competition Participation', 'Project Presentation', 'Paper Presentation',
                            'Online Course', 'Copyright', 'Internship', 'Certification', 'Product Developed',
                            'Workshop', 'Student Development Program', 'Other']
        self.cc_activity_list_box = QComboBox()
        self.cc_activity_list_box.addItems(cc_activity_list)
        self.cc_activity_list_box.currentTextChanged.connect(self.cc_activity_giver)
        self.cc_activity_input_text = QLineEdit()
        cc_other_activity_label = QLabel("If Other: Please Write Activity in Concise Manner")
        self.cc_activity_input_text.setDisabled(True)
        particulars_label = QLabel("Select Role")
        self.particulars_input = QLineEdit()
        self.particulars_input.setPlaceholderText("Example: Spoken Tutorial Course/In-house College Internship")
        particulars_description_label = QLabel("Give brief Description of activity")
        self.cc_description_input = QLineEdit()
        self.cc_description_input.setPlaceholderText("Example: Spoken Tutorial on C/Robotics Workshop")
        self.cc_description_input.setMinimumSize(20, 70)
        self.cc_multiple_date_radio = QRadioButton("Multiple Day Event")
        cc_date_label = QLabel("Select Date of Event")
        self.start_date_calender = QCalendarWidget()
        self.start_date_calender.setGridVisible(True)
        self.start_date_calender.selectionChanged.connect(self.on_start_date_selected)
        cc_end_date_label = QLabel("Select End Date Of Event")
        self.end_date_calender = QCalendarWidget()
        self.end_date_calender.setGridVisible(True)
        self.end_date_calender.setDisabled(True)
        self.end_date_calender.selectionChanged.connect(self.on_end_date_selected)
        self.generate_cc_activity_record_button = QPushButton("Generate Activity Record")
        self.generate_cc_activity_record_button.clicked.connect(self.generate_cc_activity_record)
        self.generate_cc_activity_record_button.setDisabled(True)
        self.certificate_radio = QRadioButton("Certificate Submitted")
        self.certificate_radio.clicked.connect(self.certificate_checker)
        layout.addWidget(mentee_label, 0, 0, 1, 2)
        layout.addWidget(cc_activity_label, 1, 0)
        layout.addWidget(self.cc_activity_list_box, 1, 1)
        layout.addWidget(cc_other_activity_label, 2, 0, 1, 2)
        layout.addWidget(self.cc_activity_input_text, 3, 0, 1, 2)
        layout.addWidget(particulars_label, 4, 0)
        layout.addWidget(self.particulars_input, 4, 1)
        layout.addWidget(particulars_description_label, 5, 0, 1, 2)
        layout.addWidget(self.cc_description_input, 6, 0, 1, 2)
        layout.addWidget(self.cc_multiple_date_radio, 7, 0, 1, 2)
        layout.addWidget(cc_date_label, 8, 0)
        layout.addWidget(cc_end_date_label, 8, 1)
        layout.addWidget(self.start_date_calender, 9, 0)
        layout.addWidget(self.end_date_calender, 9, 1)
        layout.addWidget(self.certificate_radio, 10, 0)
        layout.addWidget(self.generate_cc_activity_record_button, 10, 1)
        self.setLayout(layout)

    def cc_activity_giver(self):
        if self.cc_activity_list_box.currentText() != "Other":
            self.cc_activity = self.cc_activity_list_box.currentText()
        else:
            self.cc_activity_input_text.setDisabled(False)

    def on_start_date_selected(self):
        self.selected_start_date = self.start_date_calender.selectedDate()
        self.start_date = self.selected_start_date.toString("yyyy-MM-dd")  # Favourable format for SQL date
        self.end_date = "NULL"
        if self.cc_multiple_date_radio.isChecked():
            self.end_date_calender.setDisabled(False)
            self.end_date_calender.setMinimumDate(self.selected_start_date)

    def on_end_date_selected(self):
        self.selected_end_date = self.end_date_calender.selectedDate()
        self.end_date = self.selected_end_date.toString("yyyy-MM-dd")  # Favourable format for SQL date

    def certificate_checker(self):
        if self.certificate_radio.isChecked():
            self.certificate_status = True
            self.generate_cc_activity_record_button.setDisabled(False)
        else:
            self.generate_cc_activity_record_button.setDisabled(True)

    def generate_cc_activity_record(self):
        self.particulars = self.particulars_input.text()
        self.description = self.cc_description_input.text()
        if self.cc_activity_list_box.currentText() == "Other":
            self.cc_activity = self.cc_activity_input_text.text()
        cc_activity_details = {
            'name': self.mentee_name,
            'cc_activity_type': self.cc_activity,
            'particulars': self.particulars,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'certificate': self.certificate_status
        }
        tb_opt.write_co_curricular_activity_table(self.db_name, cc_activity_details=cc_activity_details)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.make_cc_activity_record(cc_activity_details, filepath, mentor_name=f"Mentor - {upg.get_username()}")
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Data was written to Database successfully!\n"
                                    "Activity Record Document was generated successfully!")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()
