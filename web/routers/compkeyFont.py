# coding=utf-8
from fastapi import APIRouter
from web.model import mongodb
from web.common import response
from web.core.coreService import analyse_compkey, update_compkey
from web.domain.DomainClass import Search_Param, Score_Param, SearchResponse

router = APIRouter(
    prefix='/font',
    responses={404: {"description": "Not found"}}
)


@router.post('/search', tags=["search"])
def search_word(request_body: Search_Param):
    # print("参数: ", request_body.keyword)
    result = analyse_compkey(request_body.keyword, mongodb.db)
    res = []
    index = 1
    for k, v in list(result.items()):
        res.append(SearchResponse(key=index, word=k, rate=v))
        index += 1
    return response.SuccessResponse(res)


@router.post('/scoring', tags=["score"])
def score_word(request_body: Score_Param):
    # print(request_body)
    # TODO here
    result = update_compkey(mongodb.db, request_body.keyword, request_body.compkey, request_body.score)
    # print(result)
    if result:
        print("评分成功")
        return response.SuccessResponse(data=None, msg="评分成功")
    else:
        print("评分失败")
        return response.FailedResponse(data=None, msg="服务端异常，评分失败")
