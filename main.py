import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer

from ui.main_window import AstroSpecWindow
from ui.styles import ASTROSPEC_STYLE

class RobustSplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        # Make the window completely borderless and ensure it stays on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Fixed geometry matching your high-resolution background asset dimensions
        self.resize(800, 450)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # ---- UNIVERSAL ROOT PATH RESOLVER ----
        # Determine the base directory where the actual application files sit
        if hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.join(base_dir, "assets", "splash_background.png")
            
        # Alternate fallback: Look in the directory exactly next to the clicked application binary
        if not os.path.exists(img_path):
            exe_dir = os.path.dirname(sys.argv[0])
            img_path = os.path.join(exe_dir, "assets", "splash_background.png")
        # ----------------------------------------

        # Use forward slashes for CSS background path formatting on Windows
        css_safe_path = img_path.replace("\\", "/")

        # Base background frame
        self.background_frame = QFrame()
        frame_layout = QVBoxLayout()
        self.background_frame.setLayout(frame_layout)

        # Force the background image to render via direct CSS style injection
        if os.path.exists(img_path) and os.path.isfile(img_path):
            self.background_frame.setStyleSheet(
                f"""
                QFrame {{
                    background-image: url("{css_safe_path}");
                    background-position: center;
                    background-repeat: no-repeat;
                    border-radius: 12px;
                }}
                """
            )
            # Add a blank layout holder to let the background graphic show clearly
            dummy_spacer = QLabel()
            frame_layout.addWidget(dummy_spacer)
        else:
            # Clean backup layout theme if path strings mismatch
            self.background_frame.setStyleSheet(
                """
                QFrame {
                    background-color: #0b132b;
                    border: 2px solid #34495e;
                    border-radius: 12px;
                }
                """
            )
            status_text = QLabel("🚀 AstroSpec Engine Starting...")
            status_text.setStyleSheet("color: white; font-size: 24px; font-weight: bold; qproperty-alignment: 'AlignCenter';")
            frame_layout.addWidget(status_text)

        layout.addWidget(self.background_frame)
        self.center_on_screen()

        # Timer loop: Hold splash for exactly 3 seconds, then transition to workspace
        QTimer.singleShot(3000, self.launch_main_app)

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def launch_main_app(self):
        self.main_win = AstroSpecWindow()
        self.main_win.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(ASTROSPEC_STYLE)

    splash = RobustSplashScreen()
    splash.show()

    sys.exit(app.exec_())
