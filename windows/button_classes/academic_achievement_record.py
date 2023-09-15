from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QComboBox, QLineEdit, QPushButton, QRadioButton, \
    QMessageBox, QFileDialog
from functions import table_options as tb_opt
from document_generators import academic_achievement_record_generator as doc_gen
from working_data import username_password_giver as upg


class AcademicAchievementsDashboard(QDialog):
    def __init__(self, db_name: str, mentee_name: str):
        super().__init__()
        self.db_name = db_name
        self.letter_type = None
        self.achievement_type_text, self.rank_text, self.subject_text, self.semester_text, self.year_text = \
            None, None, None, None, None
        self.setWindowTitle("Set Academic Achievement/LoR/LoA Record")
        layout = QGridLayout()
        self.mentee_name = mentee_name
        mentee_name_label = QLabel(f"Set Academic Achievement Record for {self.mentee_name}")
        achievement_label = QLabel("Select Achievement")
        achievement_list = ["Subject Topper", "Semester Topper", "Year Topper",
                            "College Topper", "University Topper", "Other", "Select Achievement Type"]
        rank_list = ["First Rank", "Second Rank", "Third Rank", "Select Rank"]
        self.achievement_type_box = QComboBox()
        self.achievement_type_box.addItems(achievement_list)
        self.achievement_type_box.setCurrentIndex(6)
        self.achievement_type_box.currentTextChanged.connect(self.enable_rank_or_other_field)
        self.rank_box = QComboBox()
        self.rank_box.addItems(rank_list)
        self.rank_box.setCurrentIndex(3)
        self.rank_box.currentTextChanged.connect(self.give_rank)
        self.rank_box.setDisabled(True)
        subject_label = QLabel("Enter Subject: ")
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Enter Subject")
        self.subject_input.setDisabled(True)
        semester_label = QLabel("Enter Semester: ")
        self.semester_input = QComboBox()
        self.semester_input.addItems(['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4',
                                      'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8',
                                      'Select Semester'])
        self.semester_input.setCurrentIndex(8)
        self.semester_input.currentTextChanged.connect(self.give_semester)
        self.semester_input.setDisabled(True)
        year_label = QLabel("Enter Year: ")
        self.year_input = QComboBox()
        self.year_input.addItems(['First Year', 'Second Year', 'Third Year', 'Final Year', 'Select Year'])
        self.year_input.setCurrentIndex(4)
        self.year_input.setDisabled(True)
        self.year_input.currentTextChanged.connect(self.give_year)
        academic_year_label = QLabel("Enter Academic Year: ")
        self.academic_year_input = QLineEdit()
        self.academic_year_input.setPlaceholderText("Example: 2023-24")
        self.academic_year_input.setDisabled(True)
        other_input_label = QLabel("If Achievement type is other, Please Enter Details of Type and Rank: ")
        self.other_achievement_input = QLineEdit()
        self.other_achievement_input.setPlaceholderText("Eg 'Avishkar Competition' / 'Smart India Hackathon'")
        self.other_achievement_input.setDisabled(True)
        self.other_achievement_rank = QLineEdit()
        self.other_achievement_rank.setPlaceholderText("Eg 'First Prize' / 'Participation'")
        self.other_achievement_rank.setDisabled(True)
        self.generate_academic_achievement_button = QPushButton("Generate Academic Achievement Record")
        self.generate_academic_achievement_button.clicked.connect(self.generate_academic_achievement_record)
        self.generate_academic_achievement_button.setDisabled(True)
        self.LoR_LoA_radio = QRadioButton("Select to Generate LoR/LoA record")
        self.LoR_LoA_radio.clicked.connect(self.lor_loa_maker)
        self.lor_loa_label = QLabel("Select Type of Letter: ")
        self.lor_loa_box = QComboBox()
        self.lor_loa_box.addItems(['Letter of Recommendation', 'Letter of Appreciation', 'Select Letter'])
        self.lor_loa_box.setCurrentIndex(2)
        self.lor_loa_box.setDisabled(True)
        self.lor_loa_box.currentTextChanged.connect(self.give_letter_type)
        issuing_faculty_label = QLabel("Faculty member issuing the letter: ")
        self.faculty_name_input = QLineEdit()
        self.faculty_name_input.setDisabled(True)
        lor_loa_reason_label = QLabel("Reason for issuing letter: ")
        self.lor_loa_reason_input = QLineEdit()
        self.lor_loa_reason_input.setPlaceholderText("Eg: LoR - Higher Studies LoA - Council Work")
        self.lor_loa_reason_input.setDisabled(True)
        self.generate_lor_loa_record_button = QPushButton("Generate LoR/LoA Record")
        self.generate_lor_loa_record_button.clicked.connect(self.generate_lor_loa_record)
        self.generate_lor_loa_record_button.setDisabled(True)
        layout.addWidget(mentee_name_label, 0, 0, 1, 3)
        layout.addWidget(achievement_label, 1, 0)
        layout.addWidget(self.achievement_type_box, 1, 1)
        layout.addWidget(self.rank_box, 1, 2)
        layout.addWidget(subject_label, 2, 0)
        layout.addWidget(self.subject_input, 2, 1, 1, 2)
        layout.addWidget(semester_label, 3, 0)
        layout.addWidget(self.semester_input, 3, 1, 1, 2)
        layout.addWidget(year_label, 4, 0)
        layout.addWidget(self.year_input, 4, 1, 1, 2)
        layout.addWidget(other_input_label, 5, 0, 1, 3)
        layout.addWidget(self.other_achievement_input, 6, 0, 1, 2)
        layout.addWidget(self.other_achievement_rank, 6, 2)
        layout.addWidget(academic_year_label, 7, 0)
        layout.addWidget(self.academic_year_input, 7, 1, 1, 2)
        layout.addWidget(self.generate_academic_achievement_button, 8, 0, 1, 2)
        layout.addWidget(self.LoR_LoA_radio, 9, 0, 1, 3)
        layout.addWidget(self.lor_loa_label, 10, 0)
        layout.addWidget(self.lor_loa_box, 10, 1, 1, 2)
        layout.addWidget(issuing_faculty_label, 11, 0)
        layout.addWidget(self.faculty_name_input, 11, 1, 1, 2)
        layout.addWidget(lor_loa_reason_label, 12, 0)
        layout.addWidget(self.lor_loa_reason_input, 12, 1, 1, 2)
        layout.addWidget(self.generate_lor_loa_record_button, 13, 0, 1, 2)
        self.setLayout(layout)

    def enable_rank_or_other_field(self):
        self.academic_year_input.setDisabled(False)
        self.achievement_type_box.removeItem(6)
        if self.achievement_type_box.currentText() != "Other":
            self.other_achievement_input.setDisabled(True)
            self.rank_box.setDisabled(False)
            self.achievement_type_text = self.achievement_type_box.currentText()
            match self.achievement_type_text:
                case 'Subject Topper':
                    self.input_field_bools(False, False, False)
                case 'Semester Topper':
                    self.input_field_bools(True, False, False)
                case 'Year Topper':
                    self.input_field_bools(True, True, False)
                case _:
                    self.input_field_bools(True, True, True)
        else:
            self.other_achievement_input.setDisabled(False)
            self.other_achievement_rank.setDisabled(False)
            self.rank_box.setDisabled(True)
            self.input_field_bools(True, True, True)
        self.generate_academic_achievement_button.setDisabled(False)

    def input_field_bools(self, bool1: bool, bool2: bool, bool3: bool):
        self.subject_input.setDisabled(bool1)
        self.semester_input.setDisabled(bool2)
        self.year_input.setDisabled(bool3)

    def give_rank(self):
        self.rank_box.removeItem(3)
        self.rank_text = self.rank_box.currentText()

    def give_semester(self):
        self.semester_input.removeItem(8)
        self.subject_text = self.subject_input.text()
        self.semester_text = self.semester_input.currentText()
        match self.semester_text:
            case 'Semester 1' | 'Semester 2':
                self.year_input.setCurrentIndex(0)
                self.year_text = self.year_input.currentText()
            case 'Semester 3' | 'Semester 4':
                self.year_input.setCurrentIndex(1)
                self.year_text = self.year_input.currentText()
            case 'Semester 5' | 'Semester 6':
                self.year_input.setCurrentIndex(2)
                self.year_text = self.year_input.currentText()
            case 'Semester 7' | 'Semester 8':
                self.year_input.setCurrentIndex(3)
                self.year_text = self.year_input.currentText()

    def give_year(self):
        self.year_input.removeItem(4)
        self.year_text = self.year_input.currentText()

    def generate_academic_achievement_record(self):
        academic_achievement_details = {
            'name': self.mentee_name,
            'achievement_type': self.achievement_type_text,
            'rank': self.rank_text,
            'academic_year': self.academic_year_input.text()
        }
        if self.achievement_type_box.currentText() != "Other":
            match self.achievement_type_text:
                case 'Subject Topper':
                    academic_achievement_details['subject'] = self.subject_text
                    academic_achievement_details['semester'] = self.semester_text
                    academic_achievement_details['year'] = self.year_text
                case 'Semester Topper':
                    academic_achievement_details['subject'] = "Not Relevant"
                    academic_achievement_details['semester'] = self.semester_text
                    academic_achievement_details['year'] = self.year_text
                case 'Year Topper':
                    academic_achievement_details['subject'] = "Not Relevant"
                    academic_achievement_details['semester'] = "Not Relevant"
                    academic_achievement_details['year'] = self.year_text
                case _:
                    academic_achievement_details['subject'] = "Not Relevant"
                    academic_achievement_details['semester'] = "Not Relevant"
                    academic_achievement_details['year'] = "Not Relevant"
        else:
            academic_achievement_details['achievement_type'] = self.other_achievement_input.text()
            academic_achievement_details['rank'] = self.other_achievement_rank.text()
            academic_achievement_details['subject'] = "Not Relevant"
            academic_achievement_details['semester'] = "Not Relevant"
            academic_achievement_details['year'] = "Not Relevant"
        tb_opt.write_academic_achievements_table(self.db_name,
                                                 academic_achievement_details=academic_achievement_details)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.make_academic_achievement_record(academic_achievement_details, filepath,
                                                 mentor_name=f"Mentor - {upg.get_username()}")
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setIcon(QMessageBox.Icon.Information)
        confirmation_widget.setText("The Data was written to Database successfully!\n"
                                    "Achievement Record Document was generated successfully!")
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        message = confirmation_widget.exec()
        if message == QMessageBox.StandardButton.Ok:
            confirmation_widget.close()

    def lor_loa_maker(self):
        if self.LoR_LoA_radio.isChecked():
            self.lor_loa_box.setDisabled(False)
            self.faculty_name_input.setDisabled(False)
            self.lor_loa_reason_input.setDisabled(False)
            self.generate_lor_loa_record_button.setDisabled(False)
        else:
            self.lor_loa_box.setDisabled(True)
            self.faculty_name_input.setDisabled(True)
            self.lor_loa_reason_input.setDisabled(True)
            self.generate_lor_loa_record_button.setDisabled(True)

    def give_letter_type(self):
        self.lor_loa_box.removeItem(2)
        self.letter_type = self.lor_loa_box.currentText()

    def generate_lor_loa_record(self):
        lor_loa_details = {
            'name': self.mentee_name,
            'letter_type': self.letter_type,
            'issuing_faculty': self.faculty_name_input.text(),
            'reason': self.lor_loa_reason_input.text()
        }
        tb_opt.write_lor_loa_table(self.db_name, lor_loa_details=lor_loa_details)
        filepath = QFileDialog.getExistingDirectory(caption='Select Folder to save file')
        doc_gen.make_lor_loa_record(lor_loa_details, filepath, mentor_name=f"Mentor - {upg.get_username()}")
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
