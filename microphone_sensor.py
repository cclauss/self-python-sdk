
# Copyright 2016 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sensor import Sensor
from sensor_manager import SensorManager

import multiprocessing
import sys
import subprocess
import pyaudio
import numpy as np

from subprocess import Popen, PIPE


def worker(sensor):
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1600)
	while True:
		data = stream.read(int(1600))
		SensorManager.get_instance().send_data(sensor, data)

class MicrophoneSensor(Sensor):

	def __init__(self, sensor_id, sensor_name, data_type, binary_type):
		super(self.__class__, self).__init__(sensor_id, sensor_name, data_type, binary_type)
		self.is_paused = False

	def on_start(self):
		print "Microphone Sensor has started!"
		self.p = multiprocessing.Process(target=worker, args=(self,))
		self.p.start()
		return True

	def on_stop(self):
		print "Microphone Sensor has stopped!"
		self.p.terminate()
		return True

	def on_pause(self):
		print "Microphone Sensor has paused!"
		self.p.terminate()
		self.is_paused = True

	def on_resume(self):
		print "Microphone Sensor has resumed!"
		self.p = multiprocessing.Process(target=worker, args=(self,))
		self.p.start()
		self.is_paused = False