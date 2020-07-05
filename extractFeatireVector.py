import jieba
import re
import string
import collections as coll
jieba.load_userdict('.\\manual-dict.txt') # 导入搜狗的红楼梦词库，这步遇到一个小问题

class featureVector:
	def __init__(self):
		pass


	def delCNf(self,line):
		regex = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9\s]')
		return regex.sub('', line)


	# 对整篇文章分词，注意这里是整篇文章
	def cut_words(self):
		HLM = open('.\\红楼梦.txt','r',encoding = 'utf-8')
		file_out = open('.\\红楼梦-词.txt','a',encoding = 'utf-8')
		delset = string.punctuation
		line = HLM.readline()

		while line:
			seg_list = jieba.cut(line,cut_all = False)
			words = ' '.join(seg_list)
			words = words.translate(delset) # 去除英文标点
			words = "".join(words.split('\n')) # 去除回车符
			words = self.delCNf(words) # 去除中文标点
			words = re.sub('[ \u3000]+',' ',words) # 去除多余的空格
			file_out.write(words)
			line = HLM.readline()

		file_out.close()
		HLM.close()


	def count_words(self):
		data = open('.\\红楼梦-词.txt','r',encoding = 'utf-8')
		line = data.read()
		data.close()
		words = line.split()
		words_dict = coll.Counter(words) # 生成词频字典

		file_out = open('.\\红楼梦-词频.txt','a',encoding = 'utf-8')

		# 排序后写入文本
		sorted_result = sorted(words_dict.items(),key = lambda d:d[1],reverse = True)
		for one in sorted_result:
			line = "".join(one[0] + '\t' + str(one[1]) + '\n')
			file_out.write(line)

		file_out.close()

	def getFeatureVector(self):
		# 将分词后的120个章节文本放入一个列表中
		everychapter = []
		for loop in range(1,121):
			data = open('.\\HLMChapterWordSegmentation\\chap'+str(loop)+'-words.txt','r',encoding = 'utf-8')
			each_chapter = data.read()
			everychapter.append(each_chapter)
			data.close()

		temp = open('.\\红楼梦-词.txt','r',encoding = 'utf-8')
		word_beg = temp.read()
		word_beg = word_beg.split(' ')
		temp.close()

        # 找出每一个回合都出现的词
		cleanwords = []
		for loop in range(1,121):
			data = open('.\\HLMChapterWordSegmentation\\chap'+str(loop)+'-words.txt','r',encoding = 'utf-8')
			words_list = list(set(data.read().split()))
			data.close()
			cleanwords.extend(words_list)

		cleanwords_dict = coll.Counter(cleanwords)
		cleanwords_dict = {k:v for k, v in cleanwords_dict.items() if v >= 110}
		cleanwords_f = list(cleanwords_dict.keys())

		xuci = open('.\\文言虚词.txt','r',encoding = 'utf-8')
		xuci_list = xuci.read().split()
		xuci.close()
		featureVector = list(set(xuci_list + cleanwords_f))
		print("curious", featureVector)
		try:
			featureVector.remove('\ufeff')
		except:
			pass

		file_out = open('.\\红楼梦-特征向量.txt','a',encoding = 'utf-8')
		for one in featureVector:
			line = "".join(one+ '\n')
			file_out.write(line)
		file_out.close()
		return(featureVector)


if __name__ == '__main__':
	entity = featureVector()
	entity.cut_words()
	entity.count_words()
	entity.getFeatureVector()