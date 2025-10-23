"""
Main window for file selection and reading settings.
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QSpinBox, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox,
    QGroupBox, QFormLayout, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction

from ..utils.parser import parse_document
from ..utils.state_manager import load_progress, StateManager
from ..utils.language_manager import language_manager
from .reading_window import ReadingWindow
from .about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Main application window for file selection and settings."""
    
    # Signal emitted when language changes
    language_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.reading_window = None
        self.state_manager = StateManager()
        self.init_ui()
        self.load_recent_files()
        self.update_ui_text()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(language_manager.get_text("app_title"))
        self.setFixedSize(700, 650)
        
        # Create menu bar first
        self.create_menu_bar()
        self.setMenuBar(self.menu_bar)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # File selection section
        self.file_group = QGroupBox()
        file_layout = QVBoxLayout()
        file_layout.setSpacing(15)
        
        # File selection button and label
        file_button_layout = QHBoxLayout()
        self.select_file_btn = QPushButton()
        self.select_file_btn.clicked.connect(self.select_file)
        self.select_file_btn.setMinimumHeight(40)
        self.select_file_btn.setMinimumWidth(120)
        self.file_label = QLabel()
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("color: #666; font-style: italic; padding: 5px; font-size: 14px;")
        self.file_label.setMinimumHeight(30)
        
        file_button_layout.addWidget(self.select_file_btn)
        file_button_layout.addStretch()
        file_layout.addLayout(file_button_layout)
        file_layout.addWidget(self.file_label)
        
        self.file_group.setLayout(file_layout)
        layout.addWidget(self.file_group)
        
        # Reading settings section
        self.settings_group = QGroupBox()
        settings_layout = QFormLayout()
        settings_layout.setSpacing(15)
        settings_layout.setVerticalSpacing(15)
        settings_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Words Per Minute
        self.wpm_spinbox = QSpinBox()
        self.wpm_spinbox.setRange(100, 1000)
        self.wpm_spinbox.setValue(300)
        self.wpm_spinbox.setSuffix(language_manager.get_text("wpm_suffix"))
        self.wpm_spinbox.setMinimumHeight(45)
        self.wpm_spinbox.setMaximumHeight(45)
        self.wpm_spinbox.setMinimumWidth(150)
        self.wpm_label = QLabel()
        self.wpm_label.setMinimumWidth(200)
        settings_layout.addRow(self.wpm_label, self.wpm_spinbox)
        
        # Font Size
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(24, 200)
        self.font_size_spinbox.setValue(72)
        self.font_size_spinbox.setSuffix(language_manager.get_text("px_suffix"))
        self.font_size_spinbox.setMinimumHeight(45)
        self.font_size_spinbox.setMaximumHeight(45)
        self.font_size_spinbox.setMinimumWidth(150)
        self.font_size_label = QLabel()
        self.font_size_label.setMinimumWidth(200)
        settings_layout.addRow(self.font_size_label, self.font_size_spinbox)
        
        # Paragraph Pause
        self.para_pause_spinbox = QDoubleSpinBox()
        self.para_pause_spinbox.setRange(0.0, 5.0)
        self.para_pause_spinbox.setValue(1.0)
        self.para_pause_spinbox.setSingleStep(0.1)
        self.para_pause_spinbox.setSuffix(language_manager.get_text("sec_suffix"))
        self.para_pause_spinbox.setMinimumHeight(45)
        self.para_pause_spinbox.setMaximumHeight(45)
        self.para_pause_spinbox.setMinimumWidth(150)
        self.para_pause_label = QLabel()
        self.para_pause_label.setMinimumWidth(200)
        settings_layout.addRow(self.para_pause_label, self.para_pause_spinbox)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([language_manager.get_text("light"), language_manager.get_text("dark")])
        self.theme_combo.setCurrentText(language_manager.get_text("light"))
        self.theme_combo.setMinimumHeight(45)
        self.theme_combo.setMaximumHeight(45)
        self.theme_combo.setMinimumWidth(150)
        self.theme_label = QLabel()
        self.theme_label.setMinimumWidth(200)
        settings_layout.addRow(self.theme_label, self.theme_combo)
        
        self.settings_group.setLayout(settings_layout)
        layout.addWidget(self.settings_group)
        
        # Recent files section
        self.recent_group = QGroupBox()
        recent_layout = QVBoxLayout()
        recent_layout.setSpacing(10)
        
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(120)
        self.recent_list.setMinimumHeight(80)
        self.recent_list.itemClicked.connect(self.on_recent_file_selected)
        self.recent_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        recent_layout.addWidget(self.recent_list)
        
        self.recent_group.setLayout(recent_layout)
        layout.addWidget(self.recent_group)
        
        # Start reading button
        self.start_reading_btn = QPushButton()
        self.start_reading_btn.setEnabled(False)
        self.start_reading_btn.clicked.connect(self.start_reading)
        self.start_reading_btn.setMinimumHeight(50)
        self.start_reading_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        layout.addWidget(self.start_reading_btn)
        layout.addStretch()
        
        central_widget.setLayout(layout)
        
        # Apply window styling
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 10px 15px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 14px;
                min-height: 25px;
                line-height: 1.2;
            }
            QLabel {
                padding: 5px 0px;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #f0f0f0;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                color: #000000;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-bottom: 2px solid #007acc;
                font-weight: bold;
                font-size: 14px;
            }
            QMenuBar::item {
                padding: 8px 12px;
                background-color: transparent;
                color: #ffffff;
                border-radius: 3px;
                margin: 2px;
            }
            QMenuBar::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            QMenuBar::item:pressed {
                background-color: #005a9e;
                color: #ffffff;
            }
            QMenu {
                background-color: #ffffff;
                border: 2px solid #007acc;
                border-radius: 5px;
                color: #000000;
                font-size: 14px;
            }
            QMenu::item {
                padding: 8px 20px;
                color: #000000;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #007acc;
                color: #ffffff;
            }
            QMenu::separator {
                height: 1px;
                background-color: #cccccc;
                margin: 4px 0px;
            }
        """)
    
    def create_menu_bar(self):
        """Create the menu bar with Help and Language menus."""
        self.menu_bar = QMenuBar()
        
        # File menu
        file_menu = self.menu_bar.addMenu(language_manager.get_text("file_menu"))
        
        # Exit action
        exit_action = QAction(language_manager.get_text("exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = self.menu_bar.addMenu(language_manager.get_text("help_menu"))
        
        # About action
        about_action = QAction(language_manager.get_text("about"), self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        # Language menu
        language_menu = self.menu_bar.addMenu(language_manager.get_text("language_menu"))
        
        # Language actions
        self.english_action = QAction(language_manager.get_text("english"), self)
        self.english_action.setCheckable(True)
        self.english_action.triggered.connect(lambda: self.change_language("en"))
        language_menu.addAction(self.english_action)
        
        self.turkish_action = QAction(language_manager.get_text("turkish"), self)
        self.turkish_action.setCheckable(True)
        self.turkish_action.triggered.connect(lambda: self.change_language("tr"))
        language_menu.addAction(self.turkish_action)
        
        # Set current language as checked
        if language_manager.get_current_language() == "en":
            self.english_action.setChecked(True)
        else:
            self.turkish_action.setChecked(True)
    
    def update_ui_text(self):
        """Update all UI text based on current language."""
        # Update window title
        self.setWindowTitle(language_manager.get_text("app_title"))
        
        # Update group box titles
        self.file_group.setTitle(language_manager.get_text("file_selection"))
        self.settings_group.setTitle(language_manager.get_text("reading_settings"))
        self.recent_group.setTitle(language_manager.get_text("recent_readings"))
        
        # Update button and label texts
        self.select_file_btn.setText(language_manager.get_text("select_file"))
        self.file_label.setText(language_manager.get_text("no_file_selected"))
        self.start_reading_btn.setText(language_manager.get_text("start_reading"))
        
        # Update form labels
        self.wpm_label.setText(language_manager.get_text("words_per_minute") + ":")
        self.font_size_label.setText(language_manager.get_text("font_size") + ":")
        self.para_pause_label.setText(language_manager.get_text("paragraph_pause") + ":")
        self.theme_label.setText(language_manager.get_text("theme") + ":")
        
        # Update spinbox suffixes
        self.wpm_spinbox.setSuffix(language_manager.get_text("wpm_suffix"))
        self.font_size_spinbox.setSuffix(language_manager.get_text("px_suffix"))
        self.para_pause_spinbox.setSuffix(language_manager.get_text("sec_suffix"))
        
        # Update theme combo items
        current_theme = self.theme_combo.currentText()
        self.theme_combo.clear()
        self.theme_combo.addItems([language_manager.get_text("light"), language_manager.get_text("dark")])
        
        # Restore theme selection
        if current_theme == language_manager.get_text("light") or current_theme == "Light":
            self.theme_combo.setCurrentText(language_manager.get_text("light"))
        else:
            self.theme_combo.setCurrentText(language_manager.get_text("dark"))
        
        # Update menu bar
        self.menu_bar.clear()
        self.create_menu_bar()
        self.setMenuBar(self.menu_bar)
    
    def change_language(self, language_code):
        """Change the application language."""
        language_manager.set_language(language_code)
        
        # Update check states
        self.english_action.setChecked(language_code == "en")
        self.turkish_action.setChecked(language_code == "tr")
        
        # Update UI text
        self.update_ui_text()
        
        # Emit signal for other windows to update
        self.language_changed.emit()
    
    def show_about_dialog(self):
        """Show the about dialog."""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def select_file(self):
        """Open file dialog to select a PDF or EPUB file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            language_manager.get_text("select_file"),
            "",
            "Supported Files (*.pdf *.epub);;PDF Files (*.pdf);;EPUB Files (*.epub);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            # Display just the filename, not the full path
            filename = os.path.basename(file_path)
            self.file_label.setText(f"{language_manager.get_text('selected')}: {filename}")
            self.file_label.setStyleSheet("color: #333; font-style: normal;")
            self.start_reading_btn.setEnabled(True)
            self.load_recent_files()  # Refresh recent files list
    
    def start_reading(self):
        """Start the reading session with the selected file and settings."""
        if not self.selected_file:
            QMessageBox.warning(self, language_manager.get_text("error"), language_manager.get_text("no_file_selected_msg"))
            return
        
        try:
            # Parse the document
            word_list, total_word_count = parse_document(self.selected_file)
            
            if not word_list:
                QMessageBox.warning(self, language_manager.get_text("error"), language_manager.get_text("no_text_found"))
                return
            
            # Load saved progress
            start_index = load_progress(self.selected_file)
            
            # Get settings
            settings = {
                'wpm': self.wpm_spinbox.value(),
                'font_size': self.font_size_spinbox.value(),
                'para_delay': self.para_pause_spinbox.value(),
                'theme': self.theme_combo.currentText().lower()
            }
            
            # Create and show reading window
            self.reading_window = ReadingWindow(
                word_list=word_list,
                total_word_count=total_word_count,
                start_index=start_index,
                file_path=self.selected_file,
                settings=settings
            )
            
            # Connect the closed signal to show main window
            self.reading_window.closed.connect(self.show_main_window)
            
            # Connect language change signal
            self.language_changed.connect(self.reading_window.update_ui_text)
            
            # Hide main window and show reading window
            self.hide()
            self.reading_window.show()
            
            # Start reading automatically
            self.reading_window.start_reading()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                language_manager.get_text("error"), 
                f"{language_manager.get_text('failed_to_open')}\n{str(e)}"
            )
    
    def show_main_window(self):
        """Show the main window when returning from reading."""
        self.show()
        self.raise_()
        self.activateWindow()
        self.load_recent_files()  # Refresh recent files when returning
    
    def load_recent_files(self):
        """Load and display recent files."""
        self.recent_list.clear()
        recent_files = self.state_manager.get_recent_files(5)
        
        for file_path, word_index, total_words in recent_files:
            filename = os.path.basename(file_path)
            item_text = f"{filename} (Word {word_index + 1})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.recent_list.addItem(item)
    
    def on_recent_file_selected(self, item):
        """Handle selection of a recent file."""
        try:
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path and os.path.exists(file_path):
                self.selected_file = file_path
                filename = os.path.basename(file_path)
                self.file_label.setText(f"{language_manager.get_text('selected')}: {filename}")
                self.file_label.setStyleSheet("color: #333; font-style: normal;")
                self.start_reading_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(
                self, 
                language_manager.get_text("error"), 
                f"{language_manager.get_text('failed_to_select')}\n{str(e)}"
            )
    
    def closeEvent(self, event):
        """Handle window close event."""
        # If reading window is open, close it first
        if self.reading_window and not self.reading_window.isHidden():
            self.reading_window.close()
        event.accept()
