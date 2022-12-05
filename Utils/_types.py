# @Time : 2022/12/1 20:58
# @Author : cyq
# @File : _types.py 
# @Software: PyCharm
# @Desc:
from typing import Union, Tuple, Callable, Mapping, Optional, Sequence, List

"""
Optional 可选类型 参数除了给定的类型外还可以是None
Sequence 不确定list 还是 tuple
"""

"""
Union 多种类型

"""


def demo(arg: Union[int, None] = 1):
    return arg


AuthTypes = Union[
    Mapping[str,str],
    Callable[["Request"], "Request"],
    "Auth",
]

QueryParamTypes = Union[
    "QueryParams",
    Mapping[str, Union[Optional[Union[str, int, float, bool]], Sequence[Optional[Union[str, int, float, bool]]]]],
    List[Tuple[str, Optional[Union[str, int, float, bool]]]],
    Tuple[Tuple[str, Optional[Union[str, int, float, bool]]], ...],
    str,
    bytes,
]
if __name__ == '__main__':
    print( demo())
