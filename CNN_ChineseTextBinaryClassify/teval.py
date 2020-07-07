# coding:utf-8
# ! /usr/bin/env python
#20200707
import tensorflow as tf
import numpy as np
import os
import time
import datetime
from CNN_ChineseTextBinaryClassify import data_helpers
from text_cnn import TextCNN
from tensorflow.contrib import learn
import csv
import fenci_jieba

tf.flags.DEFINE_string("positive_data_file", '.\\fenci\\cao.txt', "Data source for the positive data.")
tf.flags.DEFINE_string("negative_data_file",'.\\fenci\\gao.txt' , "Data source for the positive data.")


# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
# 填写训练获得模型的存储位置
tf.flags.DEFINE_string("checkpoint_dir", ".\\runs\\1594125564\\checkpoints\\", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", True, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

def eval_test(real_data_path,bullshit_data_path,relative_path):
    #def eval_model(self,):
    # import sys
    # reload(sys)
    # sys.setdefaultencoding("utf-8")

    # ============
    # 命令行执行：python eval.py --eval_train --checkpoint_dir="./runs/1541671904/checkpoints/"
    # 预测结果在runs/1541671904/prediction.csv中。
    # ============

    # 参数：我们这里使用命令行传入参数的方式执行该脚本
    #real_data_path = "./fenci/real_data_test.txt"
    #bullshit_data_path = "./fenci/bullshit_data_test.txt"
    #relative_path = "./runs/1594054688/checkpoints/"

    FLAGS = tf.flags.FLAGS
    FLAGS.positive_data_file = real_data_path
    FLAGS.negative_data_file = bullshit_data_path
    FLAGS.checkpoint_dir = relative_path
    #print(FLAGS)
    # CHANGE THIS: Load data. Load your own data here
    if FLAGS.eval_train:
        #print(FLAGS.eval_train)
        #print(FLAGS.positive_data_file)
        #print(FLAGS.negative_data_file)
        #x_raw, y_test = data_helpers.load_data_and_labels(FLAGS.positive_data_file, FLAGS.negative_data_file)

        x_raw = data_helpers.load_single_file(FLAGS.positive_data_file)

        #y_test = np.argmax(y_test, axis=1)
        print('*********************************in here****************************************')

    else :
        print('something wrong')
    '''
    else:
        # x_raw = ["a masterpiece four years in the making", "everything is off."]
        # y_test = [1, 0]
        print('++++++++++++++++++++++what about here++++++++++++++++++++++++++++')
        x1 = '''
         #三个 三个臭皮匠 臭皮 臭皮匠 皮匠 顶 个 诸葛 诸葛亮   以此 以此类推 此类 类推   如果 能 把 一个 个人 跟 另外 100 万 人 的 大脑 连接 连接起来 接起 起来   就 会 诞生   超级 大脑
         #正因如此 如此   现在 才 出现 了 好几 好几家 几家 公司 争相 开发 脑 机界面 界面   希望 把 人 的 思维 与 机器 连接 连接起来 接起 起来   如果 能够 率先 将 笔记 笔记本 笔记本电脑 电脑 的 功能 植入 你 的 大脑   就 将 为 人们 开辟 一条 道路   使 之 得以 随意 通过 无缝 渠道 与 任何 任何人 何人   甚至 任何 东西   交换 信息
         #目前 有 两位 IT 行业 的 大佬 都 在 参与 这场 角逐   他们 分别 是 特斯 特斯拉 斯拉 创始 创始人 埃 隆   马斯克  Elon Musk  和 Facebook 创始 创始人 人马 马克   扎克 伯格  Mark Zuckerberg   他们 两 人 的 项目 分别 别名 名为 Neuralink 和 Building 8  而 据 知情 知情人 情人 人士 透露   这 两个 项目 都 需要 对 大脑 进行 外科 外科手术 手术
         #然而   还有 一些 没有 那么 野心 野心勃勃 勃勃 勃勃的 微创 方式   也 可以 解决 脑 机界面 界面 问题   只 需要 把 脑电波 电波 的 数据 转化 转化成 化成 简单 的 指令   然后 由 应用 或 设备 进行 处理 即可   一家 名为 Nuro 的 创业 公司 就 采取 了 这种 方式   他们 希望 借助 自己 的 软件 软件平台 平台   让 那些 因为 严重 受伤 或 疾病 而 丧失 交流 能力 的 人 恢复 这种 能力
    '''
        x_raw = [x1]
        y_test = [1]
    '''
    # Map data into vocabulary
    vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
    print("checkpoint_file========", checkpoint_file)

    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))

            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

            # 存储模型预测结果
            all_predictions = []
            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])

    # Print accuracy if y_test is defined
    '''
    y_test = []
    if y_test is not None:
        correct_predictions = float(sum(all_predictions == y_test))

        print("Total number of test examples: {}".format(len(y_test)))
        print("Accuracy: {:g}".format(correct_predictions / float(len(y_test))))
        print()
    '''
    # [0,1]
    # [1,0]

    # 将二分类的0，1标签转化为中文标签
    y = []
    sum_ai = 0
    sum_real = 0
    for i in all_predictions:
        if i == 0.0:
            y.append("[AI生成]")
            sum_ai = sum_ai+1
        else:
            y.append("[真实]")
            sum_real = sum_real+1
    # 把预测的结果保存到本地
    print('sum_real = ',sum_real)
    print('sum_ai = ',sum_ai)
    if sum_ai >= 3 * sum_real:
        print('This article is from AI')
        print('all prediction long',len(all_predictions))
        return 'AI'

    else :
        print('This article is from person')
        print('all prediction long',len(all_predictions))
        return 'Person'

    '''
    predictions_human_readable = np.column_stack((y, np.array(x_raw)))
    out_path = os.path.join(FLAGS.checkpoint_dir, "..", "prediction.csv")
    print("Saving evaluation to {0}".format(out_path))
    with open(out_path, 'w',encoding='gb18030') as f:
    #with open(out_path, 'w') as f:
        #f.encoding = 'gbk'
        csv.writer(f).writerows(predictions_human_readable)
    '''

