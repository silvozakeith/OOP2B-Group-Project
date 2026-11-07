import os
import sys
from PyQt6.QtWidgets import QApplication


from user_screen import UserOrderWindow
from admin_screen import AdminWindow




def main():
    app = QApplication(sys.argv)


    # Apply global stylesheet
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(base_dir, "style.qss")


    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())


    # Instantiate and open both windows side-by-side
    user_window = UserOrderWindow()
    user_window.resize(920, 580)
    user_window.move(80, 100)
    user_window.show()


    admin_window = AdminWindow()
    admin_window.resize(920, 580)
    admin_window.move(1020, 100)
    admin_window.show()


    sys.exit(app.exec())




if __name__ == "__main__":
    main()