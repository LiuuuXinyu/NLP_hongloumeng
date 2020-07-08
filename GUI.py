import wx
from tkinter import *
import os 
import tkinter
import sys
import re
from win32com import client as wc
import time

import dataPrepare
import extractFeatureVector
import Feature2Matrix
import NaiveBayes
import SVM
import 删除一次流程的生成文件
import random
from CNN_ChineseTextBinaryClassify import fenci_jieba
#from CNN_ChineseTextBinaryClassify import train
from CNN_ChineseTextBinaryClassify import teval			
from CNN_ChineseTextBinaryClassify import honglou_teval


class MyFrame(wx.Frame):#继承而来的Frame类
	def __init__(self,superior):
		wx.Frame.__init__(self,parent = superior,title = "Fake Detector",pos=(150,5),size=(874,620))#pos是显示在哪，size是窗口大小

class MyButton(wx.Button):#继承而来的Button类，其实不继承也可以但是这样便于后续添加
	def __init__(self,frame,label,pos,size):
		wx.Button.__init__ (self, parent = frame,label = label,pos = pos,size = size)
class MyPanle(wx.Panel):
	def __init__(self,frame,pos,size,name):
		wx.Panel.__init__(self,parent = frame,pos = pos,size = size,name = name)

class MainInterface():
	
	def __init__(self):#在主界面__init__中，初始化所有按钮并绑定到执行程序，初始化所有需要的标语，初始化所有需要的框
		frame = MyFrame(None)
		frame.Show(True)

		#输入文本框1
		self.FileName = wx.TextCtrl(frame,pos = (5,8),size = (210,25))
		self.FileName.SetValue("请在此加载训练数据集")
		self.loadButton_1 = MyButton(frame,label = "打开",pos = (220,8),size=(80,25))
		self.loadButton_1.Bind(wx.EVT_BUTTON, self.ClickOpenButton_1)# binding
		self.clearButton_1 = MyButton(frame,label = "Clear",pos = (305,8),size=(80,25))
		self.clearButton_1.Bind(wx.EVT_BUTTON, self.ClickClearButton_1)# binding
		self.pButton_1 = MyButton(frame,label = "preProcessLoad",pos = (390,8),size=(100,25))
		self.pButton_1.Bind(wx.EVT_BUTTON, self.ClickLoadButton_1)# binding

		#输入文本框2
		self.FileName_2 = wx.TextCtrl(frame,pos = (5,80),size = (210,25))
		self.FileName_2.SetValue("请在此加载测试数据集")
		self.loadButton_2 = MyButton(frame,label = "打开数据集",pos = (220,80),size=(80,25))
		self.loadButton_2.Bind(wx.EVT_BUTTON, self.ClickOpenButton_2)# binding


		self.loadButton_3 = MyButton(frame,label = "loadmodel",pos = (305,80),size=(80,25))
		self.loadButton_3.Bind(wx.EVT_BUTTON, self.ClickOpenButton_3)# binding


		self.clearButton_2 = MyButton(frame,label = "Clear",pos = (390,112),size=(100,25))
		self.clearButton_2.Bind(wx.EVT_BUTTON, self.ClickClearButton_2)# binding
		self.pButton_2 = MyButton(frame,label = "preProcessLoad",pos = (390,80),size=(100,25))
		self.pButton_2.Bind(wx.EVT_BUTTON, self.ClickLoadButton_2)# binding


		list1 = ["第[一二三四五六七八九十]回","第[1234567890]回"]		
		self.radiobox1 = wx.RadioBox(frame,-1,"Segmentation",(500,0),(350, 104),list1,len(list1),wx.RA_SPECIFY_COLS)
		#self.radiobox1.Bind(wx.EVT_RADIOBOX,self.ClearPanel)# 这个绑定的东西要和之前的分开绑定
		

		list2 = ["Naive Bayes","   SVM   ","   TextCNN   "]		
		self.radiobox2 = wx.RadioBox(frame,-1,"Algorithm",(500,107),(350,88),list2,len(list2),wx.RA_SPECIFY_COLS)

		self.trainButton = MyButton(frame,label = "Train",pos = (5,153),size=(209,42))
		self.trainButton.Bind(wx.EVT_BUTTON, self.ClickTrainButton)# binding

		#随机拿出一条来展示
		self.testOneButton = MyButton(frame,label = "TestOne",pos = (222,153),size=(130,42))
		self.testOneButton.Bind(wx.EVT_BUTTON, self.ClickTestOneButton)# binding

		#test all
		self.testAllButton = MyButton(frame,label = "TestAll",pos = (360,153),size=(130,42))
		self.testAllButton.Bind(wx.EVT_BUTTON, self.ClickTestAllButton)# binding

		#
		self.resetAllButton = MyButton(frame,label = "ResetAll",pos = (5,480),size=(844,42))
		self.resetAllButton.Bind(wx.EVT_BUTTON, self.ClickResetAllButton)# binding

		self.tutorialButton = MyButton(frame,label = "Tutorial",pos = (5,530),size=(844,42))
		self.tutorialButton.Bind(wx.EVT_BUTTON, self.ClickTutorialButton)# binding


		self.FileName_8 = wx.TextCtrl(frame,pos = (220,112),size=(165,25))
		self.FileName_8.SetValue("trained_model")


		self.FileContent = wx.TextCtrl(frame, pos = (5,210),size = (485,260), style = wx.TE_MULTILINE | wx.HSCROLL)
		self.FileContent2 = wx.TextCtrl(frame, pos = (500,210),size = (350,260), style = wx.TE_MULTILINE | wx.HSCROLL)

		self.keepGoing = True
		self.count = 0

		self.FileName_3 = wx.TextCtrl(frame,pos = (5,40),size = (135,25))
		self.FileName_3.SetValue("训练集加载结果")

		self.FileName_4 = wx.TextCtrl(frame,pos = (5,112),size = (210,25))
		self.FileName_4.SetValue("测试集加载结果")

		self.FileName_5 = wx.TextCtrl(frame,pos = (148,40),size = (181,25))
		self.FileName_5.SetValue("train标注label1的范围(例:70 代表训练集中1-70为label1)")

		self.FileName_6 = wx.TextCtrl(frame,pos = (337,40),size = (73,25))
		self.FileName_6.SetValue("label1")

		self.FileName_7 = wx.TextCtrl(frame,pos = (418,40),size = (73,25))
		self.FileName_7.SetValue("label2")


	def ClickTutorialButton(self,event):
		dlg = wx.MessageDialog(None, u"软件使用说明：①打开数据集并选择合适的章节区分方法加载数据集；②标注训练集和label并选择方法训练；③加载测试集；④选择方法测试测试集；⑤ResetAll全部清空")
		if dlg.ShowModal() == wx.ID_YES:
			self.Close(True)
			dlg.Destroy()

	def ClickOpenButton_1(self,event):

		wildcard = 'txt files (*.txt)|*.txt'
		dialog = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
		if dialog.ShowModal() == wx.ID_OK:
			self.FileName.SetValue(dialog.GetPath())
			dialog.Destroy

	def ClickOpenButton_2(self,event):

		wildcard = 'txt files (*.txt)|*.txt'
		dialog = wx.FileDialog(None,'select',os.getcwd(),'',wildcard,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
		if dialog.ShowModal() == wx.ID_OK:
			self.FileName_2.SetValue(dialog.GetPath())
			dialog.Destroy


	def ClickOpenButton_3(self,event):

		#wildcard = 'txt files (*.txt)|*.txt'
		dialog = wx.DirDialog(None,'选择文件夹',style = wx.DD_DEFAULT_STYLE ) 
		if dialog.ShowModal() == wx.ID_OK:
			self.FileName_8.SetValue(dialog.GetPath())
			dialog.Destroy

	
	def ClickClearButton_1(self,event):
		
		self.FileName.Clear()
		self.FileName.SetValue("请在此加载训练数据集")
		self.FileName_3.SetValue("训练集加载结果")
		删除一次流程的生成文件.del_file('.\\chapter\\')
		删除一次流程的生成文件.del_file('.\\ChapterWordCount\\')
		删除一次流程的生成文件.del_file('.\\ChapterWordSegmentation\\')
		dlg = wx.MessageDialog(None, u"训练集清除成功")
		if dlg.ShowModal() == wx.ID_YES:
			self.Close(True)
			dlg.Destroy()


	def ClickClearButton_2(self,event):
		
		self.FileName_2.Clear()
		self.FileName_2.SetValue("请在此加载测试数据集")
		self.FileName_4.SetValue("测试集加载结果")
		self.FileName_8.Clear()
		self.FileName_8.SetValue("trained_model")
		删除一次流程的生成文件.del_file('.\\chapter2\\')
		删除一次流程的生成文件.del_file('.\\ChapterWordCount2\\')
		删除一次流程的生成文件.del_file('.\\ChapterWordSegmentation2\\')
		dlg = wx.MessageDialog(None, u"测试集清除成功")
		if dlg.ShowModal() == wx.ID_YES:
			self.Close(True)
			dlg.Destroy()


	def ClickLoadButton_1(self,event):
		'''
		load data to X y???
		'''
		try:
			dataPrepare.divideIntoChapter(file_dir = self.FileName.GetValue(), mode = self.radiobox1.GetSelection(), mode2 = 0)
			
			file_out_dir_1 = '.\\chapter\\'
			train_end_1 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_1))])
			flag = 1
			if train_end_1 < 5:
				flag = 0
				dlg = wx.MessageDialog(None, u"请检测选择的拆分方法是否有误")
				删除一次流程的生成文件.del_file('.\\chapter\\')
				if dlg.ShowModal() == wx.ID_YES:
					self.Close(True)
					dlg.Destroy()
			if flag:

				dataPrepare.doChapterWordSegmentation(mode2 = 0)
				dataPrepare.do_wordcount(mode2 = 0)
				self.FileName_3.Clear()
				self.FileName_3.SetValue("加载到训练集共"+str(train_end_1-1)+'篇')

				

		except:
			dlg = wx.MessageDialog(None, u"请检查输入的训练集是否有误")
			if dlg.ShowModal() == wx.ID_YES:
				self.Close(True)
				dlg.Destroy()


	def ClickLoadButton_2(self,event):
		'''
		load data to X y????
		'''
		try:
			dataPrepare.divideIntoChapter(file_dir = self.FileName_2.GetValue(), mode = self.radiobox1.GetSelection(), mode2 = 1)
			
			file_out_dir_2 = '.\\chapter2\\'
			train_end_2 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_2))])
			flag = 1
			if train_end_2 < 5:
				flag = 0
				dlg = wx.MessageDialog(None, u"请检测选择的拆分方法是否有误")
				删除一次流程的生成文件.del_file('.\\chapter2\\')
				if dlg.ShowModal() == wx.ID_YES:
					self.Close(True)
					dlg.Destroy()
			if flag:
				dataPrepare.doChapterWordSegmentation(mode2 = 1)
				dataPrepare.do_wordcount(mode2 = 1)

				self.FileName_4.Clear()
				self.FileName_4.SetValue("加载到测试集共"+str(train_end_2-1)+'篇')

		except:
			dlg = wx.MessageDialog(None, u"请检查输入的测试集是否有误")
			if dlg.ShowModal() == wx.ID_YES:
				self.Close(True)
				dlg.Destroy()


	def ClickTrainButton(self, event):
		'''
		依据！！！！！训练集！！！！！构成特征向量
		#在训练中生成对应的特征向量
		'''
		#********************************************

		try:

			extractFeatureVector.cut_words(file_dir = self.FileName.GetValue())
			extractFeatureVector.count_words()
			extractFeatureVector.getFeatureVector()
		except:
			dlg = wx.MessageDialog(None, u"请检查输入的训练集是否有误")
			if dlg.ShowModal() == wx.ID_YES:
				self.Close(True)
				dlg.Destroy()


	def ClickTestAllButton(self, event):
		#原来tools.py
		#特征向量对到矩阵中，可以直接强行匹配，前xxx行为train，后yyy行为test

		#错误处理



		try:

			if self.radiobox2.GetSelection() == 0:
				matrix = Feature2Matrix.txt2matrix()
				file_out_dir_1 = '.\\chapter\\'
				train_end_1 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_1))])-1
				labe1range = int(self.FileName_5.GetValue())
				label1 = str(self.FileName_6.GetValue())
				label2 = str(self.FileName_7.GetValue())
				result, textall = NaiveBayes.built_model(x_train=matrix,trainrange=train_end_1,labe1range=labe1range,label1=label1,label2=label2)####+_HLM
				strr = '朴素贝叶斯：'
				self.FileContent.SetValue(strr+"全数据测试")
				self.FileContent2.SetValue(str(textall))
				
			elif self.radiobox2.GetSelection() == 1:
				matrix = Feature2Matrix.txt2matrix()
				file_out_dir_1 = '.\\chapter\\'
				train_end_1 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_1))])-1
				labe1range = int(self.FileName_5.GetValue())
				label1 = str(self.FileName_6.GetValue())
				label2 = str(self.FileName_7.GetValue())
				result, textall = SVM.built_model(x_train=matrix,trainrange=train_end_1,labe1range=labe1range,label1=label1,label2=label2)####+_HLM
				strr = 'SVM：'
				self.FileContent.SetValue(strr+"全数据测试")
				self.FileContent2.SetValue(str(textall))

			elif self.radiobox2.GetSelection() == 2:
				label1 = str(self.FileName_6.GetValue())
				label2 = str(self.FileName_7.GetValue())
				strr = 'TextCNN'
				textall = ''
				progressMax = 200
				dialog = wx.ProgressDialog("TextCNN测试中...", "TextCNN测试中", progressMax,\
					style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
				keepGoing = True
				count = 0


				if self.FileName_8.GetValue().split('\\')[-1] == '1594161410': 
					for i in range(1,28):

						real_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\cnn_test_file\\chap" +str(i)+".txt"
						bullshit_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\fenci\\bullshit_data_test.txt"
						relative_test_path = "C:\\Users\\Administrator\\Desktop\\HLM\\Final版本\\GUI-Final\\CNN_ChineseTextBinaryClassify\\runs\\1594161410\\checkpoints\\"
						result = teval.eval_test(real_test_data_path,bullshit_test_data_path,relative_test_path)
						dirr = '.\\CNN_ChineseTextBinaryClassify\\chapter2\\' + real_test_data_path.split('\\')[-1]
						if result == 'Person':
							result = label1
						else:
							result = label2
						
						with open(real_test_data_path,'r',encoding = 'utf-8') as f:
							line = f.readline()
							line=line.strip('\n')
							textall += line
							textall += ':\t'
							textall += str(result)
							textall += '\n'
						count = count + 1#box
						keepGoing = dialog.Update(count)#box
						self.FileContent.SetValue(strr+"全数据测试")
						self.FileContent2.SetValue(str(textall))



				elif self.FileName_8.GetValue().split('\\')[-1] == '1594157519': 
					for i in range(1,20):


						real_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\honglou_cnn_test_file\\chap" +str(i)+".txt"
						bullshit_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\fenci\\bullshit_data_test.txt"
						relative_test_path = ".\\CNN_ChineseTextBinaryClassify\\runs\\1594157519\\checkpoints\\"
						result = honglou_teval.eval_test(real_test_data_path,bullshit_test_data_path,relative_test_path)
			
						dirr = '.\\CNN_ChineseTextBinaryClassify\\HLMchapter2\\' + real_test_data_path.split('\\')[-1]
						if result == '曹雪芹':
							result = label1
						else:
							result = label2
							
						with open(real_test_data_path,'r',encoding = 'utf-8') as f:
							line = f.readline()
							line=line.strip('\n')
							textall += line
							textall += ':\t'
							textall += str(result)
							textall += '\n'
						count = count + 1#box
						keepGoing = dialog.Update(count)#box

					count = count + (progressMax-count)
					keepGoing = dialog.Update(count)
					dialog.Destroy()

					self.FileContent.SetValue(strr+"全数据测试")
					self.FileContent2.SetValue(str(textall))


				elif self.FileName_8.GetValue().split('\\')[-1] == 'trained_model':
					dlg = wx.MessageDialog(None, u"请先加载model再进行测试")
					if dlg.ShowModal() == wx.ID_YES:
						self.Close(True)
						dlg.Destroy()

		except:
			dlg = wx.MessageDialog(None, u"请检查输入的测试集是否有误")
			if dlg.ShowModal() == wx.ID_YES:
				self.Close(True)
				dlg.Destroy()


	def ClickTestOneButton(self, event):

		#错误处理

		try:
			if self.radiobox2.GetSelection() == 0:
				matrix = Feature2Matrix.txt2matrix()
				file_out_dir_1 = '.\\chapter\\'
				train_end_1 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_1))])-1
				labe1range = int(self.FileName_5.GetValue())
				label1 = str(self.FileName_6.GetValue())
				label2 = str(self.FileName_7.GetValue())
				result,_ = NaiveBayes.built_model(x_train=matrix,trainrange=train_end_1,labe1range=labe1range,label1=label1,label2=label2)
				strr = '朴素贝叶斯：'
			
			elif self.radiobox2.GetSelection() == 1:
				matrix = Feature2Matrix.txt2matrix()
				file_out_dir_1 = '.\\chapter\\'
				train_end_1 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_1))])-1
				labe1range = int(self.FileName_5.GetValue())
				label1 = str(self.FileName_6.GetValue())
				label2 = str(self.FileName_7.GetValue())
				result, _ = SVM.built_model(x_train=matrix,trainrange=train_end_1,labe1range=labe1range,label1=label1,label2=label2)
				strr = 'SVM：'

			elif self.radiobox2.GetSelection() == 2:


				if self.FileName_8.GetValue().split('\\')[-1] == '1594161410': #Bullshit的单回问题
					
					temp = random.randint(1,28)
					real_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\cnn_test_file\\chap" +str(temp)+".txt"
					bullshit_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\fenci\\bullshit_data_test.txt"
					relative_test_path = ".\\CNN_ChineseTextBinaryClassify\\runs\\1594161410\\checkpoints\\"



					result = teval.eval_test(real_test_data_path,bullshit_test_data_path,relative_test_path)
					strr = 'TextCNN'

				elif self.FileName_8.GetValue().split('\\')[-1] == '1594157519': #红楼梦的单回问题
					
					temp = random.randint(1,20)
					real_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\honglou_cnn_test_file\\chap" +str(temp)+".txt"
					bullshit_test_data_path = ".\\CNN_ChineseTextBinaryClassify\\fenci\\bullshit_data_test.txt"
					relative_test_path = ".\\CNN_ChineseTextBinaryClassify\\runs\\1594157519\\checkpoints\\"
					
					result = honglou_teval.eval_test(real_test_data_path,bullshit_test_data_path,relative_test_path)
					strr = 'TextCNN'

				elif self.FileName_8.GetValue().split('\\')[-1] == 'trained_model':
					dlg = wx.MessageDialog(None, u"请先加载model再进行测试")
					if dlg.ShowModal() == wx.ID_YES:
						self.Close(True)
						dlg.Destroy()
				

		
			if self.radiobox2.GetSelection() != 2:
				file_out_dir_33 = '.\\chapter2\\'
				train_end_33 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_33))]) - 1
				temp = random.randint(1,train_end_33-1)
				print("测试数据集总量，从中进行筛选",train_end_33)
				templine = ''
				file_out_dir_22 = '.\\chapter\\'
				train_end_22 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_22))]) - 1

				dirr = '.\\chapter2\\chap'+str(temp)+'.txt'
				with open(dirr,'r',encoding = 'utf-8') as f:
					lines = f.readlines()
					for line in lines:
						templine += line
				self.FileContent.SetValue(templine)
				self.FileContent2.SetValue(strr+"\n"+"经判断，该回书为"+str(result[int(train_end_22-1+int(temp))])+"所作")
			
			else:

				label1 = str(self.FileName_6.GetValue())
				label2 = str(self.FileName_7.GetValue())

				if self.FileName_8.GetValue().split('\\')[-1] == '1594161410': #Bullshit的单回问题
					dirr = '.\\CNN_ChineseTextBinaryClassify\\chapter2\\' + real_test_data_path.split('\\')[-1]
					if result == 'Person':
						result = label1
					else:
						result = label2

				elif self.FileName_8.GetValue().split('\\')[-1] == '1594157519':#HLM的单回问题
					dirr = '.\\CNN_ChineseTextBinaryClassify\\HLM_chapter2\\' + real_test_data_path.split('\\')[-1] 
					if result == '曹雪芹':
						result = label1
					else:
						result = label2

				templine = ''
				with open(dirr,'r',encoding = 'utf-8') as f:
					lines = f.readlines()
					for line in lines:
						templine += line


				self.FileContent.SetValue(templine)
				self.FileContent2.SetValue(strr+"\n"+"经判断，该回书为"+result+"所作")
			

		except:
			dlg = wx.MessageDialog(None, u"请检查输入的测试集是否有误")
			if dlg.ShowModal() == wx.ID_YES:
				self.Close(True)
				dlg.Destroy()


	def ClickResetAllButton(self,event):
		删除一次流程的生成文件.delall()
		self.FileName.SetValue("请在此加载训练数据集")
		self.FileName_2.SetValue("请在此加载测试数据集")
		self.FileName_3.SetValue("训练集加载结果")
		self.FileName_4.SetValue("测试集加载结果")
		self.FileName_5.SetValue("train标注label1的范围(例:70 代表训练集中1-70为label1)")
		self.FileName_6.SetValue("label1")
		self.FileName_7.SetValue("label2")
		self.FileName_8.SetValue("trained_model")
		dlg = wx.MessageDialog(None, u"done!")
		if dlg.ShowModal() == wx.ID_YES:
			self.Close(True)
			dlg.Destroy()

		self.FileContent.Clear()
		self.FileContent2.Clear()

if __name__ == '__main__':

		app = wx.App()
		MainFace = MainInterface()
		app.MainLoop()
