from pydantic import BaseModel


class Search_Param(BaseModel):
    keyword: str


class Score_Param(BaseModel):
    keyword: str
    compkey: str
    score: float


class SearchResponse(BaseModel):
    key: int
    word: str
    rate: float


class BackSearchResponse(BaseModel):
    key: int
    word: str
    detail: dict


class EchartResponse(BaseModel):
    count: int
    detail: list


class EchartDetailResponse(BaseModel):
    name: str
    value: int


class AllCompKeyDetail(BaseModel):
    key: int
    word: str
    detail: dict
