import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        self.central_widget.setLayout(layout)

    def loadCSV(self, file_path):
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        column_names = df.columns.tolist()

        # Get the number of rows and columns
        num_rows, num_columns = df.shape

        # Set the number of rows and columns for the table
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_columns)

        # Populate the table with data
        for row_idx, row_data in df.iterrows():
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                self.table_widget.setItem(row_idx, col_idx, item)

        # Set the column names as headers
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # Resize columns to content
        self.table_widget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CSVViewer()
    window.loadCSV('./data/pima-indians-diabetes3.csv')  # Replace 'your_csv_file.csv' with your CSV file path
    window.show()
    sys.exit(app.exec_())
