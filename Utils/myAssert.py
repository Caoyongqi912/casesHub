# @Time : 2022/9/17 10:54 
# @Author : cyq
# @File : myAssert.py 
# @Software: PyCharm
# @Desc:
from json import JSONDecodeError
from typing import Any, Dict, List
from requests import Response
from Utils import MyLog
from .myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyAssert:
    def __init__(self, response: Response = None):
        self.response = response
        self.LOG = []

    def doAssert(self, step: int, assertList: List[Dict[str, Any]]):
        """
        校验开始
        :param  step 步骤id
        :param assertList: demo [{"extraOpt": "jsonpath","extraValue": "$.code","assertOpt": "==","expect": "0"}]
        :return:
        """
        flag = True
        assert_result = []
        if assertList:
            for _ in assertList:

                extraOpt = _["extraOpt"]
                extraValue = _["extraValue"]
                assertOpt = _["assertOpt"]
                expect = _['expect']

                log.info(f"校验方法   -> [{extraOpt}]")
                log.info(f"校验语法   -> [{extraValue}]")
                log.info(f"断言方法   -> [{assertOpt}]")
                log.info(f"预期值     -> [{expect}]")
                self.LOG.append(f"step-{step}:校验方法  ====== {extraOpt}\n")
                self.LOG.append(f"step-{step}:校验语法  ====== {extraValue}\n")
                self.LOG.append(f"step-{step}:断言方法  ====== {assertOpt}\n")
                self.LOG.append(f"step-{step}:预期值  ====== {expect}\n")

                if extraOpt == "jsonpath":
                    # jsonpath 提取
                    try:
                        actual: Any = MyJsonPath(response=self.response, expr=extraValue).value
                    except JSONDecodeError as e:
                        log.error(repr(e))
                        flag = False
                        return assert_result, flag
                    log.info(f"实际返回   -> [{actual}]")
                    self.LOG.append(f"step-{step}:实际返回  ====== {actual}\n")

                    _['actual'] = actual
                    # assert 断言
                    try:
                        self._option(assertOpt, expect, actual)
                        _["result"] = True
                        assert_result.append(_)
                        log.info(f"assert   -> [{flag}]")
                    except Exception as e:
                        log.error(repr(e))
                        flag, _["result"] = False, False
                        assert_result.append(_)
                        log.error(f"result   -> [{flag}]")
                elif extraOpt == "re":
                    pass

        return assert_result, flag, self.LOG

    def _option(self, T: str, expect: Any, actual: Any):
        """
        断言配置
        :param T: 配置类型
        :param expect: 预期值
        :param actual: 实际值
        :return:
        """
        _ = {
            "==": self.assertEqual,
            "!=": self.assertUnEqual,
            ">": self.assertGreater,
            "<": self.assertLess,
            ">=": self.assertEqualGreater,
            "<=": self.assertEqualLess,
            "in": self.assertIn,
            "notIn": self.assertNotIn
        }

        return _[T](expect, actual)

    @staticmethod
    def assertEqual(expect: Any, actual: Any):
        """
        校验相等
        :param expect:
        :param actual:
        :assert expect == actual
        """
        assert str(expect) == str(actual)

    @staticmethod
    def assertUnEqual(expect: Any, actual: Any):
        """
        校验不相等
        :param expect:
        :param actual:
        :return:expect != actual
        """

        assert expect != actual

    @staticmethod
    def assertIn(expect: Any, actual: Any):
        """
        校验包含
        :param expect:
        :param actual:
        :return:
        """
        assert expect in actual

    @staticmethod
    def assertNotIn(expect: Any, actual: Any):
        """
        校验不包含
        :param expect:
        :param actual:
        :return:
        """

        assert expect not in actual

    @staticmethod
    def assertGreater(expect: Any, actual: Any):
        """
        校验大于
        :param expect:
        :param actual:
        :return:
        """

        assert expect > actual

    @staticmethod
    def assertLess(expect: Any, actual: Any):
        """
        校验大于
        :param expect:
        :param actual:
        :return:
        """

        assert expect < actual

    @staticmethod
    def assertEqualGreater(expect: Any, actual: Any):
        """
        校验大于等于
        :param expect:
        :param actual:
        :return:
        """

        assert expect >= actual

    @staticmethod
    def assertEqualLess(expect: Any, actual: Any):
        """
        校验小于等于
        :param expect:
        :param actual:
        :return:
        """

        assert expect <= actual
