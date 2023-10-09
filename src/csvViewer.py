import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class CSVViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV Viewer')

        lay = QVBoxLayout()
        self.__tableWidget = QTableWidget()
        lay.addWidget(self.__tableWidget)
        self.setLayout(lay)

    def loadCSV(self, file_path):
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        column_names = df.columns.tolist()

        # Get the number of rows and columns
        num_rows, num_columns = df.shape

        # Set the number of rows and columns for the table
        self.__tableWidget.setRowCount(num_rows)
        self.__tableWidget.setColumnCount(num_columns)

        # Populate the table with data
        for row_idx, row_data in df.iterrows():
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                self.__tableWidget.setItem(row_idx, col_idx, item)

        # Set the column names as headers
        self.__tableWidget.setHorizontalHeaderLabels(column_names)

        # Resize columns to content
        self.__tableWidget.resizeColumnsToContents()