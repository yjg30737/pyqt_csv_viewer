import os, sys

# Get the absolute path of the current script file
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont

from csvViewer import CSVViewer
from findPathWidget import FindPathWidget

script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QListWidget, QSplitter, QWidget, \
    QLabel, QFrame

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('CSV Viewer')

        findPathWidget = FindPathWidget()
        findPathWidget.setAsDirectory(True)
        findPathWidget.getLineEdit().setPlaceholderText('Select The Folder')
        findPathWidget.added.connect(self.__addList)

        self.__listWidget = QListWidget()
        self.__listWidget.itemActivated.connect(self.__showContent)
        self.__listWidget.itemClicked.connect(self.__showContent)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        lay = QVBoxLayout()
        lay.addWidget(findPathWidget)
        lay.addWidget(sep)
        lay.addWidget(QLabel('File List'))
        lay.addWidget(self.__listWidget)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        self.__csvViewer = CSVViewer()

        lay = QVBoxLayout()
        lay.addWidget(QLabel('CSV Window'))
        lay.addWidget(self.__csvViewer)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        splitter = QSplitter()
        splitter.addWidget(leftWidget)
        splitter.addWidget(rightWidget)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([300, 700])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")

        self.setCentralWidget(splitter)

    def __addList(self, dirname):
        filenames = [os.path.join(dirname, filename) for filename in os.listdir(dirname) if os.path.splitext(filename)[-1] == '.csv']
        self.__listWidget.addItems(filenames)

    def __showContent(self, item):
        if item:
            csv_f = item.text()
            self.__csvViewer.loadCSV(csv_f)

    def __run(self):
        pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())