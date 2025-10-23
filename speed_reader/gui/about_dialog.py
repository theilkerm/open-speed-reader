"""
About dialog showing application information and README content.
"""

import os
import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTextEdit, QScrollArea, QWidget, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ..utils.language_manager import language_manager


class AboutDialog(QDialog):
    """Dialog showing application information and README content."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(language_manager.get_text("about_title"))
        self.setFixedSize(700, 600)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title and version
        title_label = QLabel("Speed Reader")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        version_label = QLabel(f"{language_manager.get_text('version')} 1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(version_label)
        
        # Description
        desc_label = QLabel(language_manager.get_text("description"))
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("margin: 10px 0;")
        layout.addWidget(desc_label)
        
        # Features section
        features_group = QGroupBox(language_manager.get_text("features"))
        features_layout = QVBoxLayout()
        
        features_text = f"""
• {language_manager.get_text('feature_pdf_epub')}
• {language_manager.get_text('feature_customizable_speed')}
• {language_manager.get_text('feature_progress_tracking')}
• {language_manager.get_text('feature_fullscreen')}
• {language_manager.get_text('feature_theme_support')}
• {language_manager.get_text('feature_font_size')}
• {language_manager.get_text('feature_paragraph_pauses')}
• {language_manager.get_text('feature_hotkeys')}
• {language_manager.get_text('feature_navigation')}
        """
        
        features_label = QLabel(features_text.strip())
        features_label.setWordWrap(True)
        features_layout.addWidget(features_label)
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # README section
        readme_group = QGroupBox("README")
        readme_layout = QVBoxLayout()
        
        # README link button
        readme_link_label = QLabel("View full README on GitHub:")
        readme_link_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        
        self.readme_link_btn = QPushButton("📖 Open README on GitHub")
        self.readme_link_btn.clicked.connect(self.open_readme_on_github)
        self.readme_link_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                border: 2px solid #007acc;
                border-radius: 5px;
                background-color: #f0f8ff;
                color: #007acc;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
                border-color: #005a9e;
            }
        """)
        
        readme_layout.addWidget(readme_link_label)
        readme_layout.addWidget(self.readme_link_btn)
        readme_group.setLayout(readme_layout)
        layout.addWidget(readme_group)
        
        # Repository section
        repo_layout = QHBoxLayout()
        repo_label = QLabel(f"{language_manager.get_text('repository')}:")
        self.repo_button = QPushButton("https://github.com/theilkerm/open-speed-reader")
        self.repo_button.clicked.connect(self.open_repository)
        self.repo_button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        repo_layout.addWidget(repo_label)
        repo_layout.addWidget(self.repo_button)
        layout.addLayout(repo_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.close_btn = QPushButton(language_manager.get_text("close"))
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setDefault(True)
        
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
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
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #fafafa;
            }
        """)
    
    def open_readme_on_github(self):
        """Open the README on GitHub in the default browser."""
        try:
            webbrowser.open("https://github.com/theilkerm/open-speed-reader#readme")
        except Exception as e:
            # Fallback: show error message
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Could not open README: {str(e)}")
    
    def open_repository(self):
        """Open the repository URL in the default browser."""
        try:
            webbrowser.open("https://github.com/theilkerm/open-speed-reader")
        except Exception as e:
            # Fallback: show error message
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Could not open repository: {str(e)}")
