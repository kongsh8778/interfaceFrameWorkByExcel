# -*-coding:utf-8 -*-

import re


class CheckResult(object):
    """检查响应报文和检查点中要求的是否一致"""
    type_dict = {
        'N': 'int',
        'S': 'str',
        'L': 'list',
        'T': 'tuple'
    }

    @staticmethod
    def check(response, check_point):
        """
        checkPoint: {"code":"00","userid":{"type":"N"},"id":{"value":"\d+"}}
        检查点分为3种格式：
        1、完全相等
        2、模糊检查，只检查类型
        3、包含
        :param response: 响应报文
        :param check_point: 检查点
        :return: 字典
        """
        # 存放比较失败的键值对
        err_dict = {}
        for k, v in check_point.items():
            if k not in response:
                err_dict[k] = 'Not found in response'
                continue
            if isinstance(v, str):
                # 说明是全等匹配
                if v != response[k]:
                    err_dict[k] = response[k]
            elif isinstance(v, dict):
                value = response[k]
                # 说明是模糊匹配
                if "type" in v:
                    # 说明是类型匹配
                    type_str = v["type"]
                    if type_str in CheckResult.type_dict:
                        if not isinstance(value, eval(CheckResult.type_dict[type_str])):
                            err_dict[k] = value
                    else:
                        print("待检查的类型%s不在%s中" % (type_str, CheckResult.type_dict))
                elif "value" in v:
                    # 说明是正则匹配
                    reg_exp = v["value"]
                    if not re.match(reg_exp, value):
                        err_dict[k] = value
        return err_dict


if __name__ == "__main__":
    checkPoint = {"code": "00", "userid": {"type": "N"}, "id": {"value": "^\d+$"}}
    response = {"code": "00", "userid": 45, "id": "a122"}
    response = {'data': [{'content': 'python port test', 'title': 'python'}], 'code': '00', 'userid': 32874}
    checkPoint = {"code": "00", "userid": {"type": "N"}}
    print(CheckResult.check(response, checkPoint))
