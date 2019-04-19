# -*- coding: utf-8 -*-
import config
import json
import os

DEBUG_FILE_READER_LINES = 10000
DEBUG = True

# 按行返回文件内容
def file_reader():
    os.chdir(config.DATA_FILE_PATH)
    flist = os.listdir(os.getcwd())
    for f in flist:
        with open(f, 'r') as fin:
            while True:
                line = fin.readline()
                if line:
                    yield line
                else:
                    break

# 函数包，按行调用函数func处理
def func_wrapper_one_arg(func):
    cnt = 0
    for line in file_reader():
        func(line)
        cnt += 1
        if cnt == DEBUG_FILE_READER_LINES and DEBUG:
            break

def func_wrapper_two_args(func, arg2):
    cnt = 0
    for line in file_reader():
        func(line, arg2)
        cnt += 1
        if cnt == DEBUG_FILE_READER_LINES and DEBUG:
            break


def get_features():
    # 获取训练数据中的特征
    all_feature_map = {}
    all_data_count = 0
    with open(config.TRAIN_FILE, 'r') as fin, open(config.FEATURE_OUT_FILE, 'w') as fout:
        line = fin.readline()
        while line:
            all_data_count += 1
            line = line.split(config.DATA_SPLIT)
            if len(line) != 2:
                continue
            # label = line[0]  # 标记
            feas = line[1]  # 特征串
            feaMap = json.loads(feas, encoding='utf-8')
            for k in feaMap.keys():
                if k not in all_feature_map.keys():
                    all_feature_map[k] = 1
                else:
                    all_feature_map[k] += 1
            line = fin.readline()
        fout.write(all_feature_map)
        fout.write("\n")
        fout.write(all_data_count)
    return all_feature_map, all_data_count

def add_feature_value_2_set(v, all_feature_map, k):
    if type(v).__name__ == 'list':
        for i in v:
            all_feature_map[k].add(i)
    else:
        all_feature_map[k].add(v)


# 取出分类特征中每列的不同项
def get_unique_elems_for_category_features_mapper(line, all_feature_map):
    line = line.split(config.DATA_SPLIT)
    if len(line) != 2:
        return
    # label = line[0]  # 标记
    feaMap = json.loads(line[1])
    for k, v in feaMap.items():
        if k in config.IGNORE_COLS or k in config.NUMERIC_COLS:
            continue
        if k not in all_feature_map.keys():
            all_feature_map[k] = set()
            add_feature_value_2_set(v, all_feature_map, k)
        else:
            add_feature_value_2_set(v, all_feature_map, k)


# 将数值特征加入特征map
def set_numeric_features_map(line, feature_map):
    line = line.split(config.DATA_SPLIT)
    if len(line) != 2:
        return
    feaMap = json.loads(line[1])
    for k, v in feaMap.items():
        if k in config.NUMERIC_COLS and k not in feature_map.keys():
            feature_map[k] = set()
            feature_map[k].add(1)


# 给每个特征的不同取值编码, 并返回特征个数
def set_index_for_features(all_feature_map):
    feature_id = 0
    all_feature_index_map = {}
    for f, vs in all_feature_map.items():
        if f not in all_feature_index_map.keys():
            all_feature_index_map[f] = {}
        for ff in vs:
            all_feature_index_map[f][ff] = feature_id
            feature_id += 1
    return all_feature_index_map, feature_id + 1


all_feature_map = {}
func_wrapper_two_args(get_unique_elems_for_category_features_mapper, all_feature_map)
func_wrapper_two_args(set_numeric_features_map, all_feature_map)
_, f_num = set_index_for_features(all_feature_map)
print f_num

