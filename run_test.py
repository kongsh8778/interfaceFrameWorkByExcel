# -*-coding:utf-8 -*-

from utils.parse_excel import ParseExcel
from config.public_data import *
from actions.get_rely import GetRelyData
from utils.http_client import HTTPClient
from actions.check_result import CheckResult
from actions.write_result import write_result
from actions.store_data import StoreRelyData

def main():
    # 获取测试excel对象
    excel_obj = ParseExcel()
    # 将文件加载到内存
    excel_obj.loadWorkBook(excel_Path)
    # 获取测试用例sheet对象
    sheet_obj = excel_obj.getSheetByName(test_case_sheet_name)
    # 获取所有待执行的测试用例的列对象
    active_test_case_list = excel_obj.getColumn(sheet_obj, API_ACTIVE_COL)
    # print(active_test_case_list)
    # 遍历所有要执行的测试用例，组织依赖数据，发送接口请求，判断接口响应，写入测试结果
    # 去掉标题行
    for row_no, row in enumerate(active_test_case_list[1:], start=2):
        # 切换回API这个sheet
        sheet_obj = excel_obj.getSheetByName(test_case_sheet_name)
        # 判断是否需要执行
        if row.value.lower() == 'y':
            # 获取apiName
            api_name = excel_obj.getCellOfValue(sheet_obj, rowNo=row_no, colsNo=API_NAME_COL)
            # 获取RequestUrl
            request_url = excel_obj.getCellOfValue(sheet_obj, rowNo=row_no, colsNo=API_REQUEST_URL_COL)
            # 获取RequestMethod
            request_method = excel_obj.getCellOfValue(sheet_obj, rowNo=row_no, colsNo=API_REQUEST_METHOD_COL)
            # 获取paramsType
            params_type = excel_obj.getCellOfValue(sheet_obj, rowNo=row_no, colsNo=API_PARAMS_TYPE_COL)
            # 获取APITestCase
            API_test_case = excel_obj.getCellOfValue(sheet_obj, rowNo=row_no, colsNo=API_TEST_FILE_NAME_COL)
            print(api_name, request_url, request_method, params_type, API_test_case)

            # 切换到API_test_case指定的sheet中执行具体的测试案例
            sheet_obj = excel_obj.getSheetByName(API_test_case)
            # 获取是否执行的列对象
            active_test_step_list = excel_obj.getColumn(sheet_obj, CASE_ACTIVE_COL)
            for num, test_step in enumerate(active_test_step_list[1:], start=2):
                # y的话才执行
                if test_step.value.lower() == "y":
                    test_step_row_obj = excel_obj.getRow(sheet_obj, num)
                    # 获取RequestData
                    request_data = test_step_row_obj[CASE_REQUEST_DATA_COL - 1].value
                    # 获取RelyData
                    rely_data = test_step_row_obj[CASE_RELY_DATA_COL - 1].value
                    # 获取DataStore
                    data_store = test_step_row_obj[CASE_DATA_STORE_COL - 1].value
                    # 获取CheckPoint
                    check_point = test_step_row_obj[CASE_CHECKPOINT_COL - 1].value
                    # print(request_data, rely_data, data_store, check_point)

                    # 有依赖数据的话要处理依赖数据
                    if rely_data and request_data:
                        request_data = GetRelyData.get(request_data, rely_data)
                         # print(request_data)

                    # request_data如果是字符串类型的字典时要先执行eval转换为字典
                    if isinstance(request_data, str) and request_data[0] == '{' and request_data[-1] == '}':
                        request_data = eval(request_data)
                    # 发送接口请求
                    print("************%s"%request_data)
                    response = HTTPClient.request(request_url, request_method, params_type, request_data)
                    # 如果请求成功，存储依赖数据
                    if response.status_code < 400:
                        if data_store:
                            StoreRelyData().store(api_name, num-1, request_data, response.json(), eval(data_store))

                    # 检测接口响应数据
                    err = {}
                    if check_point:
                        err = CheckResult().check(response.json(), eval(check_point))
                    # 测试结果写入到excel中
                    write_result(excel_obj, sheet_obj, response.status_code, response.json(), err, num)
                else:
                    print("#++++++++【%s-->%s】中第%d条测试步骤忽略执行！" % (api_name, API_test_case, num - 1))

        else:
            print("#++++++++【%s】中第%d条测试案例忽略执行！" % (test_case_sheet_name, row_no - 1))


if __name__ == "__main__":
    main()
