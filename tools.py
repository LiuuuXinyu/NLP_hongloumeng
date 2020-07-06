import numpy as np
import re

def txt2matrix():
	'''
	生成120*shape的矩阵，为频率矩阵
	'''
	featurevector_dir = './红楼梦-特征向量.txt'
	feature_data = open(featurevector_dir,'r',encoding = 'utf-8')
	feature_list = list(feature_data.read().split())
	print("feature_list",feature_list)

	matrix = np.zeros((120,len(feature_list)))

	for k in range(1,121):
		file_dir = './HLMChapterWordCount/chap'+str(k)+'-wordcount.txt'
		file_data = open(file_dir,'r',encoding = 'utf-8')
		lines = file_data.readlines()
		for line in lines:
			for i in range(len(feature_list)):
				if feature_list[i] in line:
					temp = [int(s) for s in line.split() if s.isdigit()]
					matrix[k-1,i] += temp[0]
	
	print(matrix)
	print("matrix.shape",matrix.shape)
	return matrix

if __name__ == '__main__':
	txt2matrix()