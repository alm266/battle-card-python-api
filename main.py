from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import players, cards, decks, cardInfos

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(players.router)
app.include_router(cards.router)
app.include_router(decks.router)
app.include_router(cardInfos.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["/admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)

@app.get("/")
async def root():
    return {"Message": "Congrats! This is your first python API!"}