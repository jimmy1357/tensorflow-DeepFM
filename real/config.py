# -*- coding: utf-8 -*-
# set the path-to-files
DATA_FILE_PATH = 'E:/datas/training_data/user_datas'
TRAIN_FILE = "./data/train.csv"
TEST_FILE = "./data/test.csv"

DATA_SPLIT = '\t'
FEATURE_OUT_FILE = ""

SUB_DIR = "./output"

#NUM_SPLITS = 3
RANDOM_SEED = 2019

# 22 fields
ALL_COLS = {'rtContKwords': 5834941, 'rtcSeries': 9333518, 'rtSeries': 9789693, 'rtTitleKwords': 5816749,
            'uicSeries': 11714661, 'uiSeries': 11733037, 'chooseCar': 10731598, 'userGroup': 10731598,
            'rtAuthors': 19, 'itemFeatures': 12109999, 'itemKey': 12109999, 'biztype': 12109999,
            'netstate': 12109414, 'rtBrands': 5258333, 'devicetype': 6681524, 'rtTopics': 8565933,
            'rtBizTypes': 7147001, 'activeLevel': 10731598, 'priceLevel': 10731598, 'deviceid': 12109999,
            'nowhour': 11636457, 'clickItems': 10099853}

# types of columns of the dataset dataframe
CATEGORICAL_COLS = [
    'biztype', 'netstate', 'nowhour', 'devicetype',
    'chooseCar', 'userGroup', 'itemKey', 'activeLevel', 'priceLevel'
]

MULTI_VALUE_COLS = [
    'uiSeries', 'uicSeries', 'rtBizTypes', 'rtContKwords', 'rtcSeries',
    'rtSeries', 'rtTitleKwords', 'rtBrands', 'rtTopics', 'clickItems'
]

NUMERIC_COLS = [
    'itemFeatures'  # itemFeatures多维特征
]

IGNORE_COLS = [
    'deviceid', 'rtAuthors'
]
