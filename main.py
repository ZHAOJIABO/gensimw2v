from gensim.models import word2vec
import nltk
### 2.2. Word2vec 训练

# 用生成器的方式读取文件里的句子
# 适合读取大容量文件，而不用加载到内存
class MySentences(object):
    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):
        for line in open(self.fname, 'r'):
            yield line.split()


# 模型训练函数
def w2vTrain(f_input, model_output):
    sentences = MySentences(DataDir + f_input)
    w2v_model = word2vec.Word2Vec(sentences,
                                  min_count=MIN_COUNT,
                                  workers=CPU_NUM,
                                  size=VEC_SIZE,
                                  window=CONTEXT_WINDOW
                                  )
    w2v_model.save(ModelDir + model_output)


# 训练
DataDir = "./"
ModelDir = "./ipynb_garbage_files/"
MIN_COUNT = 4
CPU_NUM = 2  # 需要预先安装 Cython 以支持并行
VEC_SIZE = 20
CONTEXT_WINDOW = 5  # 提取目标词上下文距离最长5个词

f_input = "bioCorpus_5000.txt"
model_output = "test_w2v_model"
# w2vTrain(f_input, model_output)

### 2.3. 查看结果

# 加载模型
# w2v_model = word2vec.Word2Vec.load(ModelDir + model_output)
#
# print(w2v_model.wv.most_similar('body'))  # 结果一般
#
# print(w2v_model.wv.most_similar('heart')) # 结果太差

# 数据集不够大时，停止词太多，解决方法：去除停止词

# 停止词

# showing info http://www.nltk.org/nltk_data/
from nltk.corpus import stopwords
StopWords = stopwords.words('english')

# print(StopWords[:20])


# 重新训练,去掉停用词了
# 模型训练函数
def w2vTrain_removeStopWords(f_input, model_output):
    sentences = list(MySentences(DataDir + f_input))
    for idx, sentence in enumerate(sentences):
        sentence = [w for w in sentence if w not in StopWords]
        sentences[idx] = sentence
    w2v_model = word2vec.Word2Vec(sentences, min_count=MIN_COUNT,
                                  workers=CPU_NUM, size=VEC_SIZE)
    w2v_model.save(ModelDir + model_output)


w2vTrain_removeStopWords(f_input, model_output)
w2v_model = word2vec.Word2Vec.load(ModelDir + model_output)

print(w2v_model.wv.most_similar('body')) # 结果一般