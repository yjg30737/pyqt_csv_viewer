import pandas as pd
import numpy as np

from PyQt5.QtCore import QSortFilterProxyModel, Qt, QCollator
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QVBoxLayout, QWidget, \
    QStyledItemDelegate, QAbstractItemView, QHBoxLayout, QComboBox, QLabel, QSizePolicy, QTableView

from instantSearchBar import InstantSearchBar


class NumericSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.collator = QCollator()
        self.collator.setNumericMode(True)
        self.collator.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def lessThan(self, left, right):
        leftData = self.sourceModel().data(left)
        rightData = self.sourceModel().data(right)

        # Check if the data is numeric
        if isinstance(leftData, (int, float, np.float64)) and isinstance(rightData, (int, float, np.float64)):
            return leftData < rightData
        # Check if the data is a string that can be converted to a number
        elif isinstance(leftData, str) and isinstance(rightData, str) and leftData.isdigit() and rightData.isdigit():
            return int(leftData) < int(rightData)
        # Compare the data as strings
        else:
            # Convert the data to strings if they are not already strings
            leftData = str(leftData) if not isinstance(leftData, str) else leftData
            rightData = str(rightData) if not isinstance(rightData, str) else rightData
            return self.collator.compare(leftData, rightData) < 0


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class CSVViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('CSV & Excel Viewer')

        self.__tableWidget = QTableView()

        self.__tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # init the proxy model
        self.__proxyModel = NumericSortFilterProxyModel()

        # set the table model as source model to make it enable to feature sort and filter function
        self.__tableWidget.setModel(self.__proxyModel)

        # sort (ascending order by default)
        self.__tableWidget.setSortingEnabled(True)
        self.__tableWidget.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        # instant search bar
        self.__searchBar = InstantSearchBar()
        self.__searchBar.setPlaceHolder('Search...')
        self.__searchBar.searched.connect(self.__showResult)

        # combo box to make it enable to search by each column
        self.__comboBox = QComboBox()
        self.__comboBox.currentIndexChanged.connect(self.__currentIndexChanged)
        items = ['All']
        self.__initComboBox(items)

        # set layout
        lay = QHBoxLayout()
        lay.addWidget(QLabel('Navigation Bar'))
        lay.addWidget(self.__searchBar)
        lay.addWidget(self.__comboBox)
        lay.setContentsMargins(0, 0, 0, 0)
        btnWidget = QWidget()
        btnWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(btnWidget)
        lay.addWidget(self.__tableWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)

        # show default result (which means "show all")
        self.__showResult('')

    def __initComboBox(self, items):
        self.__comboBox.clear()
        for i in range(len(items)):
            self.__comboBox.addItem(items[i])
        # Stretch combo box to fill the remaining space
        self.__comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def loadCSV(self, file_path):
        # Check extension
        df = ''
        if file_path.endswith('.csv'):
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(file_path)
        else:
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(file_path)

        column_names = list(map(str, df.columns.tolist()))
        num_rows, num_columns = df.shape

        # Initialize the model with rows and columns
        self.__model = QStandardItemModel(num_rows, num_columns)

        # Populate the model with data
        for row_idx in range(num_rows):
            for col_idx in range(num_columns):
                item = QStandardItem(str(df.iloc[row_idx, col_idx]))
                self.__model.setItem(row_idx, col_idx, item)

        # Set the model to the proxy model
        self.__proxyModel.setSourceModel(self.__model)

        # Initialize the combo box with column names
        items = ['All'] + column_names
        self.__initComboBox(items)

        # Set the column names as headers
        self.__model.setHorizontalHeaderLabels(column_names)

        # align to center
        delegate = AlignDelegate()
        for i in range(self.__tableWidget.model().columnCount()):
            self.__tableWidget.setItemDelegateForColumn(i, delegate)

        # Resize columns to content
        self.__tableWidget.resizeColumnsToContents()

    def __showResult(self, text):
        # index -1 will be read from all columns
        # otherwise it will be read the current column number indicated by combobox
        self.__proxyModel.setFilterKeyColumn(self.__comboBox.currentIndex()-1)
        # regular expression can be used
        self.__proxyModel.setFilterRegularExpression(text)

    def __currentIndexChanged(self, idx):
        self.__showResult(self.__searchBar.getSearchBar().text())
