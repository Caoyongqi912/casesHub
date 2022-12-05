# @Time : 2022/9/17 10:54 
# @Author : cyq
# @File : myAssert.py 
# @Software: PyCharm
# @Desc:
from typing import Any, Dict, List
from requests import Response
from Utils import MyLog
from myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyAssert:
    def __init__(self, response: Response):
        self.response = response

    def jpAssert(self, jps: List[Dict[str, Any]]):
        """
        jsonpath 校验
        :param jps: jsonpath [{jp: str, expect: Any, option: str}]
        :return:
        """
        flag = True
        assert_result = []
        for _ in jps:

            jp_str = _['jp']
            expect = _['expect']
            option = _['option']

            log.info(f"jsonpath -> [{jp_str}]")
            log.info(f"option   -> [{option}]")
            log.info(f"expect   -> [{expect}]")
            actual: Any = MyJsonPath(response=self.response.json(), expr=jp_str).value
            log.info(f"actual   -> [{actual}]")
            try:
                if option == "==":
                    assert expect == actual
                    _["result"] = True
                    assert_result.append(_)
                    log.info(f"result   -> [success]")
            except AssertionError as e:
                _["result"] = False
                flag = False
                assert_result.append(_)
                log.error(f"result   -> [fail]")
        return assert_result, flag
