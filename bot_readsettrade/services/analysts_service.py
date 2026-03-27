from sqlalchemy.orm import Session
from models.stock_model import AnalystData
 
def get_all_analyst(db: Session):
    analysts = db.query(AnalystData).all()
    return analysts

def get_analyst_by_symbol(db, symbol):
    analysts = db.query(AnalystData).filter_by(symbol=symbol).all()

    # result = []
    # for analyst in analysts:
    #     result.append({
    #         "symbol": analyst.symbol,
    #         "broker": analyst.broker,
    #         "analyst": analyst.analyst
    #     })

    return analysts