from sklearn import svm
import numpy as np
import tools

x_train = tools.txt2matrix()

class SVM():

    def have_Xtrainset(self):
        Xtrainset = x_train
        Xtrainset = np.vstack((Xtrainset[9:29],Xtrainset[99:119]))
        return(Xtrainset)


    def built_model(self):
        x_trainset = self.have_Xtrainset()
        y_classset = np.repeat(np.array([1,2]),[20,20])
        svm_model = svm.LinearSVC()
        svm_model.fit(x_trainset,y_classset) # 建立模型

        all_vector = x_train

        result = svm_model.predict(all_vector)
        print('前'+str(len(result[0:80]))+'回分类结果为：')
        print(result[0:80])
        print('后'+str(len(result[80:121]))+'回分类结果为：')
        print(result[80:121])

if __name__ == '__main__':
    res_svm = SVM()
    res_svm.built_model()