import requests


def demo():
    req = requests.session()
    info = {
        "url": "https://uat-nanjing.cbs.bacic5i5j.com/sales/house/main/inserthouse",
        "json": {'businesstype': 2}
    }
    resp = getattr(req, "post")(**info)
    print(resp.text)


def score():
    c = (100 - c)/0.04
    print(c)


if __name__ == '__main__':
    score()
