# coding=utf-8
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import compkeyFont, compkeyBack
from model import mongodb

app = FastAPI()
app.include_router(compkeyFont.router)
app.include_router(compkeyBack.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    # 客户端前台的源
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)


@app.get('/')
async def api_main():
    return {"msg": "Hello World"}


@app.on_event('startup')
async def app_start():
    print('Fast API Service Running...')


@app.on_event('shutdown')
async def app_shutdown():
    mongodb.mongo_client.close()


if __name__ == '__main__':
    uvicorn.run(
        'web.main:app',
        host='127.0.0.1',
        port=8080,
        reload=True
    )
