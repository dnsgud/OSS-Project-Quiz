import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QTimer, Qt
from PIL import Image
import os
import random

class BrandLogoQuiz:
    def __init__(self, logo_directory):
        self.logo_directory = logo_directory
        self.logo_files = [f for f in os.listdir(self.logo_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.logo_files:
            print("No valid logo image files found in the directory.")
            sys.exit()

        self.coordinates = (100, 50, 300, 250)
        self.current_logo_file = ""
        self.score = 0
        self.countdown = 5
        self.countdown_timer = QTimer()

        self.app = QApplication(sys.argv)
        self.root = QWidget()
        self.root.setWindowTitle("Brand Logo Quiz")

        self.setup_ui()
