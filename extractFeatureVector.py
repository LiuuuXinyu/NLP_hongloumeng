import jieba
import re
import string
import collections as coll
import os
import wx

jieba.load_userdict('.\\manual-dict.txt') # 导入搜狗的红楼梦词库，这步遇到一个小问题



def delCNf(line):
	regex = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9\s]')
	return regex.sub('', line)


# 对整篇文章分词，注意这里是整训练集
def cut_words(file_dir):
	HLM = open(file_dir,'r',encoding = 'utf-8')
	file_out = open('.\\train-词.txt','a',encoding = 'utf-8')
	delset = string.punctuation
	line = HLM.readline()

	progressMax = 100000
	dialog = wx.ProgressDialog("训练集整体分词中...", "训练集整体分词中", progressMax,\
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	keepGoing = True
	count = 0

	while line:
		seg_list = jieba.cut(line,cut_all = False)
		words = ' '.join(seg_list)
		words = words.translate(delset) # 去除英文标点
		words = "".join(words.split('\n')) # 去除回车符
		words = delCNf(words) # 去除中文标点
		words = re.sub('[ \u3000]+',' ',words) # 去除多余的空格
		file_out.write(words)
		line = HLM.readline()
		count = count + 1#box
		keepGoing = dialog.Update(count)#box

	file_out.close()
	HLM.close()

	count = count + (progressMax-count)
	keepGoing = dialog.Update(count)
	dialog.Destroy()


def count_words():
	data = open('.\\train-词.txt','r',encoding = 'utf-8')
	line = data.read()
	data.close()
	words = line.split()
	words_dict = coll.Counter(words) # 生成词频字典

	file_out = open('.\\词频.txt','a',encoding = 'utf-8')

	# 排序后写入文本
	sorted_result = sorted(words_dict.items(),key = lambda d:d[1],reverse = True)

	progressMax = 100000
	dialog = wx.ProgressDialog("训练集词频统计中...", "训练集词频统计中", progressMax,\
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	keepGoing = True
	count = 0

	for one in sorted_result:
		line = "".join(one[0] + '\t' + str(one[1]) + '\n')
		file_out.write(line)
		count = count + 1#box
		keepGoing = dialog.Update(count)#box
	
	file_out.close()
	count = count + (progressMax-count)
	keepGoing = dialog.Update(count)
	dialog.Destroy()

def getFeatureVector():
	#从！！！！！训练集！！！！！中获取train vector

	file_out_dir = '.\\chapter\\'
	endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])
	everychapter = []

	progressMax = 100000
	dialog = wx.ProgressDialog("训练集生成特征向量中...", "训练集生成特征向量中...", progressMax,\
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
	keepGoing = True
	count = 0


	for loop in range(1,endlen):
		data = open('.\\ChapterWordSegmentation\\chap'+str(loop)+'-words.txt','r',encoding = 'utf-8')
		each_chapter = data.read()
		everychapter.append(each_chapter)
		data.close()
		count = count + 1#box
		keepGoing = dialog.Update(count)#box

	temp = open('.\\train-词.txt','r',encoding = 'utf-8')
	word_beg = temp.read()
	word_beg = word_beg.split(' ')
	temp.close()

    # 找出每一个回合都出现的词
	cleanwords = []
	for loop in range(1,endlen):
		data = open('.\\ChapterWordSegmentation\\chap'+str(loop)+'-words.txt','r',encoding = 'utf-8')
		words_list = list(set(data.read().split()))
		data.close()
		cleanwords.extend(words_list)
		count = count + 1#box
		keepGoing = dialog.Update(count)#box

	cleanwords_dict = coll.Counter(cleanwords)
	cleanwords_dict = {k:v for k, v in cleanwords_dict.items() if v >= 100}
	cleanwords_f = list(cleanwords_dict.keys())

	xuci = open('.\\文言虚词.txt','r',encoding = 'utf-8')
	xuci_list = xuci.read().split()
	xuci.close()
	featureVector = list(set(xuci_list + cleanwords_f))
	
	print("curious", featureVector)
	print("特征向量长度:",len(featureVector))
	try:
		featureVector.remove('\ufeff')
	except:
		pass

	file_out = open('.\\特征向量.txt','a',encoding = 'utf-8')
	for one in featureVector:
		line = "".join(one+ '\n')
		file_out.write(line)
		count = count + 1#box
		keepGoing = dialog.Update(count)#box
	file_out.close()

	count = count + (progressMax-count)
	keepGoing = dialog.Update(count)
	dialog.Destroy()



	return(featureVector)
