import os

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def delall():
    try:
        del_file('.\\chapter\\')
    except:
        print("ERROR")
    try:    
        del_file('.\\chapter2\\')
    except:
        print("ERROR")
    try:
        del_file('.\\ChapterWordCount\\')
    except:
        print("ERROR")
    try:
        del_file('.\\ChapterWordCount2\\')
    except:
        print("ERROR")
    try:
        del_file('.\\ChapterWordSegmentation\\')
    except:
        print("ERROR")
    try:
        del_file('.\\ChapterWordSegmentation2\\')
    except:
        print("ERROR")
    try:
        os.remove('.\\train-词.txt')
    except:
        print("ERROR")
    try:
        os.remove('.\\词频.txt')
    except:
        print("ERROR")
    try:
        os.remove(".\\特征向量.txt")
    except:
        print("ERROR")


if __name__ == '__main__':

    pass