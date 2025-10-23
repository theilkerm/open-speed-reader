"""
Settings dialog for changing reading parameters during reading.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout,
    QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt


class SettingsDialog(QDialog):
    """Dialog for adjusting reading settings during reading."""
    
    def __init__(self, current_settings, parent=None):
        """
        Initialize the settings dialog.
        
        Args:
            current_settings: Dictionary with current settings values
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_settings = current_settings
        self.init_ui()
        self.set_initial_values()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Reading Settings")
        self.setFixedSize(350, 300)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Settings group
        settings_group = QGroupBox("Reading Settings")
        settings_layout = QFormLayout()
        
        # Words Per Minute
        self.wpm_spinbox = QSpinBox()
        self.wpm_spinbox.setRange(100, 1000)
        self.wpm_spinbox.setSuffix(" WPM")
        settings_layout.addRow("Words Per Minute:", self.wpm_spinbox)
        
        # Font Size
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(24, 200)
        self.font_size_spinbox.setSuffix(" px")
        settings_layout.addRow("Font Size:", self.font_size_spinbox)
        
        # Paragraph Pause
        self.para_pause_spinbox = QDoubleSpinBox()
        self.para_pause_spinbox.setRange(0.0, 5.0)
        self.para_pause_spinbox.setSingleStep(0.1)
        self.para_pause_spinbox.setSuffix(" sec")
        settings_layout.addRow("Paragraph Pause:", self.para_pause_spinbox)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        settings_layout.addRow("Theme:", self.theme_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Apply styling
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
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:default {
                background-color: #007acc;
                color: white;
                border: 1px solid #007acc;
            }
            QPushButton:default:hover {
                background-color: #005a9e;
            }
        """)
    
    def set_initial_values(self):
        """Set the initial values from current settings."""
        self.wpm_spinbox.setValue(self.current_settings.get('wpm', 300))
        self.font_size_spinbox.setValue(self.current_settings.get('font_size', 72))
        self.para_pause_spinbox.setValue(self.current_settings.get('para_delay', 1.0))
        
        theme = self.current_settings.get('theme', 'light')
        theme_text = theme.capitalize()
        if theme_text in ["Light", "Dark"]:
            self.theme_combo.setCurrentText(theme_text)
        else:
            self.theme_combo.setCurrentText("Light")
    
    def get_settings(self):
        """
        Get the current settings from the dialog controls.
        
        Returns:
            Dictionary with the current settings values
        """
        return {
            'wpm': self.wpm_spinbox.value(),
            'font_size': self.font_size_spinbox.value(),
            'para_delay': self.para_pause_spinbox.value(),
            'theme': self.theme_combo.currentText().lower()
        }
