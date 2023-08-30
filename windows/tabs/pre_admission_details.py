from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget


class PreAdmissionDetailTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        table_header = ("Name",
                        "10th %", "10th Institute", "10th Board",
                        "12th %", "12th Institute", "12th Board",
                        "CET Score", "JEE Score", "Diploma %")
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table, 0, 0, 1, 3)
        self.setLayout(self.layout)
