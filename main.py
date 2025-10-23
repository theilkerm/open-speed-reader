"""
Speed Reader Application - Main Entry Point

A PyQt6-based desktop application for speed reading PDF and EPUB documents.
Displays text one word at a time at user-defined WPM with customizable settings.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add the speed_reader package to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speed_reader.gui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Speed Reader")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Speed Reader")
    
    # Set application properties
    # Note: AA_EnableHighDpiScaling and AA_UseHighDpiPixmaps are deprecated in PyQt6
    # High DPI scaling is enabled by default in PyQt6
    
    try:
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        # Start the application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        # Show error message if application fails to start
        QMessageBox.critical(
            None,
            "Application Error",
            f"Failed to start Speed Reader:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
