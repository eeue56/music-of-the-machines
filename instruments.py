from __future__ import division

from random import randint

class Instrument(object):
    def __init__(self, data_length, volume_max):
        self.data_length = data_length
        self.volume_max = volume_max
        self.fifth = self.data_length / 5
        self.volume_increase = self.volume_max / self.fifth

    def variance(self, intended_frequency, current_frequency):
        return current_frequency + randint(-100, 100)

    def envelope(self, current_volume, current_i):
        """ Basic envelope model """

        fifth = self.fifth
        volume_increase = self.volume_increase
        
        if current_i <= fifth:
            return current_volume + volume_increase
        elif current_i <= fifth * 2:
            return current_volume - (volume_increase / 2)
        elif current_i >= fifth * 4.2:
            return current_volume - (volume_increase / 1.5)
        elif current_volume < 0:
            return fifth / 5
        else:
            return current_volume - (volume_increase / fifth)

class Flatter(Instrument):
    def __init__(self, *args, **kwargs):
        Instrument.__init__(self, *args, **kwargs)
        self.forth = self.data_length / 4
        self.volume_increase = self.volume_max / self.forth

        self._debug = True

    def variance(self, intended_frequency, current_frequency):
        if current_frequency > intended_frequency:
            return intended_frequency - 20
        else:
            return intended_frequency + 37

    def envelope(self, current_volume, current_i):

        forth = self.forth
        volume_increase = self.volume_increase
        
        if current_i <= forth:
            return current_volume + volume_increase
        elif current_i <= forth * (2 / 3):
            return current_volume - (volume_increase / 2)
        elif current_i >= forth * (5 / 3):
            return current_volume - (volume_increase / 1.5)
        elif current_volume < 0:
            return forth / 4
        else:
            return current_volume - (volume_increase / forth)

