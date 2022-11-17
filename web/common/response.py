# coding=utf-8
from pydantic import BaseModel
from typing import Any


class Response(BaseModel):
    code: int
    msg: str
    data: Any = None


def SuccessResponse(data, msg='请求成功', code=200):
    result = Response(code=code, msg=msg, data=data)
    return result


def FailedResponse(data, msg='请求失败', code=500):
    result = Response(code=code, msg=msg, data=data)
    return result
