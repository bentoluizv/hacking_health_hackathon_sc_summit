from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from hackathon.api import (
    paciente,
    triagem,
)
from hackathon.db import get_session
from hackathon.models import PacienteOrm

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')


@app.get(
    '/triagem',
    response_class=HTMLResponse,
)
async def triagem_page(
    paciente_id: str,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
):
    paciente_orm = session.get(PacienteOrm, paciente_id)

    if not paciente_orm:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Paciente não encontrado'
        )

    return templates.TemplateResponse(
        request=request,
        name='triagem.html',
        context={
            'paciente': paciente_orm,
        },
    )


app.include_router(paciente.router)
app.include_router(triagem.router)
