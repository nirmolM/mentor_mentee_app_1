from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget


class OutcomeDetailTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        table_header = ("Name",
                        "Placement Status", "Higher Studies Status", "Entrepreneurship Status")
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table, 0, 0, 1, 3)
        self.setLayout(self.layout)
