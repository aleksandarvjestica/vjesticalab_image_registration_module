import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QFrame, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import editing_functions as f
import general.general_functions as gf
import numpy as np

matplotlib.use("Qt5Agg")

class Single(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit single transformation matrix")

        # Create the widgets
        self.display1 = QLabel('Step1: \tSelect folder with transformation matrices')
        self.transfmat_path_edit = QLineEdit(self)                                 # Create line edit for the first variable              
        self.browse_button = QPushButton("Browse", clicked=self.browse_folder)

        self.display2 = QLabel('Step2: \tDouble click on the transformationMatrix to view and edit it.')        
        self.transf_mat_list = QListWidget()
        self.transf_mat_list.itemDoubleClicked.connect(self.transfMat_script)


        self.update_label = QLabel('<b>After double-clicking the matrix, you can update its range.<\b>', self)   # Create a label
        self.update_label.setTextFormat(Qt.RichText)
        
        self.start_timepoint_label = QLabel('Set new start point:', self)   # Create a label
        self.start_timepoint_edit = QLineEdit(self)                         # Create line edit for the second variable

        self.end_timepoint_label = QLabel('Set new end point:', self)   # Create a label
        self.end_timepoint_edit = QLineEdit(self)                       # Create line edit for the third variable

        self.submit_button = QPushButton('Update', self)            # Create a button to submit the chages to the transformation matrix
        #if self.transfmat_path: self.submit_button.clicked.connect(self.submit_values)      # Link submit button to action
        self.submit_button.clicked.connect(self.update_clicked)
        
        self.quit_button = QPushButton('Quit', self)    # Create a button to quit the interface
        self.quit_button.clicked.connect(self.close)    # Link quit button to action

        # Add a horizontal line to the layout
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.HLine)

        # Add the widgets to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.display1)
        layout.addWidget(self.transfmat_path_edit)
        layout.addWidget(self.browse_button)

        layout.addWidget(self.display2)
        layout.addWidget(self.transf_mat_list)
        layout.addWidget(self.quit_button)
        
        layout.addWidget(self.line1)
        
        layout.addWidget(self.update_label)
        layout.addWidget(self.start_timepoint_label)
        layout.addWidget(self.start_timepoint_edit)
        layout.addWidget(self.end_timepoint_label)
        layout.addWidget(self.end_timepoint_edit)
        layout.addWidget(self.submit_button)


        # Set the layout for the window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        self.transfmat_path_edit.setText(self.folder_path)

        transfMatFiles = gf.extract_transfMat(os.listdir(self.folder_path))
        for file in transfMatFiles:
            self.transf_mat_list.addItem(file)      
               
    def update_clicked(self):
        try:
            self.transfmat_path
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No values')
            msg.setWindowTitle("Error")
            msg.show()
            print('\n')
            raise(e)
        else:
            print('\nUpdating plot')
            self.submit_values()        

    def transfMat_script(self, item):
        transformation_mat_name = item.text() #name of selected transformation matrix is passed to the variable    
        transformation_mat_path = os.path.join(self.folder_path, transformation_mat_name)

        #This is bad coding. Please fix it if you know how
        self.transfMat_name = transformation_mat_name
        self.transfmat_path = transformation_mat_path
        print('\nMatrix plotted: ', self.transfMat_name)

        self.display_graph = DisplayGraphWindow(self.transfmat_path)
        self.display_graph.setWindowTitle(self.transfMat_name)
        self.display_graph.move(700,0)
        self.display_graph.show()

    def submit_values(self):
        # This function defines the actions of the "Submit" button
        # Get the values from the line edits
        
        start_timepoint = self.start_timepoint_edit.text()
        end_timepoint = self.end_timepoint_edit.text()        
        
        # Update the transformation matrix with indicated values
        print('\nMatrix path that will be edited: ', self.transfmat_path)
        f.edit_main(self.transfmat_path, int(start_timepoint), int(start_timepoint), int(end_timepoint))
        
        # Create an instance of the second window
        self.display_graph = DisplayGraphWindow(self.transfmat_path)
        self.display_graph.setWindowTitle(self.transfMat_name)
        self.display_graph.move(700,0)
        self.display_graph.show()

