from __future__ import division

from random import randint

class Instrument(object):
	def __init__(self, data_length, volume_max):
		self.data_length = data_length
		self.volume_max = volume_max
		self.fifth = self.data_length / 5
		self.volume_increase = self.volume_max / fifth

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
        else:
            return current_volume - (volume_increase / fifth)
