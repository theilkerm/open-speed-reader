"""
State management utilities for saving and loading reading progress.
"""

import json
import os
from typing import Dict, Any


class StateManager:
    """Manages reading progress state using JSON file storage."""
    
    def __init__(self, progress_file: str = "progress.json"):
        """
        Initialize the state manager.
        
        Args:
            progress_file: Path to the JSON file storing progress data
        """
        self.progress_file = progress_file
        self._ensure_progress_file_exists()
    
    def _ensure_progress_file_exists(self):
        """Ensure the progress file exists and is valid JSON."""
        if not os.path.exists(self.progress_file):
            # Create empty progress file
            try:
                with open(self.progress_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2)
            except (OSError, IOError) as e:
                # If we can't create the file, that's okay - we'll handle it in other methods
                pass
        else:
            # Validate existing file
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except (json.JSONDecodeError, ValueError, OSError, IOError):
                # If file is corrupted or can't be read, recreate it
                try:
                    with open(self.progress_file, 'w', encoding='utf-8') as f:
                        json.dump({}, f, indent=2)
                except (OSError, IOError):
                    # If we can't write the file, that's okay - we'll handle it in other methods
                    pass
    
    def save_progress(self, file_path: str, word_index: int) -> None:
        """
        Save the current reading progress for a file.
        
        Args:
            file_path: Path to the document file
            word_index: Current word index position
        """
        # Normalize file path for consistent storage
        normalized_path = os.path.normpath(os.path.abspath(file_path))
        
        try:
            # Load existing progress
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
            progress_data = {}
        
        # Update progress for this file
        progress_data[normalized_path] = word_index
        
        # Save updated progress
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, indent=2)
        except (OSError, IOError):
            # If we can't save progress, that's okay - the app will still work
            pass
    
    def load_progress(self, file_path: str) -> int:
        """
        Load the saved reading progress for a file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            The saved word index, or 0 if no progress is found
        """
        # Normalize file path for consistent lookup
        normalized_path = os.path.normpath(os.path.abspath(file_path))
        
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            
            return progress_data.get(normalized_path, 0)
        except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
            return 0
    
    def clear_progress(self, file_path: str = None) -> None:
        """
        Clear progress for a specific file or all files.
        
        Args:
            file_path: Path to specific file to clear, or None to clear all
        """
        if file_path is None:
            # Clear all progress
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
        else:
            # Clear progress for specific file
            normalized_path = os.path.normpath(os.path.abspath(file_path))
            
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
                
                if normalized_path in progress_data:
                    del progress_data[normalized_path]
                    
                    with open(self.progress_file, 'w', encoding='utf-8') as f:
                        json.dump(progress_data, f, indent=2)
            except (json.JSONDecodeError, FileNotFoundError):
                pass  # File doesn't exist or is corrupted, nothing to clear
    
    def get_all_progress(self) -> Dict[str, int]:
        """
        Get all saved progress data.
        
        Returns:
            Dictionary mapping file paths to word indices
        """
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
            return {}


# Convenience functions for backward compatibility
def save_progress(file_path: str, word_index: int) -> None:
    """Save progress using the default state manager."""
    manager = StateManager()
    manager.save_progress(file_path, word_index)


def load_progress(file_path: str) -> int:
    """Load progress using the default state manager."""
    manager = StateManager()
    return manager.load_progress(file_path)
