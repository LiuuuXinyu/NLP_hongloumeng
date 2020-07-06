import re
import jieba
import string
import collections as coll
jieba.load_userdict('./manual-dict.txt') 

class textProcesser:
	def __init__(self):
		pass

	def divideIntoChapter(self):
		'''
		注释预留位
		'''
		HLM = open('./红楼梦.txt',encoding='utf-8')
		each_line = HLM.readline()
		chapter_count = 0
		chapter_text = ''
		complied_rule = re.compile('第[一二三四五六七八九十百一二三四五六七八九十]+回')

		while each_line:
			#print(each_line)
			if re.findall(complied_rule,each_line):
				file_name = 'chap'+str(chapter_count)#第xxx回
				file_out = open('./HLMchapter/'+file_name+'.txt','a',encoding = 'utf-8')
				file_out.write(chapter_text)
				chapter_count += 1
				file_out.close()
				chapter_text = each_line
			else:
				chapter_text += each_line
			each_line = HLM.readline()

		file_name = 'chap'+str(120)#第120回
		file_out = open('./HLMchapter/'+file_name+'.txt','a',encoding = 'utf-8')
		file_out.write(chapter_text)
		HLM.close()

	# 对单个章节的分词
	def segmentation(self,text,text_count):
		file_name = 'chap'+str(text_count)+'-words.txt'
		file_out = open('./HLMChapterWordSegmentation/'+file_name,'a',encoding='utf-8')
		delset = string.punctuation
		line=text.readline()

		while line:
			seg_list = jieba.cut(line,cut_all = False)
			words = " ".join(seg_list)
			words = words.translate(delset) # 去除英文标点
			words = "".join(words.split('\n')) # 去除回车符
			words = self.delCNf(words) # 去除中文标点
			words = re.sub('[ \u3000]+',' ',words) # 去除多余的空格
			file_out.write(words)
			line = text.readline()

		file_out.close()
		text.close()

	def doChapterWordSegmentation(self):
		for loop in range(1,121):
			file_name = 'chap'+str(loop)+'.txt'
			file_in = open('./HLMChapter/'+file_name,'r',encoding = 'utf-8')
			self.segmentation(file_in,loop)
			file_in.close()

	# 去除中文字符函数
	def delCNf(self,line):
		regex = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9\s]')
		return regex.sub('', line)


	def count_words(self,text,textID):
		line = str(text)
		words = line.split()
		words_dict = coll.Counter(words) # 生成词频字典

		file_name = 'chap'+str(textID)+'-wordcount.txt'
		file_out = open('./HLMChapterWordCount/'+file_name,'a',encoding = 'utf-8')

		# 排序后写入文本
		sorted_result = sorted(words_dict.items(),key = lambda d:d[1],reverse = True)
		for one in sorted_result:
			line = "".join(one[0] + '\t' + str(one[1]) + '\n')
			file_out.write(line)

		file_out.close()



	def do_wordcount(self):
		for loop in range(1,121):
			file_name = 'chap'+str(loop)+'-words.txt'
			file_in = open('./HLMChapterWordSegmentation/'+file_name,'r',encoding = 'utf-8')
			line = file_in.readline()
			text = ''
			while line:
				text += line
				line = file_in.readline()
			self.count_words(text,loop)
			file_in.close()


if __name__ == '__main__':
	entity = textProcesser()
	entity.divideIntoChapter()
	entity.doChapterWordSegmentation()
	entity.do_wordcount()
