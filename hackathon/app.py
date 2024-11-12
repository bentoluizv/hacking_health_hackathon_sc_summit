from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from hackathon.api import (
    atendimento,
    consulta,
    evolucao,
    paciente,
    triagem,
)
from hackathon.db import get_session
from hackathon.models import PacienteOrm
from hackathon.utils.to_tb import paciente_orm_to_model

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.get('/cadastro', response_class=HTMLResponse)
async def cadastro_paciente(request: Request):
    return templates.TemplateResponse(request=request, name='cadastro.html')


@app.get('/pacientes/{id}', response_class=HTMLResponse)
async def paciente_page(
    request: Request, session: Annotated[Session, Depends(get_session)]
):
    paciente_orm = session.get(PacienteOrm, id)

    if not paciente_orm:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Paciente não encontrado'
        )

    paciente_model = paciente_orm_to_model(paciente_orm)

    return templates.TemplateResponse(
        request=request,
        name='paciente.html',
        context={'paciente': paciente_model},
    )


app.include_router(atendimento.router)
app.include_router(consulta.router)
app.include_router(evolucao.router)
app.include_router(paciente.router)
app.include_router(triagem.router)
