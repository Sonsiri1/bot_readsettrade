from sqlalchemy import Column, Integer, String, TIMESTAMP, UniqueConstraint
from datetime import datetime
from core.database import Base


class AnalystData(Base):
    __tablename__ = "analyst_consensus"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), nullable=False)
    broker = Column(String(100), nullable=False)
    analyst = Column(String(255), nullable=False)

    eps_2569 = Column(String(50))
    eps_2570 = Column(String(50))

    profit_2569 = Column(String(50))
    profit_2570 = Column(String(50))

    pe_2569 = Column(String(50))
    pe_2570 = Column(String(50))

    pbv_2569 = Column(String(50))
    pbv_2570 = Column(String(50))

    dividend_2569 = Column(String(50))
    dividend_2570 = Column(String(50))

    target_price = Column(String(50))
    upside_downside = Column(String(100))
    recommendation = Column(String(100))
    report_date = Column(String(50))

    scraped_at = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("symbol", "broker", "analyst", "report_date", name="uq_symbol_broker_analyst_report"),
    )