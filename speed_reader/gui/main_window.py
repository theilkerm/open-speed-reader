"""
Main window for file selection and reading settings.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QSpinBox, QDoubleSpinBox, QComboBox, QFileDialog, QMessageBox,
    QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..utils.parser import parse_document
from ..utils.state_manager import load_progress
from .reading_window import ReadingWindow


class MainWindow(QWidget):
    """Main application window for file selection and settings."""
    
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.reading_window = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Speed Reader")
        self.setFixedSize(500, 400)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # File selection section
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        # File selection button and label
        file_button_layout = QHBoxLayout()
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.select_file)
        self.file_label = QLabel("No file selected")
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("color: #666; font-style: italic;")
        
        file_button_layout.addWidget(self.select_file_btn)
        file_button_layout.addStretch()
        file_layout.addLayout(file_button_layout)
        file_layout.addWidget(self.file_label)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Reading settings section
        settings_group = QGroupBox("Reading Settings")
        settings_layout = QFormLayout()
        
        # Words Per Minute
        self.wpm_spinbox = QSpinBox()
        self.wpm_spinbox.setRange(100, 1000)
        self.wpm_spinbox.setValue(300)
        self.wpm_spinbox.setSuffix(" WPM")
        settings_layout.addRow("Words Per Minute:", self.wpm_spinbox)
        
        # Font Size
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(24, 200)
        self.font_size_spinbox.setValue(72)
        self.font_size_spinbox.setSuffix(" px")
        settings_layout.addRow("Font Size:", self.font_size_spinbox)
        
        # Paragraph Pause
        self.para_pause_spinbox = QDoubleSpinBox()
        self.para_pause_spinbox.setRange(0.0, 5.0)
        self.para_pause_spinbox.setValue(1.0)
        self.para_pause_spinbox.setSingleStep(0.1)
        self.para_pause_spinbox.setSuffix(" sec")
        settings_layout.addRow("Paragraph Pause:", self.para_pause_spinbox)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText("Light")
        settings_layout.addRow("Theme:", self.theme_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Start reading button
        self.start_reading_btn = QPushButton("Start Reading")
        self.start_reading_btn.setEnabled(False)
        self.start_reading_btn.clicked.connect(self.start_reading)
        self.start_reading_btn.setMinimumHeight(40)
        self.start_reading_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
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
        
        self.setLayout(layout)
        
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
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
    
    def select_file(self):
        """Open file dialog to select a PDF or EPUB file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document",
            "",
            "Supported Files (*.pdf *.epub);;PDF Files (*.pdf);;EPUB Files (*.epub);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            # Display just the filename, not the full path
            filename = os.path.basename(file_path)
            self.file_label.setText(f"Selected: {filename}")
            self.file_label.setStyleSheet("color: #333; font-style: normal;")
            self.start_reading_btn.setEnabled(True)
    
    def start_reading(self):
        """Start the reading session with the selected file and settings."""
        if not self.selected_file:
            QMessageBox.warning(self, "No File Selected", "Please select a file first.")
            return
        
        try:
            # Parse the document
            word_list, total_word_count = parse_document(self.selected_file)
            
            if not word_list:
                QMessageBox.warning(self, "No Text Found", "No readable text was found in the selected file.")
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
            
            # Hide main window and show reading window
            self.hide()
            self.reading_window.show()
            
            # Start reading automatically
            self.reading_window.start_reading()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to open the document:\n{str(e)}"
            )
    
    def closeEvent(self, event):
        """Handle window close event."""
        # If reading window is open, close it first
        if self.reading_window and not self.reading_window.isHidden():
            self.reading_window.close()
        event.accept()
