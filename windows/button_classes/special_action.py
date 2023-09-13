from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QFileDialog
from functions import table_options as tb_opt
from working_data import username_password_giver as upg


class SpecialMenteeAction(QDialog):
    def __init__(self, db_name: str, mentee_name: str):
        super().__init__()
        self.action_taken_input_text, self.outcome_improvement_input_text = None, None
        self.issue_description_text, self.issue_input_text = None, None
        self.setWindowTitle("Mentor-Mentee Issue and Special Action")
        self.db_name = db_name
        self.mentee_name = mentee_name
        self.mentor_name = upg.get_username()
        mentor_name_label = QLabel(self.mentor_name)
        mentee_name_label = QLabel(f"Issue pertaining - {self.mentee_name}")
        issue_raised_label = QLabel("Issue Raised")
        self.issue_input = QLineEdit()
        issue_description_label = QLabel("Issue Description (optional)")
        self.issue_description = QLineEdit()
        self.issue_description.setFixedWidth(500)
        self.issue_description.setFixedHeight(100)
        issue_resolution_label = QLabel("Issue Resolution")
        action_taken_label = QLabel("Action Taken")
        self.action_taken_input = QLineEdit()
        self.action_taken_input.setFixedWidth(500)
        self.action_taken_input.setFixedHeight(50)
        outcome_improvement_label = QLabel("Outcome/Improvement")
        self.outcome_improvement_input = QLineEdit()
        self.outcome_improvement_input.setFixedWidth(500)
        self.outcome_improvement_input.setFixedHeight(50)
        generate_ticket_button = QPushButton("Generate Mentor-Mentee Issue Document")
        generate_ticket_button.clicked.connect(self.make_mentee_ticket)
        layout = QGridLayout()
        layout.addWidget(mentor_name_label, 0, 0, 1, 2)
        layout.addWidget(mentee_name_label, 1, 0, 1, 2)
        layout.addWidget(issue_raised_label, 2, 0)
        layout.addWidget(self.issue_input, 2, 1)
        layout.addWidget(issue_description_label, 3, 0, 1, 2)
        layout.addWidget(self.issue_description, 4, 0, 1, 2)
        layout.addWidget(issue_resolution_label, 5, 0, 1, 2)
        layout.addWidget(action_taken_label, 6, 0, 1, 2)
        layout.addWidget(self.action_taken_input, 7, 0, 1, 2)
        layout.addWidget(outcome_improvement_label, 8, 0, 1, 2)
        layout.addWidget(self.outcome_improvement_input, 9, 0, 1, 2)
        layout.addWidget(generate_ticket_button, 10, 0, 1, 2)
        self.setLayout(layout)

    def make_mentee_ticket(self):
        self.issue_input_text = self.issue_input.text()
        self.issue_description_text = self.issue_description.text()
        self.action_taken_input_text = self.action_taken_input.text()
        self.outcome_improvement_input_text = self.outcome_improvement_input.text()
        issue_details = {
            'name': self.mentee_name,
            'issue': self.issue_input_text,
            'issue_description': self.issue_description_text,
            'action': self.action_taken_input_text,
            'outcome': self.outcome_improvement_input_text
        }
        #  todo -> Make documentation code
        tb_opt.write_special_action_table(self.db_name, issue_details=issue_details)
        """filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
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
            confirmation_widget.close()"""
