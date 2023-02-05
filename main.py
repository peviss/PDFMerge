import hashlib
import random
import sys
import os
from PIL import Image
import PyPDF2
from PyQt5 import QtWidgets

class MergeWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the "Merge" button
        self.merge_button = QtWidgets.QPushButton('Merge', self)
        self.merge_button.clicked.connect(self.merge)

        # Create the output filename text field
        self.output_text = QtWidgets.QLineEdit(self)
        self.output_text.setPlaceholderText('Output filename')

        # Create the file list widget
        self.file_list = QtWidgets.QListWidget(self)
        self.file_list.setAcceptDrops(True)
        self.file_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # Delete button
        self.delete_button = QtWidgets.QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.delete_selected)

        self.setAcceptDrops(True)

        # Set up the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.output_text)
        layout.addWidget(self.file_list)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.merge_button)

    def merge(self):
        # Get the output filename from the text field
        output_filename = self.output_text.text() if '.pdf' in self.output_text.text() else f'{self.output_text.text()}.pdf'

        # Get the list of selected filenames
        filenames = [self.file_list.item(i).text() for i in range(self.file_list.count())]

        # Create a PDF merger object
        merger = PyPDF2.PdfMerger()

        # Loop through all the filenames
        for filename in filenames:
            # Check if the file is a PDF or an image
            if filename.lower().endswith(('.pdf')):
                # Open the PDF file
                with open(filename, 'rb') as f:
                    # Add the PDF to the merger
                    merger.append(f)
            else:
                # Open the image
                with Image.open(filename) as im:
                    # Convert the image to PDF
                    rgb = im.convert('RGB')
                    # Create a PDF from image
                    dirname = os.path.dirname(filename)
                    rgb_filename = os.path.join(dirname, self.generate_random_id() + '.pdf')
                    rgb.save(rgb_filename)
                    # Add the PDF to the merger
                    with open(rgb_filename, 'rb') as f:
                        merger.append(f)
                    os.remove(rgb_filename)

        # Write the combined PDF to a file
        try:
            with open(output_filename, 'wb') as f:
                merger.write(f)
            # Show a message box indicating that the PDF was created
            QtWidgets.QMessageBox.information(self, 'PDF Created', 'The PDF was created successfully!')
        except:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Error merging PDF')

    def dragEnterEvent(self, event):
        # Allow files to be dropped onto the widget
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Add the dropped files to the file list
        for url in event.mimeData().urls():
            self.file_list.addItem(url.toLocalFile())
    
    def delete_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
    
    def generate_random_id(self):
        # Create a random number
        random_number = random.randint(1000000000, 9999999999)
        # Convert the number to a string
        random_string = str(random_number)
        # Create a hash of the string using sha1
        return hashlib.sha1(random_string.encode()).hexdigest()[:11]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MergeWindow()
    window.show()
    sys.exit(app.exec_())

