import sys
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from PyQt5.QtCore import Qt

#테트삼아 수정합니다.
#테스트삼아 또 수정 합니다.

def save_csv(_vel, _ang, _listX, _listY):
    outFp = open("C:/Temp/ProjectileMotion.csv", "w")
    temp = "속도," + str(_vel) + ",\n"
    outFp.writelines(temp)
    temp = "각도," + str(_ang) + ",\n"
    outFp.writelines(temp)
    outFp.writelines("시간,x좌표,y좌표\n")

    for i in range(len(_listX)):
        t = i * 0.05
        temp = str(t) + ',' + str(_listX[i]) + ',' + str(_listY[i]) + '\n'
        outFp.writelines(temp)
    outFp.close()


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.projectile_x = 0
        self.projectile_y = 0
        self.obstacle_x = 20
        self.obstacle_y = 20
        #2
        self.list_x = []
        self.list_y = []
        self.angle = 0
        self.velocity = 0

    def setupUI(self):
        self.setGeometry(200, 200, 1200, 500)
        self.setWindowTitle("Projectile Calculator v0.1")
        self.setWindowIcon(QIcon('web.png'))
        self.setFixedSize(1200, 420)

        self.statusBar().showMessage('장애물을 맞추세요.')

        # Left Layout componemt

        # Left Layout Alignment
        leftLayout = QVBoxLayout()

        # Right Layout componemt
        self.label_velocity = QLabel("Velocity: ")
        self.lineEdit_velocity = QLineEdit("20")
        self.label_angle = QLabel("Angle: ")
        self.lineEdit_angle = QLineEdit("45")
        self.label_obstacle_x = QLabel("Obstacle_x: ")
        self.lineEdit_obsX = QLineEdit("20")
        self.label_obstacle_y = QLabel("Obstacle_y: ")
        self.lineEdit_obsY = QLineEdit("20")
        self.pushButton = QPushButton("포탄 날리기")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.saveButton = QPushButton("파일로 저장")
        self.saveButton.clicked.connect(self.saveButtonClicked)

        pixmap = QPixmap('image.png')
        pixmap = pixmap.scaledToHeight(300)
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)

        # Right Layout Alignment
        inputBoxlayout1 = QHBoxLayout()

        inputBoxlayout1.addWidget(self.label_velocity)
        inputBoxlayout1.addWidget(self.lineEdit_velocity)
        inputBoxlayout1.addWidget(self.label_angle)
        inputBoxlayout1.addWidget(self.lineEdit_angle)

        inputBoxlayout2 = QHBoxLayout()

        inputBoxlayout2.addWidget(self.label_obstacle_x)
        inputBoxlayout2.addWidget(self.lineEdit_obsX)
        inputBoxlayout2.addWidget(self.label_obstacle_y)
        inputBoxlayout2.addWidget(self.lineEdit_obsY)

        inputBoxlayout3 = QHBoxLayout()

        inputBoxlayout3.addWidget(self.pushButton)
        inputBoxlayout3.addWidget(self.saveButton)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(lbl_img)
        rightLayout.addLayout(inputBoxlayout1)
        rightLayout.addLayout(inputBoxlayout2)
        rightLayout.addLayout(inputBoxlayout3)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def paintEvent(self, e):  # QPaintEvent는 페인트이벤트는 위젯이 뒤에 있다가 앞으로 나오게되어 새로 그리기를 수행할 필요가 있을 운영체계에 의해 발생한다.
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp, self.projectile_x, self.projectile_y, self.obstacle_x, self.obstacle_y)
        qp.end()

    def draw_point(self, qp, _x, _y, _obs_x, _obs_y):

        qp.setPen(QPen(Qt.black, 2))
        qp.drawLine(0, 370, 700, 370)

        qp.setPen(QPen(Qt.blue, 8))
        _y = 370 - int(_y * 5)
        _x = int(_x * 5)
        qp.drawPoint(_x, _y)

        _obs_y = 370 - int(_obs_y * 5)
        _obs_x = int(_obs_x * 5)
        qp.setPen(QPen(Qt.red, 15))
        qp.drawPoint(_obs_x, _obs_y)

    #1
    def pushButtonClicked(self):
        try:
            self.angle = math.radians(float(self.lineEdit_angle.text()))
            self.velocity = float(self.lineEdit_velocity.text())
            self.obstacle_x = float(self.lineEdit_obsX.text())
            self.obstacle_y = float(self.lineEdit_obsY.text())
        except:
            self.statusBar().showMessage('숫자를 입력하세요.')
        else:
            self.list_x = []
            self.list_y = []
            v0 = self.velocity
            v0_x = v0 * math.cos(self.angle)
            v0_y = v0 * math.sin(self.angle)
            for i in range(400):

                t = i * 0.05
                x = v0_x * t
                y = v0_y * t - 0.5 * 9.81 * t * t
                self.list_x.append(x)
                self.list_y.append(y)
                self.projectile_x = x
                self.projectile_y = y
                QWidget.repaint(self)
                time.sleep(0.02)

                distance = math.sqrt((self.projectile_x - self.obstacle_x) * (self.projectile_x - self.obstacle_x) + (
                            self.projectile_y - self.obstacle_y) * (self.projectile_y - self.obstacle_y))
                if distance < 1:
                    self.statusBar().showMessage('맞췄습니다.')
                    break
                if self.projectile_y < 0:
                    self.statusBar().showMessage('빗나갔습니다.')
                    break

    def saveButtonClicked(self):
        save_csv(self.velocity, self.angle, self.list_x, self.list_y)
        self.statusBar().showMessage('파일로 저장 완료 하였습니다.')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()