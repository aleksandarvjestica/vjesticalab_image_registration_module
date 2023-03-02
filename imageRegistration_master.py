from functools import partial
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set the window title
        self.setWindowTitle("VLab | Image registration")
        self.clickParam = ''
        
        #Create a display image
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap("Support_files/Vlab_icon_50x50-01.png"))
        self.image_label.setAlignment(Qt.AlignCenter)

        ####### Section A #######
        ####### Modules for initial registration and calculation of transformation matrices ########
        # Create a label
        self.label_section_A = QLabel('<b>Calculate & Perform registration</b>', self)
        self.label_section_A.setTextFormat(Qt.RichText)
        # Create buttons
        self.buttonA1 = QPushButton("Individual image")
        self.buttonA1.clicked.connect(partial(self.registration, 'singleFile'))

        self.buttonA2 = QPushButton("Folder of images")
        self.buttonA2.clicked.connect(partial(self.registration, 'singleFolder'))

        self.buttonA3 = QPushButton("Collection of folders")
        self.buttonA3.clicked.connect(partial(self.registration, 'multiFolder'))
        
        ####### Section B #######
        ####### Use registration matrices to register images ########
        # Create a label
        self.label_section_B = QLabel('<b>Align with transformation matrices</b>', self)
        self.label_section_B.setTextFormat(Qt.RichText)
        # Create buttons
        self.buttonB0 = QPushButton("View aligned tyx image")
        self.buttonB0.clicked.connect(partial(self.alignment, 'view'))
        
        self.buttonB1 = QPushButton("Align image or image set")
        self.buttonB1.clicked.connect(partial(self.alignment, 'singleFile'))

        self.buttonB2 = QPushButton("Align folder of images")
        self.buttonB2.clicked.connect(partial(self.alignment, 'singleFolder'))

        self.buttonB3 = QPushButton("Align collection of folders")
        self.buttonB3.clicked.connect(partial(self.alignment, 'multiFolder'))

        ####### Section C #######
        ####### Modules for modifying registration matrices ########
        # Create a label
        self.label_section_C = QLabel('<b>Edit transformation matrices</b>', self)
        self.label_section_C.setTextFormat(Qt.RichText)
        # Create buttons
        self.buttonC1 = QPushButton("Individual")
    
        self.buttonC1.clicked.connect(partial(self.editing, 'single'))

        self.buttonC2 = QPushButton("Folder")
        self.buttonC2.clicked.connect(partial(self.editing, 'folder'))

        # Create a button to quit
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)


        # Add a horizontal line to the layout
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.HLine)
        
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)        
        
        self.line3 = QFrame()
        self.line3.setFrameShape(QFrame.HLine)    
        
        # Create the layout
        layout = QVBoxLayout()
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.label_section_A)
        layout.addWidget(self.buttonA1)
        layout.addWidget(self.buttonA2)
        layout.addWidget(self.buttonA3)

        layout.addWidget(self.line1)

        layout.addWidget(self.label_section_B)
        layout.addWidget(self.buttonB0)
        layout.addWidget(self.buttonB1)
        layout.addWidget(self.buttonB2)
        layout.addWidget(self.buttonB3)

        
        layout.addWidget(self.line2)        

        layout.addWidget(self.label_section_C)
        layout.addWidget(self.buttonC1)
        layout.addWidget(self.buttonC2)

        layout.addWidget(self.line3)     
        layout.addWidget(self.quit_button)        
        self.setLayout(layout)
        self.setFixedWidth(250)
        
        
    def registration(self, param):
        # Create a QProcess to run the Python interpreter
        process = QProcess(self)
        qscript = "registration/registration.py"
        qinterpreter = sys.executable #python path
        # Start the Python interpreter and run python script
        process.setStandardOutputFile("log/output_registration.txt")
        process.setStandardErrorFile("log/output_registration.txt")
        process.start(qinterpreter, [qscript, param])

    def alignment(self, param):
        # Create a QProcess to run the Python interpreter
        process = QProcess(self)
        qscript = "alignment/alignment.py"
        qinterpreter = sys.executable #python path
        # Start the Python interpreter and run python script
        process.setStandardOutputFile("log/output_alignment.txt")
        process.setStandardErrorFile("log/output_alignment.txt")
        process.start(qinterpreter, [qscript, param])

    def editing(self, param):
        # Create a QProcess to run the Python interpreter
        process = QProcess(self)
        qscript = "registrationEditing/editing.py"
        qinterpreter = sys.executable #python path
        # Start the Python interpreter and run python script
        process.setStandardOutputFile("log/output_editing.txt")
        process.setStandardErrorFile("log/output_editing.txt")
        process.start(qinterpreter, [qscript, param])

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.move(0,0)
    window.show()
    sys.exit(app.exec_())