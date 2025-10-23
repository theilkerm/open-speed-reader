"""
Installation script for Speed Reader dependencies.
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        print("Installing Speed Reader dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def verify_installation():
    """Verify that all required modules can be imported"""
    try:
        print("Verifying installation...")
        
        # Test PyQt6
        from PyQt6.QtWidgets import QApplication
        print("✅ PyQt6 imported successfully")
        
        # Test PyMuPDF
        import fitz
        print("✅ PyMuPDF imported successfully")
        
        # Test ebooklib
        import ebooklib
        print("✅ ebooklib imported successfully")
        
        # Test BeautifulSoup
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
        
        # Test application modules
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from speed_reader.gui.main_window import MainWindow
        from speed_reader.utils.parser import parse_document
        from speed_reader.utils.state_manager import StateManager
        print("✅ Application modules imported successfully")
        
        print("\n🎉 Installation verification complete!")
        print("You can now run the application with: python main.py")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False


def main():
    """Main installation function"""
    print("Speed Reader - Installation Script")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("Installation failed. Please check the error messages above.")
        return False
    
    print()
    
    # Verify installation
    if not verify_installation():
        print("Verification failed. Some dependencies may not be installed correctly.")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
