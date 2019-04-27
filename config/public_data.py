# -*-coding:utf-8 -*-

import os

# 工程根路径
base_dir = os.path.dirname(os.path.dirname(__file__))
# 测试数据excel路径
excel_Path = os.path.join(base_dir, "test_data", "inter_test_data.xlsx")
# 测试用例入口sheet名
test_case_sheet_name = "API"
# 保存请求参数的数据依赖
REQUEST_DATA = {}
# 保存响应对象的数据依赖
RESPONSE_DATA = {}

"""测试用例sheet对应的列号"""
API_NAME_COL = 2
API_REQUEST_URL_COL = 3
API_REQUEST_METHOD_COL = 4
API_PARAMS_TYPE_COL = 5
API_TEST_FILE_NAME_COL = 6
API_ACTIVE_COL = 7

CASE_REQUEST_DATA_COL = 1
CASE_RELY_DATA_COL = 2
CASE_RESPONSE_CODE_COL = 3
CASE_RESPONSE_DATA_COL = 4
CASE_DATA_STORE_COL = 5
CASE_CHECKPOINT_COL = 6
CASE_ACTIVE_COL = 7
CASE_STATUS_COL = 8
CASE_ERROR_INFO_COL = 9
CASE_EXECUTE_TIME_COL = 10

if __name__ == "__main__":
    print(base_dir)
