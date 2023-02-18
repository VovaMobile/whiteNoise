import threading
import globalPluginHandler
import time
import wave
import config
import os
import nvwave

class Player:
	__stop = False
	def __init__(self):
		filepath = (os.path.join(os.path.dirname(os.path.realpath(__file__)),"white.wav"))
		self.f = wave.open(filepath,"r")
		if self.f is None: raise RuntimeError("can not open file %s"%fileName)
		self.fileWavePlayer = nvwave.WavePlayer(channels=self.f.getnchannels(), samplesPerSec=self.f.getframerate(),bitsPerSample=self.f.getsampwidth()*8, outputDevice=config.conf["speech"]["outputDevice"],wantDucking=False)
	
	def play(self) :
		while not self.__stop :
			self.f.rewind()
			self.fileWavePlayer.feed(self.f.readframes(self.f.getnframes()))
			self.fileWavePlayer.idle()
	
	def stop(self) :
		self.__stop = True
		self.fileWavePlayer.stop()
		

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		self.player = Player()
		self.noiseThread = threading.Thread(target=self.player.play)
		self.noiseThread.start()
		return super(GlobalPlugin,self).__init__()
	
	def terminate(self) :
		self.player.stop()
		self.noiseThread.join()
	