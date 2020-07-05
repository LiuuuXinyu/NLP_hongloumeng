# -*- coding: utf-8 -*-

import numpy as np
from sklearn.naive_bayes import MultinomialNB
import tools

x_train = tools.txt2matrix()


class result:
    def __inti__(self):
        pass

    def have_Xtrainset(self):
        Xtrainset = x_train
        Xtrainset = np.vstack((Xtrainset[19:29],Xtrainset[109:119]))
        return(Xtrainset)

    def as_num(self,x):
        y='{:.10f}'.format(x)
        return(y)

    def built_model(self):
        x_trainset = self.have_Xtrainset()
        y_classset = np.repeat(np.array([1,2]),[10,10])

        NBclf = MultinomialNB()
        NBclf.fit(x_trainset,y_classset) # 建立模型

        all_vector = x_train

        result = NBclf.predict(all_vector)
        print('前'+str(len(result[0:80]))+'回分类结果为：')
        print(result[0:80])
        print('后'+str(len(result[80:121]))+'回分类结果为：')
        print(result[80:121])

        # diff_chapter = [80,81,83,84,87,88,90,100]
        # for i in diff_chapter:
        #     tempr = NBclf.predict_proba(all_vector[i])
        #     print('第'+str(i+1)+'回的分类概率为： ')
        #     print(str(self.as_num(tempr[0][0]))+' '+str(self.as_num(tempr[0][1])))


if __name__ == '__main__':
    res = result()
    res.built_model()