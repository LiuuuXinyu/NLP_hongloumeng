import numpy as np
import re
import os

def txt2matrix():
	'''
	生成120*shape的矩阵，为频率矩阵
	'''
	featurevector_dir = '.\\特征向量.txt'
	feature_data = open(featurevector_dir,'r',encoding = 'utf-8')
	feature_list = list(feature_data.read().split())
	print("feature_list",feature_list)

	#分两拨干这个事情
	file_out_dir_1 = '.\\chapter\\'
	train_end_1 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_1))])
	#print("hello",train_end_1)
	file_out_dir_2 = '.\\chapter2\\'
	train_end_2 = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_2))])

	matrix = np.zeros((train_end_1+train_end_2-2,len(feature_list)))

	
	
	for k in range(1,train_end_1):
		file_dir = '.\\ChapterWordCount\\chap'+str(k)+'-wordcount.txt'
		file_data = open(file_dir,'r',encoding = 'utf-8')
		lines = file_data.readlines()
		for line in lines:
			for i in range(len(feature_list)):
				if feature_list[i] in line:
					temp = [int(s) for s in line.split() if s.isdigit()]
					matrix[k-1,i] += temp[0]
	
	
	for k in range(1,train_end_2):
		file_dir = '.\\ChapterWordCount2\\chap'+str(k)+'-wordcount.txt'
		file_data = open(file_dir,'r',encoding = 'utf-8')
		lines = file_data.readlines()
		for line in lines:
			for i in range(len(feature_list)):
				if feature_list[i] in line:
					temp = [int(s) for s in line.split() if s.isdigit()]
					matrix[train_end_1+k-2,i] += temp[0]						#there are some changes

	print(matrix)
	print("matrix.shape",matrix.shape)
	#matrix前1-70为曹雪芹，71-100为高鹗的81-110；
	#matrix101-110为曹雪芹test，111-120为高鹗test
	return matrix





if __name__ == '__main__':
	pass
	#txt2matrix()