import os
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QFileDialog, QVBoxLayout, QWidget, QLineEdit, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
import alignment_functions as f
import napari
import general.general_functions as gf


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Files alignment with matrices")

        # Create the widgets
        self.display1 = QLabel('<b>Step1:</b> Select folder')    
        self.display1.setTextFormat(Qt.RichText)
        self.selected_folder = QLineEdit()         
        self.browse_button = QPushButton("Browse", clicked=self.browse_folder)

        self.display2 = QLabel('<b>Step2:</b> Double click on the image file to have it registered if matrix is available.')        
        self.display2.setTextFormat(Qt.RichText)
        
        self.images_list = QListWidget()
        self.images_list.itemDoubleClicked.connect(self.image_script)

        # Create a label and a checkbox for the decision to crop
        self.display3 = QLabel("\nNote that cropping is performed by default. Checkbox to skip cropping.")
        self.skip_cropping_yn = QCheckBox("Do NOT crop aligned image")

        # Create a button to quit
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.selected_folder)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.display2)
        layout.addWidget(self.images_list)
        layout.addWidget(self.display3)
        layout.addWidget(self.skip_cropping_yn)
        layout.addWidget(self.quit_button)

        # Set the layout for the window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.selected_folder.setText(self.folder_path)
        self.images_list.clear()
        
        
        imageFiles = gf.extract_suitable_files(os.listdir(self.folder_path))
        for file in imageFiles:
            self.images_list.addItem(file)

        #Build two file inventories: 
        # one for each file that stores the transformation matrix   

        # !!!!!! ARIANNA MODIF adding folder of the txt files
        # lets do that with pathsInventory then!!
        # before:   self.imageFile_inventory = gf.build_dictionary(self.folder_path, 'imageFile')clea
        self.imageFile_inventory = gf.build_dictionary(self.folder_path, 'imageFile')


    def image_script(self, item):
        imageFile_single = item.text()
        imageFile_single_path = os.path.join(self.folder_path,imageFile_single)
        if len(self.imageFile_inventory[imageFile_single])<1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No transformation matrix available')
            msg.setWindowTitle("Error")
            msg.show()
            print('\nNo transformation matrix available')
        
        else:  
            # Pass the transformation matrix and files to the script to align them
            skip_crop_decision = self.skip_cropping_yn.isChecked()                        
            transfMat_name = self.imageFile_inventory[imageFile_single][0]
            transfMat_single_path=os.path.join(self.folder_path,transfMat_name)
            #Open transformation mat and open imagefile
            transfMat_load = gf.read_transfMat(transfMat_single_path)
            image_load, axes_inventory = gf.open_suitable_files(imageFile_single_path)
            # eg. axes_inventory = {'T': [0, 120], 'Z': [1, 3], 'C': [2, 2], 'Y': [3, 275], 'X': [4, 390]}
            if 'C' in axes_inventory.keys() and 'Z' in axes_inventory.keys():
                for c in range(axes_inventory['C'][1]):
                    for z in range(axes_inventory['Z'][1]):
                        image_registered = gf.register_with_tmat_multiD(transfMat_load, image_load[:,z,c,:,:], 1,2, skip_decision=skip_crop_decision) 
                viewer = napari.Viewer()
                for c in range(axes_inventory['C'][1]):
                    # add channels one by one
                    viewer.add_image(image_load[:,:,c,:,:], name="Channel "+str(c), blending="additive")
            elif 'C' in axes_inventory.keys():
                for c in range(axes_inventory['C'][1]):
                    image_registered = gf.register_with_tmat_multiD(transfMat_load, image_load[:,c,:,:], 1,2, skip_decision=skip_crop_decision) 
                viewer = napari.Viewer()
                for c in range(axes_inventory['C'][1]):
                    # add channels one by one
                    viewer.add_image(image_load[:,:,c,:,:], name="Channel "+str(c), blending="additive")
            elif 'Z' in axes_inventory.keys():
                for z in range(axes_inventory['Z'][1]):
                    image_registered = gf.register_with_tmat_multiD(transfMat_load, image_load[:,z,:,:], 1,2, skip_decision=skip_crop_decision)    
                viewer = napari.view_image(image_registered)    
            else:
                image_registered = gf.register_with_tmat_multiD(transfMat_load, image_load, 1,2, skip_decision=skip_crop_decision) 
                viewer = napari.view_image(image_registered)

