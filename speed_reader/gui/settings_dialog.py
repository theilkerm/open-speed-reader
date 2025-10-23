"""
Settings dialog for changing reading parameters during reading.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout,
    QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox, QLabel
)
from PyQt6.QtCore import Qt

from ..utils.language_manager import language_manager


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
        self.setWindowTitle(language_manager.get_text("settings_title"))
        self.setFixedSize(350, 300)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Settings group
        self.settings_group = QGroupBox()
        settings_layout = QFormLayout()
        
        # Words Per Minute
        self.wpm_spinbox = QSpinBox()
        self.wpm_spinbox.setRange(100, 1000)
        self.wpm_spinbox.setSuffix(language_manager.get_text("wpm_suffix"))
        self.wpm_label = QLabel()
        settings_layout.addRow(self.wpm_label, self.wpm_spinbox)
        
        # Font Size
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(24, 200)
        self.font_size_spinbox.setSuffix(language_manager.get_text("px_suffix"))
        self.font_size_label = QLabel()
        settings_layout.addRow(self.font_size_label, self.font_size_spinbox)
        
        # Paragraph Pause
        self.para_pause_spinbox = QDoubleSpinBox()
        self.para_pause_spinbox.setRange(0.0, 5.0)
        self.para_pause_spinbox.setSingleStep(0.1)
        self.para_pause_spinbox.setSuffix(language_manager.get_text("sec_suffix"))
        self.para_pause_label = QLabel()
        settings_layout.addRow(self.para_pause_label, self.para_pause_spinbox)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([language_manager.get_text("light"), language_manager.get_text("dark")])
        self.theme_label = QLabel()
        settings_layout.addRow(self.theme_label, self.theme_combo)
        
        self.settings_group.setLayout(settings_layout)
        layout.addWidget(self.settings_group)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.ok_btn = QPushButton()
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)
        
        self.cancel_btn = QPushButton()
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Update UI text
        self.update_ui_text()
        
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
    
    def update_ui_text(self):
        """Update all UI text based on current language."""
        # Update window title
        self.setWindowTitle(language_manager.get_text("settings_title"))
        
        # Update group box title
        self.settings_group.setTitle(language_manager.get_text("reading_settings"))
        
        # Update labels
        self.wpm_label.setText(language_manager.get_text("words_per_minute") + ":")
        self.font_size_label.setText(language_manager.get_text("font_size") + ":")
        self.para_pause_label.setText(language_manager.get_text("paragraph_pause") + ":")
        self.theme_label.setText(language_manager.get_text("theme") + ":")
        
        # Update button texts
        self.ok_btn.setText(language_manager.get_text("ok"))
        self.cancel_btn.setText(language_manager.get_text("cancel"))
        
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
    
    def set_initial_values(self):
        """Set the initial values from current settings."""
        self.wpm_spinbox.setValue(self.current_settings.get('wpm', 300))
        self.font_size_spinbox.setValue(self.current_settings.get('font_size', 72))
        self.para_pause_spinbox.setValue(self.current_settings.get('para_delay', 1.0))
        
        theme = self.current_settings.get('theme', 'light')
        if theme == 'light':
            self.theme_combo.setCurrentText(language_manager.get_text("light"))
        else:
            self.theme_combo.setCurrentText(language_manager.get_text("dark"))
    
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
