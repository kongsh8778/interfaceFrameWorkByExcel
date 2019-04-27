# -*-coding:utf-8 -*-

import requests, json


class HTTPClient(object):
    """处理接口请求并返回请求结果"""

    @staticmethod
    def request(request_url, request_method, params_type, request_data=None, headers=None):
        """

        :param request_url:请求的url
        :param request_method: 请求方法：post/get
        :param params_type: 请求参数类型：form/url/json/字符串
        :param request_data:请求数据
        :param headers:请求报文头，可选参数
        :return:返回响应报文
        """
        response = None
        # get请求
        if request_method.lower() == 'get':
            if params_type.lower() == 'url':
                # 直接将请求数据拼接到url之后
                url = "%s%s" % (request_url, request_data)
                response = requests.get(url=url, headers=headers)
            elif params_type.lower() == 'params':
                # get请求的内容通过params参数传递
                if isinstance(request_data, dict):
                    response = requests.get(url=request_url, params=json.dumps(request_data), headers=headers)
                elif isinstance(request_data, str):
                    response = requests.get(url=request_url, params=request_data, headers=headers)
        # post请求
        elif request_method.lower() == 'post':
            if params_type.lower() == 'form':
                # 表单提交，请求数据通过post方法的data参数提交
                response = requests.post(url=request_url, data=json.dumps(request_data), headers=headers)
            elif params_type.lower() == 'json':
                response = requests.post(url=request_url, json=json.dumps(request_data), headers=headers)

        return response


if __name__ == "__main__":
    # post请求
    url = 'http://39.106.41.11:8080/register/'
    method = 'post'
    t = 'form'
    data = {"username": "kongsh190401", "password": "kongsh190401", "email": "wcx@qq.com"}
    result = HTTPClient.request(url, method, t, data)
    print(result.status_code)
    print(result.url)
    print(result.json())

    # get请求
    url = 'http://39.106.41.11:8080/getBlogContent/'
    method = 'get'
    t = 'url'
    data = '2'
    result = HTTPClient.request(url, method, t, data)
    print(result.status_code)
    print(result.url)
    print(result.json())