class SingleFile(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Files alignment with matrices")

        # Create the widgets
        self.display1 = QLabel('Step1: \tSelect folder')    
        self.selected_folder = QLineEdit()         
        self.browse_button = QPushButton("Browse", clicked=self.browse_folder)

        self.display2 = QLabel('<b>Option A:</b> Double click on the image file to have it registered if matrix is available.')        
        self.display2.setTextFormat(Qt.RichText)
        
        self.images_list = QListWidget()
        self.images_list.itemDoubleClicked.connect(self.image_script)

        self.display3 = QLabel('<b>Option B:</b> Double click on transformationMatrix to register all files with the same basename.')        
        self.display3.setTextFormat(Qt.RichText)
        self.transf_mat_list = QListWidget()
        self.transf_mat_list.itemDoubleClicked.connect(self.transfMat_script)

        # Create a label and a checkbox for the decision to crop
        self.display4 = QLabel("\nNote that cropping is performed by default. Checkbox to skip cropping.")
        self.skip_cropping_yn = QCheckBox("Do NOT crop aligned image")

        # Create a button to quit
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.selected_folder)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.display2)
        layout.addWidget(self.images_list)
        layout.addWidget(self.display3)
        layout.addWidget(self.transf_mat_list)
        layout.addWidget(self.display4)
        layout.addWidget(self.skip_cropping_yn)       
        layout.addWidget(self.quit_button)

        # Set the layout for the window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.selected_folder.setText(self.folder_path)
        self.images_list.clear()
        self.transf_mat_list.clear()
        
        imageFiles = gf.extract_suitable_files(os.listdir(self.folder_path))
        for file in imageFiles:
            self.images_list.addItem(file)

        transfMatFiles = gf.extract_transfMat(os.listdir(self.folder_path))
        for file in transfMatFiles:
            self.transf_mat_list.addItem(file)        

        #Build two file inventories: 
        # one for each transformation matrix key
        # one for each file that stores the transformation matrix   
        
        self.transfMat_inventory = gf.build_dictionary(self.folder_path, 'transfMat')
        
        self.imageFile_inventory = gf.build_dictionary(self.folder_path, 'imageFile')


    def image_script(self, item):
        imageFile_single = item.text()
        if len(self.imageFile_inventory[imageFile_single]) < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No transformation matrix available')
            msg.setWindowTitle("Error")
            msg.show()
            print('\nNo transformation matrix available')
        
        else:  
            # Pass the transformation matrix and files to the script to align them
            skip_crop_decision = self.skip_cropping_yn.isChecked()
            transfMat_name = self.imageFile_inventory[imageFile_single][0]
            current_inventory={}
            current_inventory[transfMat_name]= [imageFile_single]
            print('\nCurrent inventory:', current_inventory, skip_crop_decision)
            f.registration_main(self.folder_path+'/', current_inventory, skip_crop_decision)

    def transfMat_script(self, item):
        skip_crop_decision = self.skip_cropping_yn.isChecked()
        transfMat_name = item.text()
        imageFiles_list =self.transfMat_inventory[transfMat_name]      
        # Pass the transformation matrix and files to the script to align them
        current_inventory={}
        current_inventory[transfMat_name]= imageFiles_list
        print('\nCurrent inventory:', current_inventory, skip_crop_decision)
        f.registration_main(self.folder_path+'/', current_inventory, skip_crop_decision)

class SingleFolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Form")

        # Create the widgets
        self.display1 = QLabel("Step1: Select folder to process")
        self.selected_folder = QLineEdit()
        self.browse_button = QPushButton("Browse", clicked=self.browse_folder)
        self.submit_button = QPushButton("Submit", clicked=self.process_input)

        # Create a label and a checkbox for the decision to crop
        self.display2 = QLabel("\nNote that cropping is performed by default. Checkbox to skip cropping.")
        self.skip_cropping_yn = QCheckBox("Do NOT crop aligned image")


        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.selected_folder)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.display2)
        layout.addWidget(self.skip_cropping_yn) 
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)
        
        # Set the layout for the window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Create a function to open a file browser and store the selected file's path
    def browse_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.selected_folder.setText(self.folder_path)

    # Create a function to process the input
    def process_input(self):
        skip_crop_decision = self.skip_cropping_yn.isChecked()
        path = self.selected_folder.text() + '/'
        print('\nSelected folder is:', path)

        if os.path.isdir(path):
            print('\nFolder found. Starting registration...')
            f.registration_main(path, '', skip_crop_decision)
        else:
            print('\nNo such folder found!')

class MultiFolder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple folders alignment with matrices")

        # Create a label and a text input field for the folder path list
        self.display1 = QLabel("Step1: \tInsert a list of paths to folders that need to be aligned. \n\tEach folder MUST be written in a new line. \n\tSpace or slash characters at the end of the folder will confuse the script!")
        self.display1b = QLabel("<i>/Users/admin/Desktop/20220216_P0001_E0008_U002</i>")
        self.display1b.setTextFormat(Qt.RichText)
        self.folders_list = QTextEdit()

        # Create a label and a checkbox for the decision to crop
        self.display2 = QLabel("\nNote that cropping is performed by default. Checkbox to skip cropping.")
        self.skip_cropping_yn = QCheckBox("Do NOT crop aligned image")

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
        layout.addWidget(self.skip_cropping_yn) 
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

    def process_input(self):
        skip_crop_decision = self.skip_cropping_yn.isChecked()
        folder_list_text = self.folders_list.toPlainText()
        folder_list = folder_list_text.split('\n')
        print('\nYou selected ', len(folder_list), 'folders. Selected folders are:')
        for folder in folder_list:
            print('\n\t', folder)

        #Iterate through individual folders
        #Check if the folder exists, 
        #   If folder exists, activate alignment
        #   If folder does not exist, skip registration

        for folder in folder_list:    
            if os.path.isdir(folder):
                print('\nFound folder ', folder, '\nStarting registration...')
                path = folder + '/'
                f.registration_main(path, '', skip_crop_decision)
            else:
                print('\nUnable to locate folder ', folder, '\nMoving onto next folder...')

        print('\nAll folders have been aligned!')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    param = ''
    try:
        param = sys.argv[1]
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('No parameter found')
        msg.setWindowTitle("Error")
        msg.show()
        sys.exit(app.exec_())
    else:
        if param == 'view':
            form = View()
            form.move(260,0)
            form.show()
        elif param == 'singleFile':
            form = SingleFile()
            form.move(260,0)
            form.show()
        elif param == 'singleFolder':
            form = SingleFolder()
            form.move(260,0)
            form.show()
        elif param == 'multiFolder':
            form = MultiFolder()
            form.move(260,0)
            form.show()

    sys.exit(app.exec_())