import sys

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout

from final.introai.halma_core import HalmaCore

class HalmaTile(QPushButton):
    global xpos,ypos
    xpos=0
    ypos=0

    def setCoords(self,x,y):
        global xpos,ypos
        xpos = x
        ypos =y


class HalmaGui(QWidget):
    global move_queue, halma, app, tiles

    @pyqtSlot(bool)
    def pawnClicked(self):
        button = self.sender()
        x_pos = button.xpos
        y_pos = button.ypos

        if self.move_queue[0] is None:
            self.move_queue[0] = button
        else:
            last_button = self.move_queue[0]
            from_x = last_button.xpos
            from_y = last_button.ypos
            to_x = x_pos
            to_y = y_pos
            self.move_queue = [None]
            halma.moveXY(from_x,from_y,to_x,to_y)

    def __init__(self):
        super().__init__()
        global move_queue, halma, app, grid

        self.grid = QGridLayout()
        self.move_queue = [None]
        self.tiles = [[0 for x in range(halma.dimensions)] for y in range(halma.dimensions)]

        for y in range(0, halma.dimensions):
            for x in range(0, halma.dimensions):
                button = HalmaTile()
                button.xpos = x
                button.ypos = y
                button.setIconSize(QSize(28,28))
                button.setFixedSize(35,35)
                button.clicked.connect(self.pawnClicked)
                if(halma.checkLocationXY(x,y) is not None):
                    player = halma.checkLocationXY(x,y)[1]
                    if player == 0:
                        icon = QIcon('orange.png')
                    elif player == 1:
                        icon = QIcon('purple.png')
                else:
                    icon = QIcon()
                button.setStyleSheet("background-color: white; border-style: insert ")
                button.setIcon(icon)
                self.tiles[y][x] = button
                self.grid.addWidget(button, y+1, x+1)

        self.grid.setSpacing(0)
        self.setLayout(self.grid)
        self.setGeometry(100, 100, 10, 10)
        self.setWindowTitle("Halma")

    def pawnMovedEvent(self):
        for y in range(0, halma.dimensions):
            for x in range(0, halma.dimensions):
                button = self.tiles[y][x]
                if(halma.checkLocationXY(x,y) is not None):
                    player = halma.checkLocationXY(x,y)[1]
                    if player == 0:
                        icon = QIcon('orange.png')
                    elif player == 1:
                        icon = QIcon('purple.png')
                else:
                    icon = QIcon()
                button.setIcon(icon)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    halma = HalmaCore()
    gui = HalmaGui()
    halma.setGui(gui)
    gui.show()
    sys.exit(app.exec_())