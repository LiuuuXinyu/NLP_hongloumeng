import re
import jieba
import string
import collections as coll
import wx
import os
jieba.load_userdict('.\\manual-dict.txt') 


def divideIntoChapter(file_dir, mode, mode2): #mode 为
	'''
	注释预留位
	'''
	progressMax = 200
	dialog = wx.ProgressDialog("数据集拆分中...", "数据集拆分中", progressMax,\
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	keepGoing = True
	count = 0

	HLM = open(file_dir,encoding='utf-8')
	each_line = HLM.readline()
	chapter_count = 0
	chapter_text = ''

	if mode == 0:
		complied_rule = re.compile('第[一二三四五六七八九十百一二三四五六七八九十]+回')
		jieba.load_userdict('.\\manual-dict.txt')
	elif mode == 1:
		complied_rule = re.compile('第[1234567890]+回')

	if mode2 == 0:
		file_out_dir = '.\\chapter\\'
	elif mode2 == 1:
		file_out_dir = '.\\chapter2\\'


	while each_line:
		if re.findall(complied_rule,each_line):
			file_name = 'chap'+str(chapter_count)#第xxx回
			file_out = open(file_out_dir+file_name+'.txt','a',encoding = 'utf-8')
			file_out.write(chapter_text)
			chapter_count += 1
			file_out.close()
			count = count + 1#box
			keepGoing = dialog.Update(count)#box
			chapter_text = each_line
		else:
			chapter_text += each_line
		each_line = HLM.readline()

	file_name = 'chap'+str(chapter_count)
	file_out = open(file_out_dir+file_name+'.txt','a',encoding = 'utf-8')
	file_out.write(chapter_text)
	HLM.close()

	count = count + (progressMax-count)
	keepGoing = dialog.Update(count)


# 对单个章节的分词
def segmentation(text,text_count, mode2):

	if mode2 == 0:
		file_out_dir = '.\\ChapterWordSegmentation\\'
	elif mode2 == 1:
		file_out_dir = '.\\ChapterWordSegmentation2\\'


	file_name = 'chap'+str(text_count)+'-words.txt'
	file_out = open(file_out_dir+file_name,'a',encoding='utf-8')
	delset = string.punctuation
	line=text.readline()

	while line:
		seg_list = jieba.cut(line,cut_all = False)
		words = " ".join(seg_list)
		words = words.translate(delset) # 去除英文标点
		words = "".join(words.split('\n')) # 去除回车符
		words = delCNf(words) # 去除中文标点
		words = re.sub('[ \u3000]+',' ',words) # 去除多余的空格
		file_out.write(words)
		line = text.readline()

	file_out.close()
	text.close()


def doChapterWordSegmentation(mode2):
	if mode2 == 0:
		file_out_dir = '.\\chapter\\'
		endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])
	
	elif mode2 == 1:
		file_out_dir = '.\\chapter2\\'
		endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])

	progressMax = 200
	dialog = wx.ProgressDialog("章节分词中...", "章节分词中", progressMax,\
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	keepGoing = True
	count = 0

	for loop in range(1,endlen):
		file_name = 'chap'+str(loop)+'.txt'
		file_in = open(file_out_dir+file_name,'r',encoding = 'utf-8')
		segmentation(file_in,loop,mode2)
		file_in.close()
		count = count + 1#box
		keepGoing = dialog.Update(count)#box

	count = count + (progressMax-count)
	keepGoing = dialog.Update(count)
	dialog.Destroy()



# 去除中文字符函数
def delCNf(line):
	regex = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9\s]')
	return regex.sub('', line)


def count_words(text,textID,mode2):
	line = str(text)
	words = line.split()
	words_dict = coll.Counter(words) # 生成词频字典

	if mode2 == 0:
		file_out_dir = '.\\ChapterWordCount\\'
	
	elif mode2 == 1:
		file_out_dir = '.\\ChapterWordCount2\\'


	file_name = 'chap'+str(textID)+'-wordcount.txt'
	file_out = open(file_out_dir+file_name,'a',encoding = 'utf-8')

	# 排序后写入文本
	sorted_result = sorted(words_dict.items(),key = lambda d:d[1],reverse = True)
	for one in sorted_result:
		line = "".join(one[0] + '\t' + str(one[1]) + '\n')
		file_out.write(line)

	file_out.close()


def do_wordcount(mode2):

	if mode2 == 0:
		file_out_dir = '.\\chapter\\'
		endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])
		file_in_dir = '.\\ChapterWordSegmentation\\'
	
	elif mode2 == 1:
		file_out_dir = '.\\chapter2\\'
		endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])
		file_in_dir = '.\\ChapterWordSegmentation2\\'


	progressMax = 100000
	dialog = wx.ProgressDialog("按章节计数词频中...", "按章节计数词频中", progressMax,\
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	keepGoing = True
	count = 0

	for loop in range(1,endlen):
		file_name = 'chap'+str(loop)+'-words.txt'
		file_in = open(file_in_dir+file_name,'r',encoding = 'utf-8')
		line = file_in.readline()
		text = ''
		while line:
			text += line
			line = file_in.readline()
		count_words(text,loop,mode2)
		file_in.close()
		count = count + 1#box
		keepGoing = dialog.Update(count)#box

	count = count + (progressMax-count)
	keepGoing = dialog.Update(count)
	dialog.Destroy()