# Speed Reader

A cross-platform desktop application built with PyQt6 for speed reading PDF and EPUB documents. The application displays text one word at a time at a user-defined Words Per Minute (WPM) rate.

## Features

- **PDF and EPUB Support**: Read both PDF and EPUB documents
- **Customizable Reading Speed**: Adjust WPM from 100 to 1000 words per minute
- **Progress Tracking**: Automatically saves and resumes reading progress
- **Fullscreen Reading**: Distraction-free reading experience
- **Theme Support**: Light and dark themes
- **Adjustable Font Size**: Customize text size from 24px to 200px
- **Paragraph Pauses**: Configurable pause between paragraphs
- **Hotkeys**: Space to play/pause, S for settings, Escape to exit
- **Navigation Controls**: Reset, rewind 10 words, or go back to paragraph start

## Installation

1. **Install Python 3.8 or higher**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Getting Started

1. **Launch the application** by running `python main.py`
2. **Select a file** using the "Select File" button (supports PDF and EPUB)
3. **Adjust settings**:
   - Words Per Minute (WPM): Reading speed (100-1000)
   - Font Size: Text size (24-200px)
   - Paragraph Pause: Delay between paragraphs (0-5 seconds)
   - Theme: Light or Dark
4. **Click "Start Reading"** to begin

### Reading Interface

The reading interface provides several controls:

- **Reset (<<)**: Start from the beginning
- **10 Words Back (<)**: Go back 10 words
- **Paragraph Start (|<)**: Go back to start of current paragraph
- **Play/Pause (►/||)**: Toggle reading
- **Settings (⚙)**: Adjust settings during reading

### Hotkeys

- **Space**: Play/Pause
- **S**: Open settings dialog
- **Escape**: Exit reading mode

### Progress Tracking

The application automatically saves your reading progress in `progress.json` (created automatically on first use). When you reopen a document, it will resume from where you left off. This file is ignored by git to keep user progress private.

## Project Structure

```
speed_reader/
├── main.py                 # Application entry point
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # File selection and settings
│   ├── reading_window.py   # Fullscreen reading interface
│   └── settings_dialog.py  # On-the-fly settings dialog
├── utils/
│   ├── __init__.py
│   ├── parser.py           # PDF and EPUB text extraction
│   └── state_manager.py    # Progress tracking
├── progress.json           # Reading progress storage (auto-created)
└── requirements.txt        # Python dependencies
```

## Dependencies

- **PyQt6**: GUI framework
- **PyMuPDF**: PDF text extraction
- **ebooklib**: EPUB parsing
- **beautifulsoup4**: HTML parsing for EPUB content

## Technical Details

### Text Processing

- PDFs are processed using PyMuPDF (fitz) to extract text from all pages
- EPUBs are processed using ebooklib to extract text from HTML chapters
- Text is normalized and split into words with paragraph break markers
- Special tokens (`__PARAGRAPH_BREAK__`) are inserted to handle paragraph pauses

### State Management

- Reading progress is stored in JSON format
- File paths are normalized for consistent storage
- Progress is automatically saved when closing the reading window

### Performance

- Efficient word-by-word display using QTimer
- Minimal memory footprint for large documents
- Responsive UI with proper event handling

## Troubleshooting

### Common Issues

1. **"No readable text found"**: The document may be image-based or corrupted
2. **Import errors**: Ensure all dependencies are installed correctly
3. **File not opening**: Check file permissions and format support

### Error Messages

- **"PyMuPDF (fitz) is required"**: Install with `pip install PyMuPDF`
- **"ebooklib and BeautifulSoup are required"**: Install with `pip install ebooklib beautifulsoup4`

## License

This project is open source. See LICENSE.md for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.