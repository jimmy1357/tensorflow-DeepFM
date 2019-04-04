"""
A data parser for Porto Seguro's Safe Driver Prediction competition's dataset.
URL: https://www.kaggle.com/c/porto-seguro-safe-driver-prediction
"""
import pandas as pd


class FeatureDictionary(object):
    def __init__(self, trainfile=None, testfile=None,
                 dfTrain=None, dfTest=None, numeric_cols=[], ignore_cols=[]):
        assert not ((trainfile is None) and (dfTrain is None)), "trainfile or dfTrain at least one is set"
        assert not ((trainfile is not None) and (dfTrain is not None)), "only one can be set"
        assert not ((testfile is None) and (dfTest is None)), "testfile or dfTest at least one is set"
        assert not ((testfile is not None) and (dfTest is not None)), "only one can be set"
        self.trainfile = trainfile
        self.testfile = testfile
        self.dfTrain = dfTrain
        self.dfTest = dfTest
        self.numeric_cols = numeric_cols
        self.ignore_cols = ignore_cols
        self.gen_feat_dict()

    def gen_feat_dict(self): # 将所有特征编码
        if self.dfTrain is None:
            dfTrain = pd.read_csv(self.trainfile)
        else:
            dfTrain = self.dfTrain
        if self.dfTest is None:
            dfTest = pd.read_csv(self.testfile)
        else:
            dfTest = self.dfTest
        df = pd.concat([dfTrain, dfTest])#把测试集追加在训练集之后(即：合并)
        self.feat_dict = {} # 将所有特征编码
        tc = 0
        for col in df.columns:
            if col in self.ignore_cols:
                continue
            if col in self.numeric_cols:
                # map to a single index
                self.feat_dict[col] = tc # 给每列编码一个id
                tc += 1
            else:
                us = df[col].unique()# 取出当前列(分类特征)中不同的项
                self.feat_dict[col] = dict(zip(us, range(tc, len(us)+tc))) # 给当前列的每个分类分配一个id，构造成一个字典: key为分类,value为id
                tc += len(us)
        self.feat_dim = tc # 特征个数


class DataParser(object):
    def __init__(self, feat_dict):
        self.feat_dict = feat_dict

    def parse(self, infile=None, df=None, has_label=False):
        assert not ((infile is None) and (df is None)), "infile or df at least one is set"
        assert not ((infile is not None) and (df is not None)), "only one can be set"
        if infile is None:
            dfi = df.copy()
        else:
            dfi = pd.read_csv(infile)
        if has_label:
            y = dfi["target"].values.tolist() # 取出target列(label)
            dfi.drop(["id", "target"], axis=1, inplace=True) # 删除列id , 列target, inplace=True表示直接替换原数组，将删除指定列之后的数组赋值给原始数组，返回原始数组(即，直接在原数组上执行删除并保存)
        else:
            ids = dfi["id"].values.tolist() # 取出id列
            dfi.drop(["id"], axis=1, inplace=True)
        # dfi for feature index
        # dfv for feature value which can be either binary (1/0) or float (e.g., 10.24)
        dfv = dfi.copy() # Python中赋值操作会被解释为设置别名，不会解释为拷贝, 而这里的copy是拷贝，即对拷贝后的对象的操作，不会影响拷贝前的对象
        for col in dfi.columns:
            if col in self.feat_dict.ignore_cols: # 从dfi中删除需要被忽略的列
                dfi.drop(col, axis=1, inplace=True)
                dfv.drop(col, axis=1, inplace=True)
                continue
            if col in self.feat_dict.numeric_cols:
                dfi[col] = self.feat_dict.feat_dict[col] # dfi的数值列中记录数值特征的特征id
            else:
                dfi[col] = dfi[col].map(self.feat_dict.feat_dict[col]) # 把当前列(分类特征)值替换成对应的特征id
                dfv[col] = 1. # 将分类特征值赋值为1

        # list of list of feature indices of each sample in the dataset
        Xi = dfi.values.tolist() # dfi中保存的是特征的id
        # list of list of feature values of each sample in the dataset
        Xv = dfv.values.tolist() # dfv中保存的是特征的值
        if has_label:
            return Xi, Xv, y
        else:
            return Xi, Xv, ids

