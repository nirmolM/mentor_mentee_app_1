from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog, \
    QCalendarWidget, QLineEdit, QRadioButton
from functions import table_options as tb_opt
from document_generators import college_activity_record_generator as doc_gen
from working_data import username_password_giver as upg


class CollegeActivityRecordGenerator(QDialog):
    def __init__(self, db_name: str, mentee_name: str):
        super().__init__()
        self.certificate_status = None
        self.role = None
        self.description = None
        self.activity = None
        self.selected_end_date = None
        self.end_date = None
        self.start_date = None
        self.selected_start_date = None
        self.db_name = db_name
        self.mentee_name = mentee_name
        self.setWindowTitle("Mentee College Activity Record")
        layout = QGridLayout()
        mentee_label = QLabel(f"Record for {self.mentee_name}")
        activity_label = QLabel("Select College Activity Type")
        activity_list = ['Event Volunteer', 'Event Coordinator', 'Cell Member', 'Festival event coordinator',
                         'Magazine/Newsletter Editor', 'Student Council Member', 'SAKEC Studio Member',
                         'Silver Steppers Member', 'Drama Club Member', 'Art Club Member', 'Sports Team Member',
                         'Other']
        self.activity_list_box = QComboBox()
        self.activity_list_box.addItems(activity_list)
        self.activity_list_box.currentTextChanged.connect(self.activity_giver)
        self.activity_input_text = QLineEdit()
        other_activity_label = QLabel("If Other: Please Write Activity in Concise Manner")
        self.activity_input_text.setDisabled(True)
        role_label = QLabel("Select Role")
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Example: Council General Secretary/Research Cell Member")
        role_description_label = QLabel("Give brief Description of role/activity")
        self.role_description_input = QLineEdit()
        self.role_description_input.setPlaceholderText("Example: Handled Infra-Security/Documentation/Team Captain")
        self.role_description_input.setMinimumSize(20, 70)
        self.multiple_date_radio = QRadioButton("Multiple Day Event")
        event_date_label = QLabel("Select Date of Event")
        self.start_date_calender = QCalendarWidget()
        self.start_date_calender.setGridVisible(True)
        self.start_date_calender.selectionChanged.connect(self.on_start_date_selected)
        end_date_label = QLabel("Select End Date Of Event")
        self.end_date_calender = QCalendarWidget()
        self.end_date_calender.setGridVisible(True)
        self.end_date_calender.setDisabled(True)
        self.end_date_calender.selectionChanged.connect(self.on_end_date_selected)
        self.generate_activity_record_button = QPushButton("Generate Activity Record")
        self.generate_activity_record_button.clicked.connect(self.generate_activity_record)
        self.generate_activity_record_button.setDisabled(True)
        self.certificate_radio = QRadioButton("Certificate Submitted")
        self.certificate_radio.clicked.connect(self.certificate_checker)
        layout.addWidget(mentee_label, 0, 0, 1, 2)
        layout.addWidget(activity_label, 1, 0)
        layout.addWidget(self.activity_list_box, 1, 1)
        layout.addWidget(other_activity_label, 2, 0, 1, 2)
        layout.addWidget(self.activity_input_text, 3, 0, 1, 2)
        layout.addWidget(role_label, 4, 0)
        layout.addWidget(self.role_input, 4, 1)
        layout.addWidget(role_description_label, 5, 0, 1, 2)
        layout.addWidget(self.role_description_input, 6, 0, 1, 2)
        layout.addWidget(self.multiple_date_radio, 7, 0, 1, 2)
        layout.addWidget(event_date_label, 8, 0)
        layout.addWidget(end_date_label, 8, 1)
        layout.addWidget(self.start_date_calender, 9, 0)
        layout.addWidget(self.end_date_calender, 9, 1)
        layout.addWidget(self.certificate_radio, 10, 0)
        layout.addWidget(self.generate_activity_record_button, 10, 1)
        self.setLayout(layout)

    def activity_giver(self):
        if self.activity_list_box.currentText() != "Other":
            self.activity = self.activity_list_box.currentText()
        else:
            self.activity_input_text.setDisabled(False)

    def on_start_date_selected(self):
        self.selected_start_date = self.start_date_calender.selectedDate()
        self.start_date = self.selected_start_date.toString("yyyy-MM-dd")  # Favourable format for SQL date
        self.end_date = "NULL"
        if self.multiple_date_radio.isChecked():
            self.end_date_calender.setDisabled(False)
            self.end_date_calender.setMinimumDate(self.selected_start_date)

    def on_end_date_selected(self):
        self.selected_end_date = self.end_date_calender.selectedDate()
        self.end_date = self.selected_end_date.toString("yyyy-MM-dd")  # Favourable format for SQL date

    def certificate_checker(self):
        if self.certificate_radio.isChecked():
            self.certificate_status = True
            self.generate_activity_record_button.setDisabled(False)
        else:
            self.generate_activity_record_button.setDisabled(True)

    def generate_activity_record(self):
        self.role = self.role_input.text()
        self.description = self.role_description_input.text()
        if self.activity_list_box.currentText() == "Other":
            self.activity = self.activity_input_text.text()
        activity_details = {
            'name': self.mentee_name,
            'activity_type': self.activity,
            'role': self.role,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'certificate': self.certificate_status
        }
        tb_opt.write_college_activity_table(self.db_name, activity_details=activity_details)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.make_college_activity_record(activity_details, filepath, mentor_name=f"Mentor - {upg.get_username()}")
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
