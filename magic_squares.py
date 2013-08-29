from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
from random import choice

COLOURS = { 'black' : (0, 0, 0),
            'other-grey' : (0.25, 0.25, 0.25),
            'grey' : (0.4, 0.4, 0.4),
            'white' : (1, 1, 1)}

class Player(object):
    def __init__(self, x, y, health=3):
        self.x = x
        self.y = y
        self.health = health
        self.is_exploded = False
        self.color = COLOURS['grey']


class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 92, 64
    player = Player(4,4)
    eggs = {v : [] for v in COLOURS.values()}
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
 
    def draw_square(self, x, y, size=1):
        gl.glRectf(x, y, x + size, y + size)

    def add_egg(self, x, y, color=COLOURS['white']):
        self.eggs[color].append((x, y))

    def draw_eggs(self):        
        for color, items in self.eggs.iteritems():
            r, g, b = color
            gl.glColor3f(r, g, b)
            for item in items:
                x = item[0]
                y = item[1]
                self.draw_square(x, y, 1)

    def draw_player(self):

        r, g, b = self.player.color
        gl.glColor3f(r, g, b)
        self.draw_square(self.player.x, self.player.y)

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        
        # tell OpenGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        r, g, b = COLOURS['grey']
        gl.glColor3f(r, g, b)

        self.draw_eggs()
        self.draw_player()

    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size    
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, self.width, self.height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(0, 8, 0, 8, -1, 1)
 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys
 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            self.widget = GLPlotWidget()
            self.color = COLOURS['white']
            self.keys = []

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
            
            self.button_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.button_timer, QtCore.SIGNAL("timeout()"), self.check)

            QtCore.QMetaObject.connectSlotsByName(self)
            self.paint_timer.start(30)
            self.button_timer.start(50)

            self.resize(500, 500)

        def keyPressEvent(self, event):
            self.keys.append(event.key())

        def keyReleaseEvent(self, event):
            self.keys.remove(event.key())

        def check(self):

            player = self.widget.player

            for key in self.keys:
                if key == QtCore.Qt.Key_A:
                    if player.x > 0:
                        self.widget.player.x -= 1
                if key == QtCore.Qt.Key_D:
                    if player.x < 7:
                        self.widget.player.x += 1
                if key == QtCore.Qt.Key_W:
                    if player.y < 7:
                        self.widget.player.y += 1
                if key == QtCore.Qt.Key_S:
                    if player.y > 0:
                        self.widget.player.y -= 1
                if key == QtCore.Qt.Key_Space:
                    self.widget.add_egg(self.widget.player.x, self.widget.player.y, COLOURS['white'])
                if key == QtCore.Qt.Key_1:
                    self.widget.player.color = COLOURS['white']
                if key == QtCore.Qt.Key_2:
                    self.widget.player.color = COLOURS['grey']
                if key == QtCore.Qt.Key_3:
                    self.widget.player.color = COLOURS['other-grey']
 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()