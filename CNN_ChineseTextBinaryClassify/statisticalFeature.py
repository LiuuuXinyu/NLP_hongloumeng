#词性特征，无法区分
import jieba
import jieba.posseg as posseg
import time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']

#def dataPreprocess():

def wordPosseg(text,dic_count):
	'''
	对一句话进行词性分析

	output:

		- ：[pair('word','pos'),pair('word','pos'),…]
	'''
	seg = posseg.lcut(text)
	for i in range(len(seg)):
		word, value = seg[i]
		try:
			dic_count[value] += 1
		except:
			dic_count[value] = 1
	
def wordCount(file_dir, Krange):#K代表topK，是可以控制的
	'''
	注释预留
	'''
	with open(file_dir, "r", encoding='utf-8') as f:
			lines = f.readlines()
	
	#统计词性特征
	print("开始执行计时：")
	starttime = time.time()
	dic_count = {}
	for line in lines:
		wordPosseg(line, dic_count)
	endtime = time.time()
	print("执行用时：", endtime-starttime)

	#top K建表
	char2chinese = {"a":"形容词","ad":"副形词","ag":"形语素","an":"名形词","b":"区别词","c":"连词","d":"副词","df":"不要",
	"dg":"副语素","e":"叹词","f":"方位词","g":"语素","h":"前接成分","i":"成语","j":"简称略语","k":"后接成分",
	"l":"习用语","m":"数词","mg":"数语素","mq":"数量词","n":"名词","ng":"名语素","nr":"人名","nrfg":"古近代人名",
	"nrt":"外国人名","ns":"地名","nt":"机构团体","nz":"其他专名","o":"拟声词","p":"介词","q":"量词","r":"代词",
	"rg":"代语素","rr":"代词","rz":"代词","s":"处所词","t":"时间词","tg":"时间语素","u":"助词","ud":"得",
	"ug":"过","uj":"的","ul":"了","uv":"地","uz":"着","v":"动词","vd":"副动词","vg":"动语素",
	"vi":"动词","vn":"名动词","vq":"动词","x":"非语素字","y":"语气词","yg":"语气词","z":"状态词","zg":"zg","eng":"英文"
	}


	dic_count_list = sorted(dic_count.items(), key=lambda kv:(kv[1], kv[0]), reverse = True)
	word_keys = []
	word_values = []
	if Krange != -1:
		for i in range(Krange[0],Krange[1]):# k range 范围内
			word_keys.append(char2chinese[dic_count_list[i][0]])
			word_values.append(int(dic_count_list[i][1]))
	else:
		for i in range(len(dic_count_list)):# k range 范围内
			word_keys.append(char2chinese[dic_count_list[i][0]])
			word_values.append(int(dic_count_list[i][1]))

	print(word_keys)
	print(word_values)
	
	plt.axes(aspect = 1)
	plt.pie(x=word_values, labels = word_keys, autopct='%.0f%%', shadow = True)
	plt.show()#save在本地后打印输出，是否可行


if __name__ == '__main__':

	file_dir2 = "./红楼梦1-80utf-8.txt"
	wordCount(file_dir2,  Krange = -1)