class Folder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit folder of transformation matrices")

        # Create a label and line edit for the first variable
        self.self.transfmat_path_label = QLabel('Select the transformation matrix:', self)
        self.self.transfmat_path_edit = QLineEdit(self)
        
        # Create the browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)

        # Create the list widget to display the files
        self.list_widget_label = QLabel('Registration matrices that will be modified:', self)
        self.list_widget = QListWidget()
        
        # Create a label and line edit for the second variable
        self.start_timepoint_label = QLabel('Set new start point:', self)
        self.start_timepoint_edit = QLineEdit(self)

        # Create a label and line edit for the third variable
        self.end_timepoint_label = QLabel('Set new end point:', self)
        self.end_timepoint_edit = QLineEdit(self)

        # Create a button to submit the values
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_values)
        
        # Create a button to quit the application
        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.close)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.self.transfmat_path_label)
        layout.addWidget(self.self.transfmat_path_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.list_widget_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.start_timepoint_label)
        layout.addWidget(self.start_timepoint_edit)
        layout.addWidget(self.end_timepoint_label)
        layout.addWidget(self.end_timepoint_edit)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.quit_button)
        
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def submit_values(self):
        # Get the values from the line edits
        self.transfmat_path = self.self.transfmat_path_edit.text()
        start_timepoint = self.start_timepoint_edit.text()
        end_timepoint = self.end_timepoint_edit.text()        
        
        #Get the list of files that end with _transformationMatrix.txt
        list_transfmat_files = gf.list_transfMat(self.transfmat_path)
        for transfmat in list_transfmat_files:
            transfmat_filepath=self.transfmat_path+'/'+transfmat
            f.edit_main(transfmat_filepath, int(start_timepoint), int(start_timepoint), int(end_timepoint))        
            print('\nUpdated file: ', transfmat)

    def browse(self):
        # Open a file dialog to select the folder
        folder = QFileDialog.getExistingDirectory()
        self.self.transfmat_path_edit.setText(folder)

        # Clear the list widget
        self.list_widget.clear()
        
        #Get the list of transformation matrices in the selected folder
        list_transfmat_files = gf.list_transfMat(folder)

        # Add the transformation matrices files in the selected folder to the list widget
        for file in list_transfmat_files:
            self.list_widget.addItem(file)       
        self.list_widget.sortItems(order=Qt.AscendingOrder)
       
class DisplayGraphWindow(QWidget):
    def __init__(self, transfmat_path):
        super().__init__()
        
        # Create labels to display the values of the variables   
        self.plot_xy(transfmat_path)
                
        # Create a vertical layout to hold the widgets
        layout = QVBoxLayout()
        widget_graph = QWidget(self)
        widget_graph.setLayout(layout)
                
    def plot_xy(self, transfmat_path):
        #Read the transformation matrix values
        transformation_matrix = gf.read_transfMat(transfmat_path)
        
        if transformation_matrix is None:
            return
        #Read the variables from the transformation matrix
        time = list(transformation_matrix[:,0])
        included_x_shift = transformation_matrix[:,1]
        included_y_shift = transformation_matrix[:,2]
        inclusion = transformation_matrix[:,3]
        x_shift = transformation_matrix[:,4]
        y_shift = transformation_matrix[:,5]
        dim_x = transformation_matrix[:,6]
        dim_y = transformation_matrix[:,7]
        dx = dim_x - abs(x_shift)
        dy = dim_y - abs(y_shift)
        included_dx = dim_x - abs(included_x_shift)
        included_dy = dim_y - abs(included_y_shift)

        included_xy_shift = []
        xy_shift = []
        included_xy_shift = []

        for i in range(len(time)):
            distance = np.sqrt((dim_x[i]**2 - dx[i]**2) + (dim_y[i]**2 - dy[i]**2)) # √(x² - dx²) + (y² - dy²))
            if inclusion[i] == 1:
                included_distance = np.sqrt((dim_x[i]**2 - included_dx[i]**2) + (dim_y[i]**2 - included_dy[i]**2)) # √(x² - dx²) + (y² - dy²))
            else:
                included_distance = float("nan")
            max_distance = np.sqrt((dim_x[i]**2) + (dim_y[i]**2))
            #dev = abs(float(line.split(',')[1])) * abs(float(line.split(',')[2])) # |t_x| * |t_y|
            xy_shift.append((max_distance-distance)/max_distance)
            included_xy_shift.append((max_distance-included_distance)/max_distance)
        
        # Create a figure and a canvas
        figure = Figure()
        canvas = FigureCanvas(figure)

        # Create a subplot
        ax = figure.add_subplot(111)

        # Plot the data
        ax.plot(time, xy_shift, label='All timepoints')
        ax.plot(time, included_xy_shift, label='Selected timepoints')
        ax.legend()
                
        # Add a title and labels for the axes
        ax.set_title('Offset')
        ax.set_xlabel('timepoints')
        ax.set_ylabel('offset values')
                
        # Add the canvas to the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(canvas)
            

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
        if param == 'single':
            form = Single()
            form.move(260,0)
            form.show()
        elif param == 'folder':
            form = Folder()
            form.move(260,0)
            form.show()

    sys.exit(app.exec_())
