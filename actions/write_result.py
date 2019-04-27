# -*-coding:utf-8 -*-
from config.public_data import *
from utils.gen_time_str import *


def write_result(excel_obj, sheet_obj, response_code, response_data, test_result, row_no):
    """将响应码，响应数据，测试结果写入sheet_obj指定的sheet中"""
    # 写入响应码
    excel_obj.writeCell(sheet=sheet_obj, content=response_code, rowNo=row_no, colsNo=CASE_RESPONSE_CODE_COL)
    # 写入响应数据
    excel_obj.writeCell(sheet=sheet_obj, content="%s" % response_data, rowNo=row_no, colsNo=CASE_RESPONSE_DATA_COL)
    # 写入测试结果
    if test_result:
        excel_obj.writeCell(sheet=sheet_obj, content="fail", rowNo=row_no, colsNo=CASE_STATUS_COL, style='red')
        excel_obj.writeCell(sheet=sheet_obj, content="%s" % test_result, rowNo=row_no, colsNo=CASE_ERROR_INFO_COL)
    else:
        excel_obj.writeCell(sheet=sheet_obj, content="pass", rowNo=row_no, colsNo=CASE_STATUS_COL, style='green')
        excel_obj.writeCell(sheet=sheet_obj, content='', rowNo=row_no, colsNo=CASE_ERROR_INFO_COL)
    # 写入执行时间
    excel_obj.writeCell(sheet=sheet_obj, content=get_datetime(), rowNo=row_no, colsNo=CASE_EXECUTE_TIME_COL)




