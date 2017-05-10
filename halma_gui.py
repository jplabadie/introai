import sys

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QVBoxLayout

from halma_core import HalmaCore

class HalmaTile(QPushButton):

    def __init__(self, *__args):
        super().__init__(*__args)

        self.xpos=0
        self.ypos=0

    def setCoords(self,x,y):
        self.xpos = x
        self.ypos = y

    def enterEvent(self, *args, **kwargs):
        super().setIconSize(QSize(20,20))
        self.setText('\r(' + str(self.xpos) + ',' + str(self.ypos) + ')')

    def leaveEvent(self, *args, **kwargs):
        super().setIconSize(QSize(60, 60))
        self.setText('')

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        bar = self.menuBar()
        game_menu = bar.addMenu("Game")
        game_menu.addAction("save")
        game_menu.addAction("add")
        #game_menu.triggered[QAction].connect( self.gameMenuTrigger )

        self.setStyleSheet("background-color: white")
        self.statusBar = QStatusBar()
        turnButton = QPushButton()
        self.statusBar.addWidget(turnButton)
        self.setWindowTitle("Halma")
        self.setStatusBar(self.statusBar)
        self.statusChangedEvent()

    def statusChangedEvent(self):
        self.statusBar.showMessage(halma.getStatusMessage())

    def setCenterWidget(self, widget):
        self.setCentralWidget(widget)

class HalmaGui(QWidget):
    global move_queue, halma, app, tiles

    @pyqtSlot(bool)
    def pawnClicked(self):
        if self.finished:
            return
        button = self.sender()
        x_pos = button.xpos
        y_pos = button.ypos

        if self.move_queue[0] is None:
            if x_pos % 2 != 0:
                button.setStyleSheet("background-color: #aaeded; border: 1px grey white; border-style: ridge")
            else:
                button.setStyleSheet("background-color: #aaeded; border: 1px grey white; border-style: ridge")
            self.move_queue[0] = button
        else:
            last_button = self.move_queue[0]
            from_x = last_button.xpos
            from_y = last_button.ypos
            to_x = x_pos
            to_y = y_pos
            self.move_queue = [None]

            player = None
            if((from_x, from_y) in halma.green["pawns"]):
                player = halma.green
            elif((from_x, from_y) in halma.red["pawns"]):
                player = halma.red
            halma.move(player, (from_x,from_y),(to_x,to_y))
            if from_y % 2 != 0:
                if from_x % 2 == 0:
                    last_button.setStyleSheet("background-color: white; border: 1px grey white; border-style: ridge")
                else:
                    last_button.setStyleSheet("background-color: #ededed; border: 1px grey white; border-style: ridge")
            else:
                if from_x % 2 == 0:
                    last_button.setStyleSheet("background-color: #ededed; border: 1px grey white; border-style: ridge")
                else:
                    last_button.setStyleSheet("background-color: white; border: 1px grey white; border-style: ridge")

    def statusChangedEvent(self):
        mw.statusChangedEvent()

    def __init__(self):
        super().__init__()
        global move_queue, halma, app, grid

        self.finished = False
        self.grid = QGridLayout()
        self.move_queue = [None]
        self.tiles = [[0 for x in range(halma.xy_dim)] for y in range(halma.xy_dim)]
        color_toggle = False

        for y in range(0, halma.xy_dim):
            for x in range(0, halma.xy_dim):
                button = HalmaTile()
                button.setCoords(x,y)
                button.setIconSize(QSize(60,60))

                button.setFixedSize(65,65)
                button.clicked.connect(self.pawnClicked)
                if halma.board[x][y] == 0:
                    icon = QIcon('green_pawn.png')
                elif halma.board[x][y] == 1:
                    icon = QIcon('red_pawn.png')
                else:
                    icon = QIcon()

                if color_toggle:
                    button.setStyleSheet("background-color: white; border: 1px grey white; border-style: ridge ")
                    color_toggle = False
                else:
                    button.setStyleSheet("background-color: #ededed; border:1px grey white; border-style: ridge ")
                    color_toggle = True
                button.setIcon(icon)
                self.tiles[y][x] = button
                self.grid.addWidget(button, y+1, x+1)

            if color_toggle:
                color_toggle = False
            else:
                color_toggle = True
        self.grid.setSpacing(1)
        self.setLayout(self.grid)
        self.setGeometry(100, 100, 10, 10)
        self.setWindowTitle("Halma")

    def winStatusEvent(self):
        mw.statusChangedEvent()
        #self.finished = True

    def pawnMovedEvent(self):
        gui.show()
        for y in range(0, halma.xy_dim):
            for x in range(0, halma.xy_dim):
                button = self.tiles[y][x]
                if halma.board[x][y] == 0:
                    icon = QIcon('green_pawn.png')
                elif halma.board[x][y] == 1:
                    icon = QIcon('red_pawn.png')
                else:
                    icon = QIcon()
                button.setIcon(icon)

if __name__ == '__main__':
    aiplayer = sys.argv[0]

    if aiplayer is None:
        aiplayer = 0

    app = QApplication(sys.argv)
    halma = HalmaCore()
    halma.setAiPlayer(aiplayer)
    gui = HalmaGui()

    halma.gui = gui
    mw = MainWindow()
    mw.setCenterWidget(gui)
    mw.show()
    #gui.show()
    sys.exit(app.exec_())
