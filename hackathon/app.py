from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from hackathon.api import (
    atendimento,
    consulta,
    evolucao,
    paciente,
    triagem,
)

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


app.include_router(atendimento.router)
app.include_router(consulta.router)
app.include_router(evolucao.router)
app.include_router(paciente.router)
app.include_router(triagem.router)
