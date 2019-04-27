# -*-coding:utf-8 -*-

from config.public_data import RESPONSE_DATA, REQUEST_DATA
from utils.md5 import get_md5

class StoreRelyData(object):
    """将请求数据及响应数据，根据data_store指定的内容存储到全局变量RESPONSE_DATA和REQUEST_DATA"""

    @staticmethod
    def store(api_name, case_id, request_data, response_data, data_store):
        """

        :param api_name: 测试用例名称
        :param case_id:测试用例编号
        :param request_data:请求数据
        :param response_data:响应数据
        :param data_store:待存储的内容
        :return:无
        """
        k_v_dict = {}
        if isinstance(request_data, str):
            # 请求数据是字符串类型的话先转换为字典，方便后续存储
            items = request_data.split("&")
            for item in items:
                k, v = item.split("=")
                k_v_dict[k] = v
            request_data = k_v_dict

        # RESPONSE_DATA和REQUEST_DATA默认是3层的存储结构，如下：
        # REQUEST_DATA = {"用户注册": {"1": {"username": "zhangsan", "password": "234dr3"}}}
        # data_store为两层的数据结构：{"request":["username", "password"], "response": ["code"]}
        for k, v in data_store.items():
            if k.lower() == 'request':
                # 存储到REQUEST_DATA中
                # 逐级判断对应的字典结构是否已经存在，存在的话就写入，不存在的话就划出响应的空间
                for key in v:
                    if key in request_data:
                        if api_name not in REQUEST_DATA:
                            REQUEST_DATA[api_name] = {str(case_id): {key: request_data[key]}}
                        else:
                            if str(case_id) not in REQUEST_DATA[api_name]:
                                REQUEST_DATA[api_name][str(case_id)] = {key: request_data[key]}
                            else:
                                # 如果是password的话需要先md5加密后在存储
                                if key.lower() == "password":
                                    REQUEST_DATA[api_name][str(case_id)][key] = get_md5(request_data[key])
                                else:
                                    REQUEST_DATA[api_name][str(case_id)][key] = request_data[key]
                    else:
                        print('待存储的字段%s在请求数据%s中未找到!' % (key, request_data))

            elif k.lower() == 'response':
                # 存储到RESPONSE_DATA中
                # 逐级判断对应的字典结构是否已经存在，存在的话就写入，不存在的话就划出相应的空间
                for key in v:
                    if key in response_data:
                        if api_name not in RESPONSE_DATA:
                            RESPONSE_DATA[api_name] = {str(case_id): {key: response_data[key]}}
                        else:
                            if str(case_id) not in RESPONSE_DATA[api_name]:
                                RESPONSE_DATA[api_name][str(case_id)] = {key: response_data[key]}
                            else:
                                RESPONSE_DATA[api_name][str(case_id)][key] = response_data[key]
                    else:
                        print('待存储的字段%s在响应数据%s中未找到!' % (key, response_data))


if __name__ == "__main__":
    request = {"username": "srsdcx03331", "password": "wcx123wac1", "email": "wcx@qq.com"}
    store = {"request":["username", "password"], "response": ["code", "userid"]}
    response = {'userid': 'srsdcx01', 'code': '01'}
    StoreRelyData.store('用户注册', 1, request, response, store)
    print(REQUEST_DATA)
    print(RESPONSE_DATA)

    request = 'username=kongsh&password=1234&flag=true'
    StoreRelyData.store('用户注册', 2, request, response, store)
    print(REQUEST_DATA)
    print(RESPONSE_DATA)
