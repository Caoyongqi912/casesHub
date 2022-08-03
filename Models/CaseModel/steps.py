from typing import AnyStr, TypeVar, Generic, NoReturn, Union, Optional, Mapping, Any

class Steps:
    step: int
    do: AnyStr
    exp: AnyStr

    def __init__(self, info: Mapping[str, Union[int, str]]) -> NoReturn:
        self.step = info.get("step")
        self.do = info.get("do")
        self.exp = info.get("exp")

if __name__ == '__main__':
    info = {'step': 1, "do": "Adad", "exp": None}
    s = Steps(info)
    print(s.exp)
