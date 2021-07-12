import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect, Qt

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
on = True


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        destopSize = QDesktopWidget().screenGeometry()
        w, h = destopSize.width(), destopSize.height()
        self.setGeometry(w / 2 - 300, h / 2 - 250, 700, 500)
        self.setWindowTitle("Face Detection of Huy")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabImage = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tabImage, "Image")

        # Create TAB IMAGE
        # Create textbox to get path of image
        self.imagePathI = QLineEdit(self.tabImage)
        self.imagePathI.setGeometry(QRect(20, 30, 450, 30))

        # Create load Button to load image
        self.loadButtonI = QPushButton("Load", self.tabImage)
        self.loadButtonI.setGeometry(QRect(500, 30, 100, 30))
        self.loadButtonI.clicked.connect(self.loadImage)

        # Create box to show image
        self.imageView = QGraphicsView(self.tabImage)
        self.imageView.setGeometry(QRect(20, 80, 450, 360))

        # Create form to get parametes
        self.scaleLabelI = QLabel("Scale Factor:", self.tabImage)
        self.scaleLabelI.setGeometry(QRect(500, 200, 100, 30))
        self.scaleSpinBoxI = QDoubleSpinBox(self.tabImage)
        self.scaleSpinBoxI.setGeometry(QRect(600, 200, 50, 30))
        self.scaleSpinBoxI.setDecimals(1)
        self.scaleSpinBoxI.setMinimum(1.1)
        self.scaleSpinBoxI.setMaximum(2.0)
        self.scaleSpinBoxI.setSingleStep(0.1)

        self.MinNeighborLabelI = QLabel("Min Neighbor:", self.tabImage)
        self.MinNeighborLabelI.setGeometry(QRect(500, 300, 100, 30))
        self.minNeighborSpinBoxI = QSpinBox(self.tabImage)
        self.minNeighborSpinBoxI.setGeometry(QRect(600, 300, 50, 30))
        self.minNeighborSpinBoxI.setMinimum(1)
        self.minNeighborSpinBoxI.setMaximum(50)

        # Create button to Detect
        self.detectButtonI = QPushButton("Detect", self.tabImage)
        self.detectButtonI.setGeometry(QRect(550, 400, 100, 30))
        self.detectButtonI.clicked.connect(self.detectOfImage)
        # END IMAGE TAB

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def loadImage(self):
        dialog = QFileDialog()
        folder_path, _ = dialog.getOpenFileName(options=QFileDialog.Options())
        self.imagePathI.setText(folder_path)
        image_reader = QImageReader(self.imagePathI.text())
        print(folder_path)
        if image_reader.canRead() is True:
            widget_height = self.imageView.height()
            widget_width = self.imageView.width()
            image = image_reader.read().scaled(widget_width, widget_height, Qt.KeepAspectRatio)
            item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            scene = QGraphicsScene()
            scene.addItem(item)
            self.imageView.setScene(scene)
        else:
            scene = QGraphicsScene()
            self.imageView.setScene(scene)

    def detectOfImage(self):
        path = self.imagePathI.text()
        s = self.scaleSpinBoxI.value()
        m = self.minNeighborSpinBoxI.value()
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, s, m)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imwrite('result.png', img)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # self.detect_face(path,"a",s,m)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
