# 专门封装get post 请求方式
import requests


class HttpClient:
    # 只要用post，get请求方式 就创建会话
    def __init__(self):
        self.session = requests.Session()
        # requests.Session
        # requests.session()
        # requests.sessions

    # 发送请求  请求方式，接口地址， 接口参数类型，接口数据，头部信息，其他信息
    def send_request(self, url, method, params_type, data=None, headers=None, **kwargs):
        method = method.lower()
        params_type = params_type.lower()
        if method == 'get':
            rep = self.session.request(method=method, url=url, params=data, **kwargs)
        elif method == 'post':
            if params_type == 'from':
                rep = self.session.request(method=method, url=url, data=data, **kwargs)
            else:
                rep = self.session.request(method=method, url=url, json=data, **kwargs)

        elif method == 'delete':
            pass
        elif method == 'put':
            pass
        else:
            raise ValueError

        return rep

    #魔法方法   原本调用send_request前，需要示例化类.方法 即rep=HttpClient().send_request()
    #现在只需要示例化类 就可以拿到方法(省去一个调用的步骤)  rep=HttpClient()
    def __call__(self, url, method, params_type, data=None, headers=None, *args, **kwargs):
        return self.send_request(url, method, params_type,data, headers, **kwargs)

    def close_session(self):
        self.session.close()

