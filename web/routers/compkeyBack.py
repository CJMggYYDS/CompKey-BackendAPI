# coding=utf-8
from fastapi import APIRouter
from web.core.coreService import get_compkeys
from web.model import mongodb
from web.common import response
from web.domain.DomainClass import BackSearchResponse, EchartResponse, EchartDetailResponse, Search_Param, AllCompKeyDetail
from web.core.coreService import get_access_count, get_comkeys_details


router = APIRouter(
    prefix='/back',
    responses={404: {"description": "Not found"}}
)


@router.get('/keywords')
def find_all_compKey():
    result = get_compkeys(mydb=mongodb.db)
    res = []
    index = 1
    for k, v in list(result.items()):
        res.append(BackSearchResponse(key=index, word=k, detail=v))
        index += 1
    return response.SuccessResponse(res)


@router.get('/echart')
def find_echart_data():
    count, a = get_access_count(mydb=mongodb.db)
    detail = []
    for k, v in list(a.items()):
        detail.append(EchartDetailResponse(name=k, value=v))
    return response.SuccessResponse(EchartResponse(count=count, detail=detail))


@router.post('/compkey')
def find_word_all_compkey(request_body: Search_Param):
    result = get_comkeys_details(mydb=mongodb.db, keyword=request_body.keyword)
    res = []
    index = 1
    for k, v in list(result.items()):
        res.append(AllCompKeyDetail(key=index, word=k, detail=v))
        index += 1
    return response.SuccessResponse(res)


