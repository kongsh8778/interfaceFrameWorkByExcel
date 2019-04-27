# -*-coding:utf-8 -*-

from config.public_data import REQUEST_DATA, RESPONSE_DATA


class GetRelyData(object):
    """处理依赖数据的类"""
    @staticmethod
    def __store(request_data, rely_data):
        """
        :param request_data:存储获取的依赖数据
        :param rely_data:依赖数据格式, 字典类型，遍历该字典从REQUEST_DATA或 RESPONSE_DATA取数据
        :return:返回一个字典
        """
        for key, value in rely_data.items():
            # 从REQUEST_DATA中取数据
            if key.lower() == "request":
                print(REQUEST_DATA)
                for k, v in value.items():
                    sheet_name, case_no = v.split("->")
                    if k in REQUEST_DATA[sheet_name][case_no]:
                        # 从嵌套的字典中获取依赖参数的值
                        request_data[k] = REQUEST_DATA[sheet_name][case_no][k]
            # 从RESPONSE_DATA中取数据
            elif key.lower() == "response":
                for k, v in value.items():
                    sheet_name, case_no = v.split("->")
                    # print(RESPONSE_DATA)
                    if k in RESPONSE_DATA[sheet_name][case_no]:
                        # 从嵌套的字典中获取依赖参数的值
                        request_data[k] = RESPONSE_DATA[sheet_name][case_no][k]

    @staticmethod
    def get(request_data, rely_data):
        """
        从rely_data获得所有依赖的数据，可能来自请求报文，也可能来自响应报文
        :param request_data: 获取到依赖数据后添加到request_data中,分两种类型：字典或字符串(&连接)
        :param rely_data: 依赖信息获取来源
        :return:
        """
        # 如果输入参数有一个为空的话就直接返回None
        if not request_data or not rely_data:
            return None
        # 从excel读出的类型是字符串，转换为原始的数据类型
        try:
            request_data = eval(request_data)
        except SyntaxError as e:
            pass
        if rely_data:
            rely_data = eval(rely_data)
        # print(type(request_data), type(rely_data))

        # request_data为字符串类型数据，先转换为临时的字典方便统一处理
        if isinstance(request_data, str):
            # 按&切割为k=v格式的字符串
            items_list = request_data.split('&')
            k_v_dict = {}
            for item in items_list:
                k, v = item.split('=')
                k_v_dict[k] = v
            # 获取依赖数据的值，将结果填充到k_v_dict
            GetRelyData.__store(k_v_dict, rely_data)

            return "&".join([k+'='+v for k, v in k_v_dict.items()])
        # request_data为字典类型数据
        else:
            GetRelyData.__store(request_data, rely_data)
            return request_data


if __name__ == "__main__":
    REQUEST_DATA = {"用户注册": {"1": {"username": "zhangsan", "password": "234dr3"}}}
    s = {"username": "", "password": ""}
    # # s = "userid=1&password=xdswewe&username=true"
    rely = {"request": {"username": "用户注册->1", "password": "用户注册->1"}}
    print(GetRelyData.get(str(s), str(rely)))


