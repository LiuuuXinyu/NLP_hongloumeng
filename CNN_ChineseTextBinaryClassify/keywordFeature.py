import jieba
import jieba.analyse
import jieba.posseg as posseg
import time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']


def maxKWords(file_dir):
	'''
	注释预留位
	'''
	with open(file_dir, "r", encoding='utf-8') as f:
		lines = f.readlines()
	#n名词 r代词 a形容词 d副词 v动词 p介词 c连词 u助词 y语气词
	keywords = jieba.analyse.extract_tags(str(lines), topK = 5, withWeight=True,allowPOS=('n','r','a','p','c','u','y'))#allowPOS为只筛选指定词性的词

	print(keywords)
	return keywords

if __name__ == '__main__':
	
	file_dir = "./RMA.txt"
	maxKWords(file_dir)