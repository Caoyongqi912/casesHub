# @Time : 2022/12/1 20:58
# @Author : cyq
# @File : _types.py 
# @Software: PyCharm
# @Desc:
from typing import Union, Tuple, Callable, Mapping, Optional, Sequence, List, Any,IO


"""
Optional 可选类型 参数除了给定的类型外还可以是None
Sequence 不确定list 还是 tuple
"""

"""
Union 多种类型

"""

PrimitiveData = Optional[Union[str, int, float, bool]]


QueryParamTypes = Union[
    "QueryParams",
    Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]],
    List[Tuple[str, PrimitiveData]],
    Tuple[Tuple[str, PrimitiveData], ...],
    str,
    bytes,
]

HeaderTypes = Union[
    "Headers",
    Mapping[str, str],
    Mapping[bytes, bytes],
    Sequence[Tuple[str, str]],
    Sequence[Tuple[bytes, bytes]],
]
RequestData = Mapping[str, Any]

FileContent = Union[IO[bytes], bytes, str]
FileTypes = Union[
    # file (or bytes)
    FileContent,
    # (filename, file (or bytes))
    Tuple[Optional[str], FileContent],
    # (filename, file (or bytes), content_type)
    Tuple[Optional[str], FileContent, Optional[str]],
    # (filename, file (or bytes), content_type, headers)
    Tuple[Optional[str], FileContent, Optional[str], Mapping[str, str]],
]

AuthTypes = Union[
    Mapping[str, str],
    Callable[["Request"], "Request"],
    "Auth",
]

