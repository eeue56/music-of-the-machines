from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

from random import choice, randint

import numpy

import wave

from math import sin


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


class SoundFile(object):
    def  __init__(self, filename, length,  sample_rate, number_of_channels, frame_rate, sample_width):
        self.length = length
        self.file = wave.open(filename, 'wb')

        self.sample_rate = sample_rate
        self.number_of_channels = number_of_channels
        self.sample_width = sample_width
        self.frame_rate = frame_rate
        self.number_of_frames = (self.sample_rate * self.length * 2) / self.number_of_channels

    def write(self, signal):
        self.file.setparams((self.number_of_channels, self.sample_width, self.frame_rate, self.number_of_frames, 'NONE', 'noncompressed'))
        self.file.writeframes(signal)

    def close(self):
        self.file.close()


def generate_frequency(n):
    return 440 * pow (2, (n / 12))


class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 92, 64
    player = Player(4,4)
    eggs = {v : [] for v in COLOURS.values()}
    frequencies = [0 for x in xrange(8)]

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
        self.frequencies[x] = generate_frequency(y)

    def _generate_sound(self, frequency, sample_rate, omega):
        volume = 0
        period = sample_rate / frequency
        data = numpy.ones(period, dtype=numpy.float)

        data_length = len(data)

        fifth = data_length / 5

        volume_increase = 16000 / (data_length)

        for i in xrange(data_length):
            temp_frequency = frequency

            temp_frequency += randint(-100, 100) / 10

            data[i] = volume * sin(i * omega * temp_frequency)

            if i <= fifth:
                volume += volume_increase
            elif i <= fifth * 2:
                volume -= volume_increase / 2
            elif i >= fifth * 4.2:
                volume -= volume_increase / 1.5
            else:
                volume -= volume_increase / fifth

        return data

    def _generate_silence(self, sample_rate, omega):
        period = sample_rate / 128
        data = numpy.zeros(period, dtype=numpy.float)
        return data

    def make_wav(self):
        out_data = None
        tau = numpy.pi * 2

        duration = len(self.frequencies) / 0.8 # seconds
        sample_rate = 44100 # Hz
        samples = duration * sample_rate
        omega = tau / sample_rate

        resizer = int(samples / duration)

        for frequency in self.frequencies:

            if frequency == 0:
                data = self._generate_silence(sample_rate, omega)
            else:
                data = self._generate_sound(frequency, sample_rate, omega)

            data = numpy.resize(data, resizer)

            if out_data is not None:
                out_data = numpy.hstack((out_data, data))
            else:
                out_data = data

        out_data = numpy.resize(out_data, (samples,))
        out_signal = ''.join(wave.struct.pack('h', out_data[i]) for i in xrange(len(out_data)))

        sound_file = SoundFile("my_wav.wav", duration, sample_rate, 1, sample_rate, 2)

        sound_file.write(out_signal)
        sound_file.close()


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

            self.wav = None
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

            self.sound_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.sound_timer, QtCore.SIGNAL("timeout()"), self.play_sweet_songs)

            QtCore.QMetaObject.connectSlotsByName(self)
            self.paint_timer.start(30)
            self.sound_timer.start(1000 * 10)
            self.button_timer.start(50)

            self.calculated = False

            self.resize(500, 500)

        def keyPressEvent(self, event):
            self.keys.append(event.key())

        def keyReleaseEvent(self, event):
            self.keys.remove(event.key())

        def play_sweet_songs(self):
            if not self.calculated:
                return
            self.wav = QtGui.QSound("my_wav.wav")
            self.wav.play()

        def check(self):

            player = self.widget.player

            for key in self.keys[:]:
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

                if key == QtCore.Qt.Key_T:
                    if self.wav is not None:
                        self.wav.stop()
                    self.calculated = False
                    self.widget.make_wav()
                    self.calculated = True
                    if key in self.keys:
                        self.keys.remove(key)
 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()