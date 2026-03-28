from fastapi import APIRouter, Depends
# from requests import Session
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.analyst_schema import Analyst
import services.analysts_service as analysts_service
from core.database import get_db
router = APIRouter()

# @router.get("/analysts", response_model=list[Analyst])
# def get_all_analysts(db: Session = Depends(get_db)):
#     return analysts_service.get_all_analyst(db)
@router.get("/symbols", response_model=list[Analyst])
def get_symbols(db: Session = Depends(get_db)):
    symbols = db.execute(text("""
        SELECT DISTINCT symbol FROM analyst_consensus
    """)).fetchall()

    return [s[0] for s in symbols]
@router.get("/analysts/{symbol}", response_model=list[Analyst])
def get_analyst_by_symbol(symbol: str, db: Session = Depends(get_db)):
    analysts = analysts_service.get_analyst_by_symbol(db, symbol)
    return analysts