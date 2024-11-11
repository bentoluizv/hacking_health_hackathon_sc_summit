from fastapi import FastAPI

from hackathon.api import (
    atendimento,
    consulta,
    evolucao,
    paciente,
    triagem,
)

app = FastAPI()


app.include_router(atendimento.router)
app.include_router(consulta.router)
app.include_router(evolucao.router)
app.include_router(paciente.router)
app.include_router(triagem.router)
