from pydantic import BaseModel
from typing import Optional
from datetime import date

class DetailAnalyst(BaseModel):
    id: int
    symbol: str
    broker: str
    analyst: Optional[str] = None

    # เปลี่ยนเป็น float
    eps_2569: Optional[float] = None
    eps_2570: Optional[float] = None

    profit_2569: Optional[float] = None
    profit_2570: Optional[float] = None

    pe_2569: Optional[float] = None
    pe_2570: Optional[float] = None

    pbv_2569: Optional[float] = None
    pbv_2570: Optional[float] = None

    dividend_2569: Optional[float] = None
    dividend_2570: Optional[float] = None

    target_price: Optional[float] = None

    # แยก value / text
    upside_value: Optional[float] = None
    upside_text: Optional[str] = None

    recommendation: Optional[str] = None

    # เปลี่ยนเป็น date
    report_date: Optional[date] = None

    class Config:
        from_attributes = True

class CompanySchema(BaseModel):
    company_name: str
    sector: str
    industry: Optional[str] = None

    class Config:
        from_attributes = True

class AnalystColumn(BaseModel):
    id: int

    symbol: str
    broker: str
    analyst: Optional[str] = None

    target_price: Optional[float] = None

    upside_value: Optional[float] = None
    upside_text: Optional[str] = None

    recommendation: Optional[str] = None
    report_date: Optional[date] = None

    # join company
    company: Optional[CompanySchema] = None

class FilteredAnalyst(BaseModel):
    symbol: str
# class AnalystResponse(Analyst):
#     id: int
#     scraped_at: datetime

#     class Config:
#         from_attributes = True