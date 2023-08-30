from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QCalendarWidget, QPushButton, QComboBox, QLineEdit, \
    QRadioButton, QMessageBox, QFileDialog
from functions import table_options as tb_opt
from document_generators import leave_record_generator as doc_gen
from working_data import password_giver as pg


class LeaveCalculatorDashboard(QDialog):
    def __init__(self, db_name: str, mentee_name: str):
        super().__init__()
        self.mentee_name = mentee_name
        self.db_name = db_name
        self.end_date, self.start_date, self.day_count, self.description = None, None, None, None
        self.selected_end_date, self.selected_start_date, self.reason = None, None, None
        self.document_status: bool = False
        self.setWindowTitle("Select Leave Details")
        layout = QGridLayout()
        mentee_name_label = QLabel(f"Set Leave details for {self.mentee_name}")
        select_start_date_label = QLabel("Select Beginning of Leave")
        select_end_date_label = QLabel("Select End of Leave")
        self.start_date_calendar = QCalendarWidget()
        self.start_date_calendar.setGridVisible(True)
        self.start_date_calendar.selectionChanged.connect(self.on_start_date_selected)
        self.end_date_calendar = QCalendarWidget()
        self.end_date_calendar.setGridVisible(True)
        self.end_date_calendar.setDisabled(True)
        self.end_date_calendar.selectionChanged.connect(self.on_end_date_selected)
        self.calculate_days_button = QPushButton("Calculate No of Days")
        self.calculate_days_button.setToolTip("This does not account for Public Holidays")
        self.calculate_days_button.setDisabled(True)
        self.calculate_days_button.clicked.connect(self.calculate_days)
        self.total_days_label = QLabel("")
        reason_label = QLabel("Enter Reason of Leave")
        reasons = ['Medical', 'Internship', 'Course', 'STTP', 'Part-Time Job', 'Personal', 'Competition', 'Hackathon',
                   'Other', 'Select Reason']
        self.reason_input = QComboBox()
        self.reason_input.addItems(reasons)
        self.reason_input.setCurrentIndex(9)
        self.reason_input.currentTextChanged.connect(self.reason_giver)
        self.reason_input_text = QLineEdit()
        other_reason_label = QLabel("If Other: Please Write Reason in Concise Manner")
        self.reason_input_text.setDisabled(True)
        description_label = QLabel("Please write a Brief Description of reason")
        self.description_input = QLineEdit()
        self.description_input.setMinimumSize(20, 70)
        self.document_radio = QRadioButton("Document Submitted")
        self.document_radio.setDisabled(True)
        self.document_radio.clicked.connect(self.document_checker)
        self.generate_leave_record_button = QPushButton("Generate Absentia Record")
        self.generate_leave_record_button.setDisabled(True)
        self.generate_leave_record_button.clicked.connect(self.generate_absentia_record)
        layout.addWidget(mentee_name_label, 0, 0)
        layout.addWidget(select_start_date_label, 1, 0)
        layout.addWidget(select_end_date_label, 1, 1)
        layout.addWidget(self.start_date_calendar, 2, 0)
        layout.addWidget(self.end_date_calendar, 2, 1)
        layout.addWidget(self.calculate_days_button, 3, 0)
        layout.addWidget(self.total_days_label, 3, 1)
        layout.addWidget(reason_label, 4, 0)
        layout.addWidget(self.reason_input, 4, 1)
        layout.addWidget(other_reason_label, 5, 0, 1, 2)
        layout.addWidget(self.reason_input_text, 6, 0, 1, 2)
        layout.addWidget(description_label, 7, 0)
        layout.addWidget(self.description_input, 8, 0, 1, 2)
        layout.addWidget(self.document_radio, 9, 0)
        layout.addWidget(self.generate_leave_record_button, 9, 1)
        self.setLayout(layout)

    def reason_giver(self):
        self.reason_input.removeItem(9)
        if self.reason_input.currentText() != "Other":
            self.reason = self.reason_input.currentText()
        else:
            self.reason_input_text.setDisabled(False)

    def on_start_date_selected(self):
        self.selected_start_date = self.start_date_calendar.selectedDate()
        self.start_date = self.selected_start_date.toString("yyyy-MM-dd")  # Favourable format for SQL date
        self.end_date_calendar.setDisabled(False)
        self.end_date_calendar.setMinimumDate(self.selected_start_date)

    def on_end_date_selected(self):
        self.selected_end_date = self.end_date_calendar.selectedDate()
        self.end_date = self.selected_end_date.toString("yyyy-MM-dd")  # Favourable format for SQL date
        self.calculate_days_button.setDisabled(False)

    def calculate_days(self):
        self.day_count = 0
        current_date = self.selected_start_date
        while current_date <= self.selected_end_date:
            if str(current_date.dayOfWeek()) != '6' and str(current_date.dayOfWeek()) != '7':  # '6' -> Sat, '7' -> Sun
                self.day_count += 1
            current_date = current_date.addDays(1)
        self.total_days_label.setText(f"Number of Days: {self.day_count}")
        self.document_radio.setDisabled(False)

    def document_checker(self):
        if self.document_radio.isChecked():
            self.document_status = True
            self.generate_leave_record_button.setDisabled(False)
        else:
            self.generate_leave_record_button.setDisabled(True)

    def generate_absentia_record(self):
        # todo -> $BUG$ -> Causes Crash see the error that comes and rectify it
        self.description = self.description_input.text()
        if self.reason_input.currentText() == "Other":
            self.reason = self.reason_input_text.text()
        leave_details = {'name': self.mentee_name,
                         'start_date': self.start_date,
                         'end_date': self.end_date,
                         'duration': self.day_count,
                         'reason': self.reason,
                         'description': self.description,
                         'document': self.document_status}
        tb_opt.write_leave_table(self.db_name, leave_details=leave_details)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.make_leave_record(leave_details, filepath, mentor_name=f"Mentor - {pg.get_username()}")
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Data was written to Database successfully!\n"
                                    "Leave Record Document was generated successfully!")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()
