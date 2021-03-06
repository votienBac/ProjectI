 

# Form implementation generated from reading ui file 'HDRapp.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

import cv2
import joblib
from skimage.feature import hog
import numpy as np
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QImage,  QPixmap
from PyQt5.QtWidgets import ( QApplication, QPushButton, QFileDialog, QLabel,
                             QMainWindow,  QScrollArea, QLineEdit)


class Ui_Dialog(QMainWindow):

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.fileName = ""
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.scrollArea = QScrollArea()

        self.scrollArea.setWidget(self.imageLabel)

        self.setCentralWidget(self.scrollArea)



        #creation of  button for select
        self.button = QPushButton('select', self)
        self.button.move(200, 500)
        self.button.clicked.connect(self.on_click1)
        self.button.setStyleSheet("background-color: yellow")


        #creation of  button for predict
        self.button2 = QPushButton('predict', self)
        self.button2.move(800, 500)
        self.button2.clicked.connect(self.on_click2)
        self.button2.setStyleSheet("background-color: red")


        #creation of textbox for displaying output
        self.textbox = QLineEdit(self)
        self.textbox.move(800, 20)
        self.textbox.resize(880, 400)



        self.setWindowTitle("HANDWRITTEN DIGIT RECOGNITION app")
        self.resize(1400, 600)

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

    def on_click1(self):

        #for opening a file dialog Box to browse the image file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "All Files (*);;Python Files (*.py)", options=options)

        print(self.fileName)
        image = QImage(self.fileName)

        #set the image on the image label
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.scaleFactor = 1.0
        self.imageLabel.adjustSize()

    def on_click2(self):


        # t???i model
        clf = joblib.load("digits_cls.pkl")

        # ?????c h??nh ???nh ?????u v??o
        im = cv2.imread(self.fileName)

        # chuy???n h??nh ???nh sang grayscale v?? ??p d???ng b??? l???c GaussianBlur
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

        # nh??? ph??n ho?? h??nh ???nh 
        ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(im_th, kernel, iterations=1)
        #l??m n???i b???t c??c ???????ng vi???n t????ng ph???n
        edged = cv2.Canny(dilation, 50, 250)
        # t??m ???????ng bao tr??n ???nh
        ctrs, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # l???y h??nh ch??? nh???t m???i ???????ng bao
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]
        ll = []

        for rect in rects:
           

            cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 3)
           
            leng = int(rect[3])
            pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
            pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
            roi = im_th[pt1:pt1 + leng, pt2:pt2 + leng]
            # ch???nh s???a l???i k??ch th?????c ???nh
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))
            # t??nh HOG features
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualize=False)

            
            nbr = clf.predict(np.array([roi_hog_fd], 'float64'))


            
            cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 3)


            print(nbr, type(nbr), nbr.shape)
            
            a = nbr.tolist()[0]

            
            ll.append(a)


        print(ll)

        #converting the list to string
        string = ''.join(map(str, ll))
        print(string)

        from PIL import Image

        #converting the numpy array to image
        img = Image.fromarray(im, 'RGB')
        print(img)
        img.show()

        #displaying output string in the textbox widget
        self.textbox.setText(string)
        f = self.textbox.font()
        f.setPointSize(90)  # sets the size to 90
        self.textbox.setFont(f)


if __name__ == '__main__':
    import sys

    # PyQt5 application must create an application object. The sys.argv parameter is a list of arguments from a command line
    # This calls the constructor of the C++ class QApplication. It uses sys.argv  to initialize the QT application
    app = QApplication(sys.argv)
    hdrappobj = Ui_Dialog()
    hdrappobj.show()

    sys.exit(app.exec_())