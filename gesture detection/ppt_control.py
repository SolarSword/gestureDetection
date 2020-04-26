# the original author of the win32com ppt control code 
# are written by sharpdeep. 
# thanks a lot! 

import win32com.client
import win32api
import win32con
import time
import pythoncom


import os 
import sys
import pandas

import preprocess as pre 
from dtw import DTW
from dtw import cosine_cost


VK_CODE = {
	'spacebar':0x20,
	'down_arrow':0x28,
}

class PPTControler:
	def __init__(self):
        # multi-thread may cause some problems http://www.cnblogs.com/AlgorithmDot/p/3386972.html
		pythoncom.CoInitialize()
		self.app = win32com.client.Dispatch("PowerPoint.Application")

	def fullScreen(self):
		if self.hasActivePresentation():
			self.app.ActivePresentation.SlideShowSettings.Run()
			return self.getActivePresentationSlideIndex()

	def click(self):
		win32api.keybd_event(VK_CODE['spacebar'],0,0,0)
		win32api.keybd_event(VK_CODE['spacebar'],0,win32con.KEYEVENTF_KEYUP,0)
		return self.getActivePresentationSlideIndex()

	def gotoSlide(self,index):
		#go to a certain page
		if self.hasActivePresentation():
			try:
				self.app.ActiveWindow.View.GotoSlide(index)
				return self.app.ActiveWindow.View.Slide.SlideIndex
			except:
				self.app.SlideShowWindows(1).View.GotoSlide(index)
				return self.app.SlideShowWindows(1).View.CurrentShowPosition

	def nextPage(self):
		if self.hasActivePresentation():
			count = self.getActivePresentationSlideCount()
			index = self.getActivePresentationSlideIndex()
			return index if index >= count else self.gotoSlide(index+1)

	def prePage(self):
		if self.hasActivePresentation():
			index =  self.getActivePresentationSlideIndex()
			return index if index <= 1 else self.gotoSlide(index-1)

	def getActivePresentationSlideIndex(self):
		if self.hasActivePresentation():
			try:
				index = self.app.ActiveWindow.View.Slide.SlideIndex
			except:
				index = self.app.SlideShowWindows(1).View.CurrentShowPosition
		return index

	def getActivePresentationSlideCount(self):
		return self.app.ActivePresentation.Slides.Count

	def getPresentationCount(self):
		return self.app.Presentations.Count

	def hasActivePresentation(self):
		return True if self.getPresentationCount() > 0 else False


dtw = DTW()
dtw.tamplate_load('model.npy')

motion_period = 5 # 5s
frequency = 50 # 50Hz
period = motion_period * frequency

gesture_dataflow_path = 'simulation.csv'
gestures = pre.data_segmentation(gesture_dataflow_path, period, 2, 5)


ppt = PPTControler()
ppt.fullScreen()
'''
for i in range(8):
	time.sleep(1)
	ppt.nextPage()
'''

for i in range(0, len(gestures)):
	prediction_label = dtw.test(gestures[i], cosine_cost)
	if (prediction_label == 'snap_a_finger_arm_up'):
		time.sleep(1)
		ppt.nextPage()
	elif(prediction_label == 'wave_down'):
		time.sleep(1)
		ppt.prePage()
