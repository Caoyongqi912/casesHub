import re
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Login:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    def __init__(self, env: str = "uat"):
        self.work = requests.session()
        self.env = env
        self.Host = f"https://uat.cbs.bacic5i5j.com/cas/login?service=https://{self.env}-beijing.nhcbs.5i5j.com/nhcbs/"

    def getToken(self, u: str) -> str | None:
        res = self.work.get(self.Host)
        execution = re.findall('name="execution" value="(.*?)" />', res.text)
        lt = re.findall('name="lt" value="(.*?)" />', res.text)
        data = {"username": u,
                "password": "1q2w3e4r",
                "lt": lt[0],
                "execution": execution[0],
                "_eventId": "submit"}
        r = self.work.post(url=self.Host, params=data, headers=self.headers, verify=False,
                           allow_redirects=False)
        Location = r.headers.get('Location', None)
        if not Location:
            return None
        ticket = Location.split("ticket=")[1]
        data = {"ticket": ticket,
                "casService": f"https://{self.env}-beijing.nhcbs.5i5j.com/nhcbs/"
                }
        res = self.work.get(url=f"https://{self.env}-beijing.nhcbs.5i5j.com/nhapigw/nhcas", params=data, verify=False,
                            headers=self.headers)
        token = res.json()['data']
        return token
