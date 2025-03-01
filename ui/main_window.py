from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

# Import pages
from ui.pages.scan_history import ScanHistoryPage
from ui.pages.summary import SummaryPage
from ui.pages.top_threats import TopThreatsPage
from ui.pages.system_health import SystemHealthPage
from ui.pages.graph import GraphPage
from ui.pages.settings import SettingsPage
from ui.pages.about import AboutPage
from ui.pages.dashboard import DashboardPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fytra Antivirus")
        self.setWindowIcon(QIcon("ui/logos/app_logo.png"))
        self.resize(1200, 700)
        self.setStyleSheet("background-color: #091e36; color: white;")

        self.active_button = None  # Track the currently active button

        # Main Layout
        main_layout = QVBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(
            "background-color: rgb(42, 87, 111);"
            "border-top-left-radius: 20px;"
            "border-bottom-left-radius: 20px;"
            "padding: 20px 0px;"
        )
        sidebar_layout = QVBoxLayout()

        # Sidebar Header (Logo + App Name)
        logo_name_layout = QHBoxLayout()
        logo_name_layout.setSpacing(10)  # Space between logo and label
        logo_name_layout.setContentsMargins(10, 0, 10, 0)  # Tight margins

        # App Logo
        app_logo = QLabel()
        app_logo.setPixmap(QPixmap("ui/logos/app_logo.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        app_logo.setAlignment(Qt.AlignCenter)  # Center the logo vertically and horizontally

        # App Name
        app_name = QLabel("Fytra Antivirus")
        app_name.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        app_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align text to the left and center vertically

        # Add widgets to the layout
        logo_name_layout.addWidget(app_logo)
        logo_name_layout.addWidget(app_name)
        logo_name_layout.addStretch()  # Push content to the left

        # Add the header layout to the sidebar
        sidebar_layout.addLayout(logo_name_layout)

        # Create QStackedWidget for pages
        self.stacked_widget = QStackedWidget()
        self.pages = {
            "Dashboard": DashboardPage(self),
            "Scan History": ScanHistoryPage(),
            "Summary": SummaryPage(),
            "Top Threats": TopThreatsPage(),
            "System Health": SystemHealthPage(),
            "Graph": GraphPage(),
            "Settings": SettingsPage(),
            "About": AboutPage(),
        }

        for name, page in self.pages.items():
            self.stacked_widget.addWidget(page)

        # Sidebar Buttons
        self.page_buttons = {}
        for label in self.pages.keys():
            button = QPushButton(label)
            button.setStyleSheet(self.sidebar_button_style())
            button.clicked.connect(lambda _, name=label: self.set_active_page(name, self.page_buttons[name]))
            self.page_buttons[label] = button
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        # "Add Files to Scan" Button
        add_files_button = QPushButton(" Add Files \n to Scan \n +")
        add_files_button.setStyleSheet(self.add_files_button_style())
        add_files_button.setFixedSize(110, 150)
        sidebar_layout.addWidget(add_files_button, alignment=Qt.AlignCenter)

        sidebar.setLayout(sidebar_layout)

        # Main Content Area
        content_border = QFrame()
        content_border.setStyleSheet(
            "background-color: #1d2e4a; "
            "border-top-right-radius: 20px; "
            "border-bottom-right-radius: 20px;"
        )
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.stacked_widget)
        content_border.setLayout(content_layout)

        # Combine Sidebar and Main Content
        top_layout = QHBoxLayout()
        top_layout.addWidget(sidebar)
        top_layout.addWidget(content_border)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addLayout(top_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Set Default Active Page
        self.set_active_page("Dashboard", self.page_buttons["Dashboard"])

    def set_active_page(self, page_name, button):
        """Sets the active page and updates the button styling."""
        if self.active_button:
            self.active_button.setStyleSheet(self.sidebar_button_style())
        self.active_button = button
        self.active_button.setStyleSheet(self.active_button_style())
        self.stacked_widget.setCurrentWidget(self.pages[page_name])

    def active_button_style(self):
        return (
            "QPushButton {"
            "    background-color: #1d2e4a;"
            "    color: white;"
            "    font-size: 18px;"
            "    padding: 10px 25px;"
            "    text-align: left;"
            "    border: none;"
            "} "
            "QPushButton:hover {"
            "    background-color: #4A5B6E;"
            "} "
        )

    def sidebar_button_style(self):
        return (
            "QPushButton {"
            "    background-color: transparent;"
            "    color: white;"
            "    font-size: 18px;"
            "    padding: 10px 25px;"
            "    text-align: left;"
            "    border: none;"
            "} "
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "} "
        )

    def add_files_button_style(self):
        return (
            "QPushButton {"
            "    border: 2px dashed #888;"
            "    border-radius: 20px;"
            "    background-color: #2E3A48;"
            "    color: white;"
            "    font-size: 16px;"
            "    text-align: center;"
            "    padding: 10px;"
            "} "
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "} "
        )