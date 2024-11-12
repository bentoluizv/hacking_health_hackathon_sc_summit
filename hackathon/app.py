from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from hackathon.api import (
    triagem,
)

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=RedirectResponse)
def index_page():
    return '/triagem'


@app.get(
    '/triagem',
    response_class=HTMLResponse,
)
async def triagem_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name='triagem.html',
    )


app.include_router(triagem.router)
