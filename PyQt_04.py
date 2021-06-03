import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(200, 200, 1200, 420)
        self.setWindowTitle("Projectile Calculator v0.1")
        self.setFixedSize(1200, 420)

        self.statusBar().showMessage('장애물을 맞추세요.')

        self.label_velocity = QLabel("Velocity: ", self)
        self.label_velocity.move(0,0)
        self.lineEdit_velocity = QLineEdit("20", self)
        self.lineEdit_velocity.move(60, 0)
        self.pushButton = QPushButton("포탄 날리기", self)
        self.pushButton.move(0, 30)
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.lbl_img = QLabel(self)
        self.lbl_img.move(700,70)
        self.pixmap = QPixmap('image.png')
        self.pixmap = self.pixmap.scaledToHeight(300)
        self.lbl_img.setPixmap(self.pixmap)
        self.lbl_img.setFixedSize(self.pixmap.size())

    def pushButtonClicked(self):
        velocity = float(self.lineEdit_velocity.text())
        text = '펑!하고 포탄이' + str(velocity) + '의 속도로 날아갑니다.'
        self.statusBar().showMessage(text)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp, 4, 5, 20, 20)
        qp.end()

    def draw_point(self, qp, _x, _y, _obs_x, _obs_y):
        qp.setPen(QPen(Qt.black, 2))
        qp.drawLine(0, 370, 700, 370)

        _x = int(_x * 5)
        _y = 370 - int(_y * 5)
        qp.setPen(QPen(Qt.blue, 8))
        qp.drawPoint(_x, _y)

        _obs_x = int(_obs_x * 5)
        _obs_y = 370 - int(_obs_y * 5)
        qp.setPen(QPen(Qt.red, 15))
        qp.drawPoint(_obs_x, _obs_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()