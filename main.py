# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py 
from robot_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Set the size
        self.resize(950, 630)

        # list user
        self.registered_users = [
    {
        "username": "admin",
        "password": "123",
        "fullname": "Admin User",
        "phone": "0123456789",
        "verify": "fablab"
    }
]


        # set moi vô thi hien cai nao 
        self.ui.Page.setCurrentWidget(self.ui.Page_signin)
        self.ui.Dashboard.setCurrentWidget(self.ui.Dashboard_signin)   

        # click sang tab khac thi chuyen trang 
        self.ui.Signin_btn_signup.clicked.connect(lambda: self.ui.Page.setCurrentWidget(self.ui.Page_signup))
        self.ui.Signin_btn_signin.clicked.connect(lambda: self.ui.Page.setCurrentWidget(self.ui.Page_signin))

        self.ui.Signin_btn_login.clicked.connect(self.handle_login)
        self.ui.Signup_btn_signup.clicked.connect(self.handle_signup)

        # click sang tab khac thi chuyen trang 
        self.ui.Main_btn_camera.clicked.connect(lambda: self.ui.Page.setCurrentWidget(self.ui.Page_Camera))
        self.ui.Main_btn_tracking.clicked.connect(lambda: self.ui.Page.setCurrentWidget(self.ui.Page_tracking))
        self.ui.Account__btnlogout.clicked.connect(self.handle_logout)


    def handle_login(self):
        username = self.ui.Signin_username.text()
        password = self.ui.Signin_password.text()

        for user in self.registered_users:
            if user["username"] == username and user["password"] == password:
                self.ui.Page.setCurrentWidget(self.ui.Page_Camera)  # sang giao diện chính
                self.ui.Dashboard.setCurrentWidget(self.ui.Dashboard_main)
                return
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password")
        
        
    def handle_signup(self):
        fullname = self.ui.Signup_name.text()
        phone    = self.ui.Signup_phone.text()
        username = self.ui.Signup_username.text()
        password = self.ui.Signup_password.text()
        verify   = self.ui.Signup_code.text()

        # Kiểm tra có nhập đủ không
        if not all([fullname, phone, username, password, verify]):
            QMessageBox.warning(self, "Sign Up Failed", "Please fill in all fields.")
            return

        # ✅ Kiểm tra mã xác thực
        if verify.strip().lower() != "fablab":
            QMessageBox.warning(self, "Sign Up Failed", "Incorrect verification code.")
            return

        # Kiểm tra trùng username
        for user in self.registered_users:
            if user["username"] == username:
                QMessageBox.warning(self, "Sign Up Failed", "Username already exists.")
                return

        # Lưu lại nếu hợp lệ
        self.registered_users.append({
            "fullname": fullname,
            "phone": phone,
            "username": username,
            "password": password,
            "verify": verify
        })

        QMessageBox.information(self, "Success", "Account created successfully!")
        self.ui.Page.setCurrentWidget(self.ui.Page_signin)

    def handle_logout(self):
        # Tạo hộp thoại
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to log out?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setIcon(QMessageBox.Question)

        # Tự canh giữa cửa sổ cha (vì frameless không làm auto được)
        msg.adjustSize()
        main_rect = self.geometry()
        x = main_rect.x() + (main_rect.width() - msg.width()) // 2
        y = main_rect.y() + (main_rect.height() - msg.height()) // 2
        msg.move(x, y)

        # Hiển thị hộp thoại
        reply = msg.exec()

        if reply == QMessageBox.Yes:
            self.ui.Page.setCurrentWidget(self.ui.Page_signin)
            self.ui.Dashboard.setCurrentWidget(self.ui.Dashboard_signin)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
