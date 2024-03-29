from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget


class PersonalDetailTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        sizes = (100, 100, 100, 600, 600, 100, 200, 200, 200, 200, 200, 200, 200, 200, 200)
        for column, size in zip(columns, sizes):
            self.table.setColumnWidth(column, size)
        table_header = ("Name",
                        "Date of Birth", "Place of Birth",
                        "Residential Address", "Correspondent Address", "Blood Group",
                        "Mother's Name", "Mother's Phone No", "Mother's Email Id",
                        "Father's Name", "Father's Phone Number", "Father's Email Id",
                        "Guardian's Name", "Guardian's Phone No", "Guardian's Email Id")
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table, 0, 0, 1, 3)
        self.setLayout(layout)
