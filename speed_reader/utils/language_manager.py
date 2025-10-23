"""
Language management system for internationalization.
"""

import json
import os
from typing import Dict, Any


class LanguageManager:
    """Manages language translations and switching."""
    
    def __init__(self):
        self.current_language = "en"
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all available translations."""
        # English translations
        self.translations["en"] = {
            # Main window
            "app_title": "Speed Reader",
            "file_selection": "File Selection",
            "select_file": "Select File",
            "no_file_selected": "No file selected",
            "selected": "Selected",
            "reading_settings": "Reading Settings",
            "words_per_minute": "Words Per Minute",
            "font_size": "Font Size",
            "paragraph_pause": "Paragraph Pause",
            "theme": "Theme",
            "light": "Light",
            "dark": "Dark",
            "recent_readings": "Recent Readings",
            "start_reading": "Start Reading",
            "wpm_suffix": " WPM",
            "px_suffix": " px",
            "sec_suffix": " sec",
            
            # Reading window
            "reading_title": "Speed Reader - Reading",
            "ready_to_start": "Ready to start reading...",
            "reading_complete": "Reading Complete!",
            "reset": "Reset (<<)",
            "rewind_10": "10 Words Back (<)",
            "para_start": "Paragraph Start (|<)",
            "next_para": "Next Paragraph (|>)",
            "jump_to_word": "Jump to Word (#)",
            "play": "Play (►)",
            "pause": "Pause (||)",
            "settings": "Settings (⚙)",
            "paused": "Paused",
            "reading": "Reading",
            "word_of": "of",
            "eta": "ETA",
            "hours": "h",
            "minutes": "m",
            
            # Settings dialog
            "settings_title": "Reading Settings",
            "ok": "OK",
            "cancel": "Cancel",
            
            # Menu bar
            "file_menu": "File",
            "help_menu": "Help",
            "language_menu": "Language",
            "about": "About",
            "exit": "Exit",
            "turkish": "Türkçe",
            "english": "English",
            
            # About dialog
            "about_title": "About Speed Reader",
            "version": "Version",
            "description": "A cross-platform desktop application for speed reading PDF and EPUB documents.",
            "features": "Features",
            "repository": "Repository",
            "open_repository": "Open Repository",
            "close": "Close",
            
            # Messages
            "no_file_selected_msg": "Please select a file first.",
            "no_text_found": "No readable text was found in the selected file.",
            "error": "Error",
            "failed_to_open": "Failed to open the document:",
            "failed_to_select": "Failed to select the file:",
            "jump_to_word_title": "Jump to Word",
            "enter_word_number": "Enter word number",
            
            # Features list
            "feature_pdf_epub": "PDF and EPUB Support",
            "feature_customizable_speed": "Customizable Reading Speed",
            "feature_progress_tracking": "Progress Tracking",
            "feature_fullscreen": "Fullscreen Reading",
            "feature_theme_support": "Theme Support",
            "feature_font_size": "Adjustable Font Size",
            "feature_paragraph_pauses": "Paragraph Pauses",
            "feature_hotkeys": "Hotkeys",
            "feature_navigation": "Navigation Controls"
        }
        
        # Turkish translations
        self.translations["tr"] = {
            # Main window
            "app_title": "Hızlı Okuyucu",
            "file_selection": "Dosya Seçimi",
            "select_file": "Dosya Seç",
            "no_file_selected": "Dosya seçilmedi",
            "selected": "Seçilen",
            "reading_settings": "Okuma Ayarları",
            "words_per_minute": "Dakikada Kelime",
            "font_size": "Yazı Boyutu",
            "paragraph_pause": "Paragraf Duraklaması",
            "theme": "Tema",
            "light": "Açık",
            "dark": "Koyu",
            "recent_readings": "Son Okumalar",
            "start_reading": "Okumaya Başla",
            "wpm_suffix": " K/D",
            "px_suffix": " px",
            "sec_suffix": " sn",
            
            # Reading window
            "reading_title": "Hızlı Okuyucu - Okuma",
            "ready_to_start": "Okumaya başlamaya hazır...",
            "reading_complete": "Okuma Tamamlandı!",
            "reset": "Sıfırla (<<)",
            "rewind_10": "10 Kelime Geri (<)",
            "para_start": "Paragraf Başı (|<)",
            "next_para": "Sonraki Paragraf (|>)",
            "jump_to_word": "Kelimeye Git (#)",
            "play": "Oynat (►)",
            "pause": "Duraklat (||)",
            "settings": "Ayarlar (⚙)",
            "paused": "Duraklatıldı",
            "reading": "Okunuyor",
            "word_of": "kelimesi",
            "eta": "Tahmini Süre",
            "hours": "sa",
            "minutes": "dk",
            
            # Settings dialog
            "settings_title": "Okuma Ayarları",
            "ok": "Tamam",
            "cancel": "İptal",
            
            # Menu bar
            "file_menu": "Dosya",
            "help_menu": "Yardım",
            "language_menu": "Dil",
            "about": "Hakkında",
            "exit": "Çıkış",
            "turkish": "Türkçe",
            "english": "English",
            
            # About dialog
            "about_title": "Hızlı Okuyucu Hakkında",
            "version": "Sürüm",
            "description": "PDF ve EPUB belgelerini hızlı okuma için çapraz platform masaüstü uygulaması.",
            "features": "Özellikler",
            "repository": "Depo",
            "open_repository": "Depoyu Aç",
            "close": "Kapat",
            
            # Messages
            "no_file_selected_msg": "Lütfen önce bir dosya seçin.",
            "no_text_found": "Seçilen dosyada okunabilir metin bulunamadı.",
            "error": "Hata",
            "failed_to_open": "Belge açılamadı:",
            "failed_to_select": "Dosya seçilemedi:",
            "jump_to_word_title": "Kelimeye Git",
            "enter_word_number": "Kelime numarasını girin",
            
            # Features list
            "feature_pdf_epub": "PDF ve EPUB Desteği",
            "feature_customizable_speed": "Özelleştirilebilir Okuma Hızı",
            "feature_progress_tracking": "İlerleme Takibi",
            "feature_fullscreen": "Tam Ekran Okuma",
            "feature_theme_support": "Tema Desteği",
            "feature_font_size": "Ayarlanabilir Yazı Boyutu",
            "feature_paragraph_pauses": "Paragraf Duraklamaları",
            "feature_hotkeys": "Kısayol Tuşları",
            "feature_navigation": "Navigasyon Kontrolleri"
        }
    
    def get_text(self, key: str) -> str:
        """Get translated text for the given key."""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language: str):
        """Set the current language."""
        if language in self.translations:
            self.current_language = language
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages with their display names."""
        return {
            "en": self.translations["en"]["english"],
            "tr": self.translations["tr"]["turkish"]
        }
    
    def get_current_language(self) -> str:
        """Get the current language code."""
        return self.current_language


# Global language manager instance
language_manager = LanguageManager()
