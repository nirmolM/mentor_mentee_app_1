# todo -> Implement outlook email functionality
# todo -> Implement college co-curricular activities (Internships, Courses, Copyrights) - Link with Mentee Action Plan
import sys
from PyQt6.QtWidgets import QApplication
import windows.login_window
app = QApplication(sys.argv)
main_window = windows.login_window.MainWindow()
main_window.show()
sys.exit(app.exec())
