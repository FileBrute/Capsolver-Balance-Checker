import sys
import requests
import json
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QTabWidget, QTextBrowser, QSplitter, QFrame, QCheckBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer


class CapsolverBalanceChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capsolver Balance Checker")
        self.setGeometry(100, 100, 800, 400)  # Increased the window size

        # Initialize timer for automatic balance updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_check_balance)
        self.auto_update_enabled = False  # Flag to control automatic updates

        logo = QIcon("logo.png")
        self.setWindowIcon(logo)


        self.init_ui()

    def init_ui(self):
        # Apply a modern style sheet
        self.setStyleSheet("""
            QWidget {
                background-color: #222;
                font-family: Arial, sans-serif;
                color: #FFFFFF;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                color: #FFFFFF;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005AA1;
            }
            QTextEdit {
                padding: 10px;
                font-size: 14px;
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #0078D4;
                border: 1px solid #555;
                padding: 5px 10px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 14px;
                color: white;
            }
            QTabBar::tab:last {
                margin-right: 0;
            }
            QTabBar::tab:selected {
                background-color: #005AA1;
            }
        """)

        # Create a horizontal splitter
        splitter = QSplitter(Qt.Horizontal)

        # Create the "Check Balance" side
        check_balance_side = QWidget()
        self.create_check_balance_side(check_balance_side)

        # Create the tabbed sidebar
        sidebar_side = QWidget()
        self.create_sidebar(sidebar_side)

        # Add the "Check Balance" side and sidebar to the splitter
        splitter.addWidget(check_balance_side)
        splitter.addWidget(sidebar_side)

        # Set the splitter's sizes
        splitter.setSizes([300, 500])

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

    def create_check_balance_side(self, check_balance_side):
        layout = QVBoxLayout()

        self.api_key_label = QLabel("Enter your CapSolver API key:")
        self.api_key_entry = QLineEdit()
        self.check_balance_button = QPushButton("Check Balance")

        # Create a QTextBrowser for displaying responses
        self.response_browser = QTextBrowser()
        self.response_browser.setFont(QFont("Arial", 12))
        self.response_browser.setReadOnly(True)

        # Create a checkbox for auto-check balance
        self.auto_check_box = QCheckBox("Auto Check Balance")
        self.auto_check_box.stateChanged.connect(self.toggle_auto_check_balance)

        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_entry)
        layout.addWidget(self.check_balance_button)
        layout.addWidget(self.auto_check_box)
        layout.addWidget(self.response_browser)

        check_balance_side.setLayout(layout)

        self.check_balance_button.clicked.connect(self.check_balance)

    def create_sidebar(self, sidebar_side):
        layout = QVBoxLayout()

        # Create a tab widget for the sidebar
        self.sidebar_tab_widget = QTabWidget()
        self.sidebar_tab_widget.setFont(QFont("Arial", 14))

        # Add tabs for getState, createTask, and getTaskResult
        self.add_get_state_tab()
        self.add_create_task_tab()
        self.add_get_task_result_tab()

        layout.addWidget(self.sidebar_tab_widget)

        sidebar_side.setLayout(layout)

    def add_get_state_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        get_state_button = QPushButton("Get State")
        get_state_button.clicked.connect(self.get_state)

        self.state_response_browser = QTextBrowser()
        self.state_response_browser.setFont(QFont("Arial", 12))
        self.state_response_browser.setReadOnly(True)

        layout.addWidget(get_state_button)
        layout.addWidget(self.state_response_browser)
        tab.setLayout(layout)

        self.sidebar_tab_widget.addTab(tab, "Get State")

    def add_create_task_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.app_id_label = QLabel("App ID:")
        self.app_id_entry = QLineEdit()

        self.image_label = QLabel("Base64 Image:")
        self.image_entry = QTextEdit()

        create_task_button = QPushButton("Create Task")
        create_task_button.clicked.connect(self.create_task)

        self.create_response_browser = QTextBrowser()
        self.create_response_browser.setFont(QFont("Arial", 12))
        self.create_response_browser.setReadOnly(True)

        layout.addWidget(self.app_id_label)
        layout.addWidget(self.app_id_entry)
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_entry)
        layout.addWidget(create_task_button)
        layout.addWidget(self.create_response_browser)
        tab.setLayout(layout)

        self.sidebar_tab_widget.addTab(tab, "Create Task")

    def add_get_task_result_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.task_id_label = QLabel("Task ID:")
        self.task_id_entry = QLineEdit()

        get_task_result_button = QPushButton("Get Task Result")
        get_task_result_button.clicked.connect(self.get_task_result)

        self.task_result_response_browser = QTextBrowser()
        self.task_result_response_browser.setFont(QFont("Arial", 12))
        self.task_result_response_browser.setReadOnly(True)

        layout.addWidget(self.task_id_label)
        layout.addWidget(self.task_id_entry)
        layout.addWidget(get_task_result_button)
        layout.addWidget(self.task_result_response_browser)
        tab.setLayout(layout)

        self.sidebar_tab_widget.addTab(tab, "Get Task Result")

    def append_to_log(self, text, log_browser):
        current_text = log_browser.toPlainText()
        log_browser.setPlainText(current_text + text + '\n')
        log_browser.verticalScrollBar().setValue(log_browser.verticalScrollBar().maximum())

    def clear_log(self, log_browser):
        log_browser.clear()

    def check_balance(self):
        api_key = self.api_key_entry.text()
        self.clear_log(self.response_browser)
        self.append_to_log("📝 Checking balance...", self.response_browser)

        # Implement the check_balance action here
        balance = self.check_capsolver_balance(api_key)

        if balance == "Invalid Key":
            self.append_to_log("📝 Invalid API Key", self.response_browser)
        elif balance == "Error:":
            self.append_to_log("📝 An error occurred while checking the balance.", self.response_browser)
        elif balance == 0:
            self.append_to_log("📝 Balance is 0. Exiting...", self.response_browser)

    def auto_check_balance(self):
        if self.auto_check_box.isChecked():
            api_key = self.api_key_entry.text()
            self.clear_log(self.response_browser)
            self.append_to_log("📝 Automatically checking balance...", self.response_browser)

            # Implement the auto_check_balance action here
            balance = self.check_capsolver_balance(api_key)
            if balance:
                self.append_to_log(f"📝 Balance: {balance}", self.response_browser)

    def toggle_auto_check_balance(self):
        if self.auto_check_box.isChecked():
            self.timer.start(10000)  # Update every 10 seconds
        else:
            self.timer.stop()

    def get_state(self):
        api_key = self.api_key_entry.text()
        self.clear_log(self.state_response_browser)
        self.append_to_log("📝 Getting state...", self.state_response_browser)

        # Implement the get_state action here
        state = self.get_capsolver_state(api_key)

        if state == "Invalid Key":
            self.append_to_log("📝 Invalid API Key", self.state_response_browser)
        elif state == "Error:":
            self.append_to_log("📝 An error occurred while getting the state.", self.state_response_browser)
        else:
            self.append_to_log(f"📝 Capsolver State: {state}", self.state_response_browser)

    def create_task(self):
        api_key = self.api_key_entry.text()
        app_id = self.app_id_entry.text()
        image = self.image_entry.toPlainText()
        self.clear_log(self.create_response_browser)
        self.append_to_log("📝 Creating task...", self.create_response_browser)

        # Implement the create_task action here
        task_result = self.create_capsolver_task(api_key, app_id, image)

        if task_result == "Invalid Key":
            self.append_to_log("📝 Invalid API Key", self.create_response_browser)
        elif task_result == "Error:":
            self.append_to_log("📝 An error occurred while creating the task.", self.create_response_browser)
        else:
            self.append_to_log(f"📝 Task Created - Task ID: {task_result}", self.create_response_browser)

    def get_task_result(self):
        api_key = self.api_key_entry.text()
        task_id = self.task_id_entry.text()
        self.clear_log(self.task_result_response_browser)
        self.append_to_log("📝 Getting task result...", self.task_result_response_browser)

        # Implement the get_task_result action here
        task_result = self.get_capsolver_task_result(api_key, task_id)

        if task_result == "Invalid Key":
            self.append_to_log("📝 Invalid API Key", self.task_result_response_browser)
        elif task_result == "Error:":
            self.append_to_log("📝 An error occurred while getting the task result.", self.task_result_response_browser)
        else:
            self.append_to_log(f"📝 Task Result: {task_result}", self.task_result_response_browser)

    def check_capsolver_balance(self, api_key):
        # Define the endpoint URL
        endpoint_url = "https://api.capsolver.com/getBalance"

        # Set headers and data
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "clientKey": api_key,
        }

        try:
            # Make the API request
            response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))
            response_json = response.json()

            if response.status_code == 200:
                return response_json.get('balance', 0)
            elif 'ERROR_KEY_DOES_NOT_EXIST' in response_json.get('errorDescription', ''):
                return "Invalid Key"
            else:
                error_message = f"📝 Error: Invalid Key (or no balance) - {api_key}"
                self.append_to_log(error_message, self.response_browser)
                return error_message
        except Exception as e:
            error_message = f"📝 Error: An error occurred while checking the balance. {str(e)}"
            self.append_to_log(error_message, self.response_browser)
            return error_message

    def get_capsolver_state(self, api_key):
        # Define the endpoint URL
        endpoint_url = "https://api.capsolver.com/getBalance"

        # Set headers and data
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "clientKey": api_key,
        }

        try:
            # Make the API request
            response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))
            response_json = response.json()

            if response.status_code == 200:
                return response_json.get('state', 'Unknown')
            elif 'ERROR_KEY_DOES_NOT_EXIST' in response_json.get('errorDescription', ''):
                return "Invalid Key"
            else:
                error_message = f"📝 Error: Invalid Key - {api_key}"
                self.append_to_log(error_message, self.state_response_browser)
                return error_message
        except Exception as e:
            error_message = f"📝 Error: An error occurred while getting the state. {str(e)}"
            self.append_to_log(error_message, self.state_response_browser)
            return error_message

    def create_capsolver_task(self, api_key, app_id, image):
        # Define the endpoint URL
        endpoint_url = "https://api.capsolver.com/createTask"

        # Set headers and data
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "clientKey": api_key,
            "appId": app_id,
            "task": {
                "type": "ImageToTextTask",
                "body": image,
            }
        }

        try:
            # Make the API request
            response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))
            response_json = response.json()

            if response.status_code == 200:
                return response_json.get('taskId', 'Unknown')
            elif 'ERROR_KEY_DOES_NOT_EXIST' in response_json.get('errorDescription', ''):
                return "Invalid Key"
            else:
                error_message = f"📝 Error: Invalid Key (or failed to create task) - {api_key}"
                self.append_to_log(error_message, self.create_response_browser)
                return error_message
        except Exception as e:
            error_message = f"📝 Error: An error occurred while creating the task. {str(e)}"
            self.append_to_log(error_message, self.create_response_browser)
            return error_message

    def get_capsolver_task_result(self, api_key, task_id):
        # Define the endpoint URL
        endpoint_url = "https://api.capsolver.com/getTaskResult"

        # Set headers and data
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "clientKey": api_key,
            "taskId": task_id,
        }

        try:
            # Make the API request
            response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))
            response_json = response.json()

            if response.status_code == 200:
                return response_json.get('result', 'Unknown')
            elif 'ERROR_KEY_DOES_NOT_EXIST' in response_json.get('errorDescription', ''):
                return "Invalid Key"
            else:
                error_message = f"📝 Error: Invalid Key (or failed to get task result) - {api_key}"
                self.append_to_log(error_message, self.task_result_response_browser)
                return error_message
        except Exception as e:
            error_message = f"📝 Error: An error occurred while getting the task result. {str(e)}"
            self.append_to_log(error_message, self.task_result_response_browser)
            return error_message

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CapsolverBalanceChecker()
    window.show()
    sys.exit(app.exec_())