def all_test(data_path,mode2):
    result_list = []


    todir = ".\\fenci\\"
    stopWordFile = "stop_words_new.txt"
    #mode2 = 1
    if mode2 == 0:
        file_out_dir = '.\\chapter\\'
        data_out_dir = ".\\cnn_train_file\\"
        endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])

    elif mode2 == 1:
        file_out_dir = '.\\chapter2\\'
        data_out_dir = ".\\cnn_test_file\\"
        endlen = sum([len(x) for _, _, x in os.walk(os.path.dirname(file_out_dir))])

    for loop in range(1,endlen):
        file_name = 'chap'+str(loop)+'.txt'
        #file_in = open(file_out_dir+file_name,'r',encoding = 'utf-8')


        # 一次只能对一个文档进行分词
        #file = "chap5.txt"
        # file = "交通214.txt"
        infile = open(os.path.join(file_out_dir, file_name), 'r', encoding='UTF-8')
        outfile = open(os.path.join(data_out_dir, file_name), 'w+', encoding='UTF-8')
        # 这里加载停用词
        stopwords = [line.strip() for line in open(os.path.join(todir, stopWordFile), 'r', encoding='UTF-8').readlines()]
        fenci_jieba.FenCi(infile, outfile, stopwords)
        infile.close()
        outfile.close()
        temp = eval_test(data_out_dir+file_name,data_out_dir+file_name,data_path)
        #file_in.close()
        result_list.append(temp)
    print(result_list)
    return result_list


def main():
    real_test_data_path = ".\\fenci\\chap5.txt"
    bullshit_test_data_path = ".\\fenci\\bullshit_data_test.txt"
    relative_test_path = ".\\runs\\1594125564\\checkpoints\\"
    all_test(relative_test_path,0)
    #eval_test(real_test_data_path,bullshit_test_data_path,relative_test_path)

if __name__ == '__main__':
    main()
