from numpy import number
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Analyst(BaseModel):
    id: int
    symbol: str
    broker: str
    analyst: Optional[str] = None

    eps_2569: Optional[str] = None
    eps_2570: Optional[str] = None

    profit_2569: Optional[str] = None
    profit_2570: Optional[str] = None

    pe_2569: Optional[str] = None
    pe_2570: Optional[str] = None

    pbv_2569: Optional[str] = None
    pbv_2570: Optional[str] = None

    dividend_2569: Optional[str] = None
    dividend_2570: Optional[str] = None

    target_price: Optional[str] = None
    upside_downside: Optional[str] = None
    recommendation: Optional[str] = None
    report_date: Optional[str] = None


class AnalystCreate(Analyst):
    pass

# class AnalystResponse(Analyst):
#     id: int
#     scraped_at: datetime

#     class Config:
#         from_attributes = True