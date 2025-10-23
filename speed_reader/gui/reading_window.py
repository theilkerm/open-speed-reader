"""
Fullscreen reading window for displaying words at specified WPM.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QProgressBar, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence

from ..utils.state_manager import save_progress
from ..utils.language_manager import language_manager
from .settings_dialog import SettingsDialog


class ReadingWindow(QWidget):
    """Fullscreen window for reading text word by word."""
    
    # Signal emitted when window is closed to return to main window
    closed = pyqtSignal()
    
    def __init__(self, word_list, total_word_count, start_index, file_path, settings):
        """
        Initialize the reading window.
        
        Args:
            word_list: List of words with paragraph break tokens
            total_word_count: Total count of actual words
            start_index: Starting word index
            file_path: Path to the document file
            settings: Dictionary with reading settings
        """
        super().__init__()
        
        # Store parameters
        self.words = word_list
        self.total_word_count = total_word_count
        self.current_index = start_index
        self.file_path = file_path
        self.settings = settings.copy()
        
        # Reading state
        self.is_paused = True
        self.words_read = 0  # Counter for actual words (excluding break tokens)
        
        # Timer for word display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_word)
        
        # Initialize UI
        self.init_ui()
        self.update_timer_interval()
        self.apply_styles()
        
        # Set focus to receive key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(language_manager.get_text("reading_title"))
        # Set fullscreen properly
        self.showFullScreen()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Top control bar
        control_bar = QWidget()
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        
        # Control buttons
        self.reset_btn = QPushButton()
        self.reset_btn.clicked.connect(self.reset_reading)
        
        self.rewind_10_btn = QPushButton()
        self.rewind_10_btn.clicked.connect(self.rewind_10_words)
        
        self.para_start_btn = QPushButton()
        self.para_start_btn.clicked.connect(self.rewind_to_paragraph)
        
        self.next_para_btn = QPushButton()
        self.next_para_btn.clicked.connect(self.jump_to_next_paragraph)
        
        self.jump_btn = QPushButton()
        self.jump_btn.clicked.connect(self.jump_to_word)
        
        self.play_pause_btn = QPushButton()
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        
        self.settings_btn = QPushButton()
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        
        # Add buttons to layout
        control_layout.addWidget(self.reset_btn)
        control_layout.addWidget(self.rewind_10_btn)
        control_layout.addWidget(self.para_start_btn)
        control_layout.addWidget(self.next_para_btn)
        control_layout.addWidget(self.jump_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.play_pause_btn)
        control_layout.addWidget(self.settings_btn)
        
        control_bar.setLayout(control_layout)
        layout.addWidget(control_bar)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_word_count)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 3px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 2px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Central word display
        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setWordWrap(True)
        layout.addWidget(self.word_label, 1)  # Give it most of the space
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Update UI text and initial status
        self.update_ui_text()
        self.update_status()
    
    def update_ui_text(self):
        """Update all UI text based on current language."""
        # Update window title
        self.setWindowTitle(language_manager.get_text("reading_title"))
        
        # Update button texts
        self.reset_btn.setText(language_manager.get_text("reset"))
        self.rewind_10_btn.setText(language_manager.get_text("rewind_10"))
        self.para_start_btn.setText(language_manager.get_text("para_start"))
        self.next_para_btn.setText(language_manager.get_text("next_para"))
        self.jump_btn.setText(language_manager.get_text("jump_to_word"))
        self.settings_btn.setText(language_manager.get_text("settings"))
        
        # Update play/pause button
        self.update_play_pause_button()
        
        # Update word label if paused
        if self.is_paused and self.current_index == 0:
            self.word_label.setText(language_manager.get_text("ready_to_start"))
    
    def start_reading(self):
        """Start the reading session."""
        self.is_paused = False
        self.update_timer_interval()
        self.timer.start()
        self.apply_styles()
        self.show_next_word()
        self.update_play_pause_button()
    
    def show_next_word(self):
        """Display the next word in the sequence."""
        if self.is_paused or self.current_index >= len(self.words):
            if self.current_index >= len(self.words):
                # Reached end of document
                self.timer.stop()
                self.is_paused = True
                self.word_label.setText(language_manager.get_text("reading_complete"))
                self.update_play_pause_button()
                self.update_status()
            return
        
        word = self.words[self.current_index]
        
        # Handle paragraph breaks
        if word == "__PARAGRAPH_BREAK__":
            self.timer.stop()
            pause_ms = int(self.settings['para_delay'] * 1000)
            QTimer.singleShot(pause_ms, self.resume_after_paragraph)
            self.current_index += 1
            return
        
        # Display the word
        self.word_label.setText(word)
        self.words_read += 1
        self.current_index += 1
        
        # Update progress bar
        self.progress_bar.setValue(self.words_read)
        self.update_status()
    
    def resume_after_paragraph(self):
        """Resume reading after paragraph pause."""
        if not self.is_paused:
            self.timer.start()
        self.show_next_word()
    
    def toggle_play_pause(self):
        """Toggle between play and pause states."""
        self.is_paused = not self.is_paused
        
        if not self.is_paused:
            self.timer.start()
        else:
            self.timer.stop()
        
        self.update_play_pause_button()
        self.update_status()
    
    def update_play_pause_button(self):
        """Update the play/pause button text and icon."""
        if self.is_paused:
            self.play_pause_btn.setText(language_manager.get_text("play"))
        else:
            self.play_pause_btn.setText(language_manager.get_text("pause"))
    
    def update_timer_interval(self):
        """Update the timer interval based on WPM setting."""
        delay_ms = (60 / self.settings['wpm']) * 1000
        self.timer.setInterval(int(delay_ms))
    
    def apply_styles(self):
        """Apply theme and font styles."""
        if self.settings['theme'] == 'dark':
            # Dark theme
            self.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 3px;
                    padding: 8px 12px;
                }
                QPushButton:hover {
                    background-color: #4c4c4c;
                }
                QPushButton:pressed {
                    background-color: #2c2c2c;
                }
            """)
        else:
            # Light theme
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QPushButton {
                    background-color: #f0f0f0;
                    color: #000000;
                    border: 1px solid #cccccc;
                    border-radius: 3px;
                    padding: 8px 12px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
        
        # Apply font size to word label
        font = QFont()
        font.setPointSize(self.settings['font_size'])
        self.word_label.setFont(font)
    
    def update_status(self):
        """Update the status label with current reading information."""
        if self.current_index >= len(self.words):
            status = language_manager.get_text("reading_complete")
        elif self.is_paused:
            remaining_words = self.total_word_count - self.words_read
            eta_minutes = remaining_words / self.settings['wpm'] if self.settings['wpm'] > 0 else 0
            eta_hours = int(eta_minutes // 60)
            eta_mins = int(eta_minutes % 60)
            eta_text = f"{eta_hours}{language_manager.get_text('hours')} {eta_mins}{language_manager.get_text('minutes')}" if eta_hours > 0 else f"{eta_mins}{language_manager.get_text('minutes')}"
            status = f"{language_manager.get_text('paused')} - {language_manager.get_text('word_of')} {self.words_read + 1} {self.total_word_count} - {language_manager.get_text('eta')}: {eta_text}"
        else:
            remaining_words = self.total_word_count - self.words_read
            eta_minutes = remaining_words / self.settings['wpm'] if self.settings['wpm'] > 0 else 0
            eta_hours = int(eta_minutes // 60)
            eta_mins = int(eta_minutes % 60)
            eta_text = f"{eta_hours}{language_manager.get_text('hours')} {eta_mins}{language_manager.get_text('minutes')}" if eta_hours > 0 else f"{eta_mins}{language_manager.get_text('minutes')}"
            status = f"{language_manager.get_text('reading')} - {language_manager.get_text('word_of')} {self.words_read + 1} {self.total_word_count} ({self.settings['wpm']} {language_manager.get_text('wpm_suffix').strip()}) - {language_manager.get_text('eta')}: {eta_text}"
        
        self.status_label.setText(status)
    
    def reset_reading(self):
        """Reset reading to the beginning."""
        self.timer.stop()
        self.current_index = 0
        self.words_read = 0
        self.progress_bar.setValue(0)
        self.word_label.setText(language_manager.get_text("ready_to_start"))
        self.update_status()
    
    def rewind_10_words(self):
        """Go back 10 words."""
        self.timer.stop()
        
        # Count back 10 actual words (skip paragraph breaks)
        words_to_go_back = 10
        new_index = self.current_index
        
        while words_to_go_back > 0 and new_index > 0:
            new_index -= 1
            if self.words[new_index] != "__PARAGRAPH_BREAK__":
                words_to_go_back -= 1
        
        self.current_index = new_index
        self.words_read = max(0, self.words_read - 10)
        self.progress_bar.setValue(self.words_read)
        
        if self.current_index < len(self.words):
            self.word_label.setText(self.words[self.current_index])
        
        self.update_status()
    
    def rewind_to_paragraph(self):
        """Go back to the start of the current paragraph."""
        self.timer.stop()
        
        # Find the start of current paragraph
        new_index = self.current_index
        while new_index > 0:
            new_index -= 1
            if self.words[new_index] == "__PARAGRAPH_BREAK__":
                new_index += 1  # Start after the break
                break
        
        # Count words to adjust words_read counter
        words_in_paragraph = 0
        for i in range(new_index, self.current_index):
            if self.words[i] != "__PARAGRAPH_BREAK__":
                words_in_paragraph += 1
        
        self.current_index = new_index
        self.words_read = max(0, self.words_read - words_in_paragraph)
        self.progress_bar.setValue(self.words_read)
        
        if self.current_index < len(self.words):
            self.word_label.setText(self.words[self.current_index])
        
        self.update_status()
    
    def jump_to_next_paragraph(self):
        """Jump to the start of the next paragraph."""
        self.timer.stop()
        
        # Find the next paragraph break
        new_index = self.current_index
        while new_index < len(self.words) - 1:
            new_index += 1
            if self.words[new_index] == "__PARAGRAPH_BREAK__":
                new_index += 1  # Start after the break
                break
        
        # Count words to adjust words_read counter
        words_in_paragraph = 0
        for i in range(self.current_index, new_index):
            if i < len(self.words) and self.words[i] != "__PARAGRAPH_BREAK__":
                words_in_paragraph += 1
        
        self.current_index = min(new_index, len(self.words) - 1)
        self.words_read = min(self.words_read + words_in_paragraph, self.total_word_count)
        self.progress_bar.setValue(self.words_read)
        
        if self.current_index < len(self.words):
            self.word_label.setText(self.words[self.current_index])
        
        self.update_status()
    
    def jump_to_word(self):
        """Open dialog to jump to a specific word number."""
        from PyQt6.QtWidgets import QInputDialog
        
        max_word = self.total_word_count
        current_word = self.words_read + 1
        
        word_num, ok = QInputDialog.getInt(
            self, 
            language_manager.get_text("jump_to_word_title"), 
            f"{language_manager.get_text('enter_word_number')} (1-{max_word}):", 
            current_word, 
            1, 
            max_word, 
            1
        )
        
        if ok:
            self.timer.stop()
            
            # Convert word number to index (word_num is 1-based, index is 0-based)
            target_word_count = word_num - 1
            
            # Find the index that corresponds to this word count
            new_index = 0
            word_count = 0
            
            for i, word in enumerate(self.words):
                if word != "__PARAGRAPH_BREAK__":
                    if word_count == target_word_count:
                        new_index = i
                        break
                    word_count += 1
            
            self.current_index = new_index
            self.words_read = target_word_count
            self.progress_bar.setValue(self.words_read)
            
            if self.current_index < len(self.words):
                self.word_label.setText(self.words[self.current_index])
            
            self.update_status()
    
    def open_settings_dialog(self):
        """Open the settings dialog for on-the-fly changes."""
        was_paused = self.is_paused
        self.timer.stop()
        
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update settings
            new_settings = dialog.get_settings()
            self.settings.update(new_settings)
            
            # Apply changes
            self.apply_styles()
            self.update_timer_interval()
            
            # Resume if it wasn't paused before
            if not was_paused:
                self.timer.start()
        
        self.update_status()
    
    def keyPressEvent(self, event):
        """Handle key press events for hotkeys."""
        if event.key() == Qt.Key.Key_Space:
            self.toggle_play_pause()
        elif event.key() == Qt.Key.Key_S:
            self.open_settings_dialog()
        elif event.key() == Qt.Key.Key_Escape:
            self.return_to_main()
        else:
            super().keyPressEvent(event)
    
    def return_to_main(self):
        """Return to main window."""
        self.timer.stop()
        save_progress(self.file_path, self.current_index)
        self.closed.emit()
        self.close()
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop timer
        self.timer.stop()
        
        # Save progress
        save_progress(self.file_path, self.current_index)
        
        # Emit closed signal to return to main window
        self.closed.emit()
        
        event.accept()
