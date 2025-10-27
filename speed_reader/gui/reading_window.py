"""
Fullscreen reading window for displaying words at specified WPM.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QProgressBar, QMessageBox, QDialog, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QKeySequence, QTextCursor, QTextCharFormat, QColor, QTextOption

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
        
        # Prepare preview text
        self.prepare_text_preview()
        
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
        
        self.toggle_preview_btn = QPushButton()
        self.toggle_preview_btn.clicked.connect(self.toggle_text_preview)
        self.preview_visible = True
        
        # Add buttons to layout
        control_layout.addWidget(self.reset_btn)
        control_layout.addWidget(self.rewind_10_btn)
        control_layout.addWidget(self.para_start_btn)
        control_layout.addWidget(self.next_para_btn)
        control_layout.addWidget(self.jump_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.toggle_preview_btn)
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
        
        # Create splitter for main reading area and text preview
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Central word display and status
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setWordWrap(True)
        left_layout.addWidget(self.word_label, 1)
        
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        left_layout.addWidget(self.status_label)
        
        left_widget.setLayout(left_layout)
        self.splitter.addWidget(left_widget)
        
        # Right side: Text preview (book silhouette)
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self.splitter.addWidget(self.text_preview)
        
        # Set splitter sizes (60% left, 40% right)
        self.splitter.setSizes([600, 400])
        
        layout.addWidget(self.splitter, 1)
        
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
        
        # Update toggle preview button
        if self.preview_visible:
            self.toggle_preview_btn.setText("Hide Preview")
        else:
            self.toggle_preview_btn.setText("Show Preview")
        
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
    
    def prepare_text_preview(self):
        """Prepare the text preview with initial words around current position."""
        # Store all word positions for jump functionality
        self.word_positions = []
        for i, word in enumerate(self.words):
            if word == "__PARAGRAPH_BREAK__":
                self.word_positions.append(("\n", i))
            else:
                self.word_positions.append((word + " ", i))
        
        # Connect mouse click event
        self.text_preview.mousePressEvent = self.on_text_preview_click
        
        # Connect scroll bar changes for lazy loading
        self.text_preview.verticalScrollBar().valueChanged.connect(self.on_scroll_changed)
        self._auto_scrolling = False  # Flag to track programmatic scrolling
        self._last_extend_direction = None  # Track last extend direction to prevent duplicates
        
        # Load initial preview window (1000 words before and after current)
        self.update_preview_window()
    
    def update_preview_window(self, extend_forward=False, extend_backward=False):
        """Update the preview window to show words around current position."""
        window_size = 1000  # Show 1000 words before and after current
        
        # Save current scroll position before changing text
        scrollbar = self.text_preview.verticalScrollBar()
        scroll_percent = scrollbar.value() / scrollbar.maximum() if scrollbar.maximum() > 0 else 0
        
        # Get current window bounds
        if hasattr(self, 'preview_start_idx') and hasattr(self, 'preview_end_idx'):
            current_start = self.preview_start_idx
            current_end = self.preview_end_idx
        else:
            current_start = max(0, self.current_index - window_size)
            current_end = min(len(self.words), self.current_index + window_size)
        
        # Determine new bounds
        if extend_forward:
            # Extend forward by 500 words
            start_idx = current_start
            end_idx = min(len(self.words), current_end + 500)
        elif extend_backward:
            # Extend backward by 500 words
            start_idx = max(0, current_start - 500)
            end_idx = current_end
        else:
            # Center around current position
            start_idx = max(0, self.current_index - window_size)
            end_idx = min(len(self.words), self.current_index + window_size)
        
        # Build text content for this window
        text_content = ""
        window_word_positions = {}  # Map word index to position in window text
        
        for i in range(start_idx, end_idx):
            word, original_idx = self.word_positions[i]
            start_pos = len(text_content)
            
            if word == "\n":
                text_content += "\n"
                end_pos = len(text_content)
            else:
                text_content += word
                end_pos = len(text_content)
            
            window_word_positions[original_idx] = (start_pos, end_pos)
        
        # Store window info
        self.preview_start_idx = start_idx
        self.preview_end_idx = end_idx
        self.window_word_positions = window_word_positions
        self.window_text = text_content
        
        # Set text
        self.text_preview.setPlainText(text_content)
        
        # Apply theme-based text color
        is_dark = self.settings.get('theme', 'light') == 'dark'
        cursor = QTextCursor(self.text_preview.document())
        cursor.select(QTextCursor.SelectionType.Document)
        format = QTextCharFormat()
        if is_dark:
            format.setForeground(QColor("#ffffff"))
        else:
            format.setForeground(QColor("#000000"))
        cursor.setCharFormat(format)
        
        # Restore scroll position
        scrollbar = self.text_preview.verticalScrollBar()
        if scrollbar.maximum() > 0:
            target_pos = int(scrollbar.maximum() * scroll_percent)
            self._auto_scrolling = True
            scrollbar.setValue(target_pos)
            self._auto_scrolling = False
        
        # Reset extend direction flag after window update
        self._last_extend_direction = None
        
        # Update highlight
        self.update_text_preview_highlight()
    
    def on_scroll_changed(self, value):
        """Handle scroll bar changes for lazy loading."""
        # Ignore programmatic scrolling
        if self._auto_scrolling:
            return
        
        scrollbar = self.text_preview.verticalScrollBar()
        if scrollbar.maximum() == 0:
            return
        
        # Check if at or near the end (load more forward)
        # Use value + page size to check if visible area reaches near the end
        visible_end = value + scrollbar.pageStep()
        scroll_percent = value / scrollbar.maximum()
        
        # Near end or at bottom - load more forward
        if visible_end >= scrollbar.maximum() - 10:  # Within 10 pixels of bottom
            if self.preview_end_idx < len(self.words) and self._last_extend_direction != 'forward':
                self._last_extend_direction = 'forward'
                self.update_preview_window(extend_forward=True)
        # Near beginning - load more backward
        elif scroll_percent < 0.2:
            if self.preview_start_idx > 0 and self._last_extend_direction != 'backward':
                self._last_extend_direction = 'backward'
                self.update_preview_window(extend_backward=True)
        else:
            # Reset extend direction when not at edges
            self._last_extend_direction = None
    
    def on_text_preview_click(self, event):
        """Handle mouse click on text preview to jump to position."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Get cursor position at click
            cursor = self.text_preview.cursorForPosition(event.pos())
            
            # Pause reading
            self.timer.stop()
            self.is_paused = True
            self.update_play_pause_button()
            
            # Find which word this corresponds to
            click_position = cursor.position()
            word_index = self.get_word_index_at_position(click_position)
            
            if word_index is not None:
                # Jump to that word
                self.current_index = word_index
                
                # Recalculate words_read based on index
                words_read = 0
                for i in range(word_index):
                    if self.words[i] != "__PARAGRAPH_BREAK__":
                        words_read += 1
                
                self.words_read = words_read
                self.progress_bar.setValue(self.words_read)
                
                # Update display
                if self.current_index < len(self.words):
                    word = self.words[self.current_index]
                    if word != "__PARAGRAPH_BREAK__":
                        self.word_label.setText(word)
                    else:
                        self.word_label.setText("...")
                
                # Check if outside window, reload if needed
                if not hasattr(self, 'preview_start_idx') or self.current_index < self.preview_start_idx or self.current_index >= self.preview_end_idx:
                    self.update_preview_window()
                else:
                    self.update_text_preview_highlight()
                self.update_status()
    
    def get_word_index_at_position(self, position):
        """Get the word index corresponding to a text position in preview window."""
        if not hasattr(self, 'window_word_positions'):
            return self.current_index
        
        # Find the word in current window that contains this position
        best_match = None
        best_dist = float('inf')
        
        for word_idx, (start_pos, end_pos) in self.window_word_positions.items():
            if start_pos <= position <= end_pos:
                return word_idx
            else:
                # Find closest word
                dist = min(abs(position - start_pos), abs(position - end_pos))
                if dist < best_dist:
                    best_dist = dist
                    best_match = word_idx
        
        return best_match if best_match is not None else self.current_index
    
    def update_text_preview_highlight(self):
        """Update the highlight of current word in text preview."""
        if not hasattr(self, 'text_preview') or not hasattr(self, 'window_word_positions'):
            return
        
        # Check if current index is outside preview window, if so reload window
        if self.current_index < self.preview_start_idx or self.current_index >= self.preview_end_idx:
            self.update_preview_window()
            return
        
        # Find current word position in window
        if self.current_index not in self.window_word_positions:
            return
        
        start_pos, end_pos = self.window_word_positions[self.current_index]
        current_word, _ = self.word_positions[self.current_index]
        
        if current_word == "\n":
            return
        
        # Get theme-based colors
        is_dark = self.settings.get('theme', 'light') == 'dark'
        
        # Efficiently update highlights: only format affected regions
        document = self.text_preview.document()
        
        # Clear previous highlight if exists
        if hasattr(self, '_last_highlight_pos'):
            last_start, last_end = self._last_highlight_pos
            cursor = QTextCursor(document)
            cursor.setPosition(last_start)
            cursor.setPosition(last_end, QTextCursor.MoveMode.KeepAnchor)
            reset_format = QTextCharFormat()
            if is_dark:
                reset_format.setBackground(QColor("#2a2a2a"))
                reset_format.setForeground(QColor("#ffffff"))
            else:
                reset_format.setBackground(QColor("#ffffff"))
                reset_format.setForeground(QColor("#000000"))
            cursor.setCharFormat(reset_format)
        
        # Apply new highlight
        cursor = QTextCursor(document)
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.MoveMode.KeepAnchor)
        
        highlight_format = QTextCharFormat()
        if is_dark:
            highlight_format.setBackground(QColor("#4a4a2a"))
            highlight_format.setForeground(QColor("#ffff00"))
        else:
            highlight_format.setBackground(QColor("#ffff00"))
            highlight_format.setForeground(QColor("#000000"))
        cursor.setCharFormat(highlight_format)
        
        # Store current highlight position
        self._last_highlight_pos = (start_pos, end_pos)
        
        # Auto-scroll every 30 words
        if not hasattr(self, '_scroll_counter'):
            self._scroll_counter = 0
        self._scroll_counter += 1
        
        if self._scroll_counter % 30 == 0:
            scrollbar = self.text_preview.verticalScrollBar()
            if scrollbar.maximum() > 0:
                target_pos = int(scrollbar.maximum() * (start_pos / len(self.window_text)))
                self._auto_scrolling = True
                scrollbar.setValue(target_pos)
                self._auto_scrolling = False
    
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
        
        # Update text preview highlight every word
        self.update_text_preview_highlight()
        
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
            # Starting automatic reading - reset preview window to ±1000 words
            self.update_preview_window()
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
    
    def toggle_text_preview(self):
        """Toggle visibility of text preview."""
        self.preview_visible = not self.preview_visible
        
        if self.preview_visible:
            self.text_preview.show()
            self.toggle_preview_btn.setText("Hide Preview")
            # Restore splitter sizes
            self.splitter.setSizes([600, 400])
        else:
            self.text_preview.hide()
            self.toggle_preview_btn.setText("Show Preview")
            # Make left side take full width
            self.splitter.setSizes([1000, 0])
    
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
                QTextEdit {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    border: 1px solid #555555;
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
                QTextEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
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
        self.update_preview_window()
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
        
        # Check if outside window, reload if needed
        if not hasattr(self, 'preview_start_idx') or self.current_index < self.preview_start_idx or self.current_index >= self.preview_end_idx:
            self.update_preview_window()
        else:
            self.update_text_preview_highlight()
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
        
        # Check if outside window, reload if needed
        if not hasattr(self, 'preview_start_idx') or self.current_index < self.preview_start_idx or self.current_index >= self.preview_end_idx:
            self.update_preview_window()
        else:
            self.update_text_preview_highlight()
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
        
        # Check if outside window, reload if needed
        if not hasattr(self, 'preview_start_idx') or self.current_index < self.preview_start_idx or self.current_index >= self.preview_end_idx:
            self.update_preview_window()
        else:
            self.update_text_preview_highlight()
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
            
            # Check if outside window, reload if needed
            if not hasattr(self, 'preview_start_idx') or self.current_index < self.preview_start_idx or self.current_index >= self.preview_end_idx:
                self.update_preview_window()
            else:
                self.update_text_preview_highlight()
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
        elif event.key() == Qt.Key.Key_P:
            self.toggle_text_preview()
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
