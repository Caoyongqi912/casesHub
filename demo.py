import requests


def demo():
    req = requests.session()
    info = {
        "url": "https://uat-nanjing.cbs.bacic5i5j.com/sales/house/main/inserthouse",
        "json": {'businesstype': 2}
    }
    resp = getattr(req,"post")(**info)
    print(resp.text)


if __name__ == '__main__':
    demo()
