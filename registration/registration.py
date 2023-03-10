import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QWidget, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
import registration_functions as f

class SingleFile(QWidget):
    def __init__(self):
        super().__init__()

        # Create a label and a text input field for the folder path
        self.setWindowTitle("Single image registration")
        
        self.display1 = QLabel("Step1: \tSelect image file to process")
        self.selected_file = QLineEdit()
        # Create a button to open the file browser and fill the selected_file field
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)

        # Create a label and a text input field for the reference file identifier
        self.display2 = QLabel("\nStep2: \tThe basename (string preceeding the _) \n\tcan be used to co-align files.")
        self.coalignment_yn = QCheckBox("Co-align files with the same basename")

        # Create a button to process the input
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.process_input)

        # Create a button to quit
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.selected_file)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.display2)
        layout.addWidget(self.coalignment_yn)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        self.selected_file.setText(file_path)

    def process_input(self):
        path = self.selected_file.text()
        print('\nSelected file is:', path)

        reference_identifier = 'Calculated in target function'

        coalignment = self.coalignment_yn.isChecked()
        print('\nCo-alignment will be performed? ', coalignment)

        if os.path.isfile(path):
            print('\nFile found. Starting registration...')
            try:
                f.registration_main(path, reference_identifier, coalignment)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
                print('\n')
                raise(e)
        else:
            print('\nNo such file found!')

        self.close()

class SingleFolder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image folder registration")

        # Create a label and a text input field for the folder path
        self.display1 = QLabel("Step1: Select folder to process")
        self.selected_folder = QLineEdit()
        # Create a button to open the file browser and fill the selected_folder field
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_folder)

        # Create a label and a text input field for the reference file identifier
        self.display2 = QLabel("\nStep2: Specify the unique identifier of reference files")
        self.reference_identifier_entry = QLineEdit()

        # Create a checkbox for co-alignment
        self.display3 = QLabel("\nStep3:")
        self.coalignment_yn = QCheckBox("Co-align files with the same basename")

        # Create a button to process the input
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.process_input)

        # Create a button to quit
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.selected_folder)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.display2)
        layout.addWidget(self.reference_identifier_entry)
        layout.addWidget(self.display3)
        layout.addWidget(self.coalignment_yn)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.selected_folder.setText(folder_path)

    def process_input(self):
        path = self.selected_folder.text() + '/'
        print('\nSelected folder is:', path)

        reference_identifier = self.reference_identifier_entry.text()
        print('\nReference file identifier is: ',reference_identifier)

        coalignment = self.coalignment_yn.isChecked()
        print('\nCo-alignment will be performed: ', coalignment)

        if os.path.isdir(path):
            print('\nFolder found. Starting registration...')
            try:
                f.registration_main(path, reference_identifier, coalignment)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
                print('\n')
                raise(e)
        else:
            print('\nNo such folder found!')

        self.close()

class MultiFolder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple folders registration")
        
        # Create a label and a text input field for the folder path list
        self.display1 = QLabel("Step1: \tInsert a list of paths to folders that need to be aligned. \n\tEach folder MUST be written in a new line. \n\tSpace or slash characters at the end of the folder will confuse the script!")
        self.display1b = QLabel("<i>/Users/admin/Desktop/20220216_P0001_E0008_U002</i>")
        self.display1b.setTextFormat(Qt.RichText)
        self.folders_list = QTextEdit()
        
        # Create a label and a text input field for the reference file identifier
        self.display2 = QLabel("\nStep2: \tSpecify the unique identifier of reference files")
        self.reference_identifier_entry = QLineEdit()

        # Create a checkbox for co-alignment
        self.display3 = QLabel("\nStep3: \tThe basename (the string preceeding the _) can be used to co-align files. ")
        self.coalignment_yn = QCheckBox("Co-align files with the same basename")

        # Create a button to process the input
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.process_input)

        # Create a button to quit
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.display1b)
        layout.addWidget(self.folders_list)
        layout.addWidget(self.display2)
        layout.addWidget(self.reference_identifier_entry)
        layout.addWidget(self.display3)
        layout.addWidget(self.coalignment_yn)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

    def process_input(self):
        folder_list_text = self.folders_list.toPlainText()
        folder_list = folder_list_text.split('\n')
        print('\nYou selected ', len(folder_list), 'folders. Selected folders are:')
        for folder in folder_list:
            print('\n\t', folder)

        reference_identifier = self.reference_identifier_entry.text()
        print('\nReference file identifier is: ',reference_identifier)

        coalignment = self.coalignment_yn.isChecked()
        print('\nCo-alignment will be performed: ', coalignment)

        #Iterate through individual folders
        #Check if the folder exists, 
        #   If folder exists, activate registration
        #   If folder does not exist, skip registration

        for folder in folder_list:    
            if os.path.isdir(folder):
                print('\nFound folder ', folder, '\nStarting registration...')
                path = folder + '/'
                try:
                    f.registration_main(path, reference_identifier, coalignment)
                except Exception as e:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText(str(e))
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    print('\n')
                    raise(e)
            else:
                print('\nUnable to locate folder ', folder, '\nMoving onto next folder...')

        print('\nAll folders have been registered!')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    param = ''
    try:
        param = sys.argv[1]
    except:
        print('\n')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('No parameter found')
        msg.setWindowTitle("Error")
        msg.show()
        sys.exit(app.exec_())
    else:
        if param == 'singleFile':
            form = SingleFile()
            form.move(260,0)
            form.show()
            sys.exit(app.exec_())
        elif param == 'singleFolder':
            form = SingleFolder()
            form.move(260,0)
            form.show()
            sys.exit(app.exec_())
        elif param == 'multiFolder':
            form = MultiFolder()
            form.move(260,0)
            form.show()
            sys.exit(app.exec_())

    sys.exit(app.exec_())