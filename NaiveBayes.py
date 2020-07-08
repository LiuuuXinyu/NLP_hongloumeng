import numpy as np
from sklearn.naive_bayes import MultinomialNB
import os


def have_Xtrainset(x_train, trainrange):
    Xtrainset = x_train
    Xtrainset = Xtrainset[0:trainrange]#np.vstack((Xtrainset[0:100],Xtrainset[99:119]))
    return(Xtrainset)

def as_num(x):
    y='{:.10f}'.format(x)
    return(y)

def built_model(x_train,trainrange,labe1range,label1,label2):#label1range是最关键的
    x_trainset = have_Xtrainset(x_train,trainrange)
    y_classset = np.repeat(np.array([label1,label2]),[labe1range,trainrange-labe1range]) #####

    NBclf = MultinomialNB()
    NBclf.fit(x_trainset,y_classset) # 建立模型

    all_vector = x_train

    result = NBclf.predict(all_vector)


    file_out_dir_temp = '.\\chapter2\\'
    train_end_temp = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir_temp))])
    #每个读取一个名称，然后加上其label
    textall = ''
    
    for i in range(1,train_end_temp):
        with open(file_out_dir_temp+'chap'+str(i)+'.txt','r',encoding = 'utf-8') as f:
            line = f.readline()
            line=line.strip('\n')
            textall += line
            textall += ':\t'
            textall += str(result[trainrange-1+i])
            textall += '\n'

    print(textall)
    
    return result,textall
