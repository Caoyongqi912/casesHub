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

            # jsonpath 提取
            try:
                actual: Any = MyJsonPath(response=self.response.json(), expr=jp_str).value
            except JSONDecodeError as e:
                log.error(repr(e))
                flag = False
                return assert_result, flag
            log.info(f"actual   -> [{actual}]")

            # assert 断言
            try:
                self._option(option, expect, actual)
                # assert expect == actual
                _["result"] = True
                assert_result.append(_)
                log.info(f"assert   -> [{flag}]")
            except Exception as e:
                log.error(repr(e))
                flag, _["result"] = False, False
                assert_result.append(_)
                log.error(f"result   -> [{flag}]")

        return assert_result, flag

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
        assert expect == actual

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
