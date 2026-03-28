from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class AnalystData(Base):
    __tablename__ = "analyst_consensus"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), ForeignKey("companies.symbol"), nullable=False)
    broker = Column(String(100), nullable=False)
    analyst = Column(String(255))

    eps_2569 = Column(Numeric)
    eps_2570 = Column(Numeric)

    profit_2569 = Column(Numeric)
    profit_2570 = Column(Numeric)

    pe_2569 = Column(Numeric)
    pe_2570 = Column(Numeric)

    pbv_2569 = Column(Numeric)
    pbv_2570 = Column(Numeric)

    dividend_2569 = Column(Numeric)
    dividend_2570 = Column(Numeric)

    target_price = Column(Numeric)

    upside_value = Column(Numeric)
    upside_text = Column(String(100))

    recommendation = Column(String(100))

    report_date = Column(Date)

    scraped_at = Column(TIMESTAMP, default=datetime.utcnow)

    company = relationship("Company", back_populates="analysts")

    __table_args__ = (
        UniqueConstraint(
            "symbol", "broker", "analyst", "report_date",
            name="uq_symbol_broker_analyst_report"
        ),
    )


class Company(Base):
    __tablename__ = "companies"

    symbol = Column(String(20), primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    market = Column(String(50))
    sector = Column(String(100))
    industry = Column(String(100))
    address = Column(String(255))
    postal_code = Column(String(20))
    phone = Column(String(50))
    fax = Column(String(50))
    website = Column(String(255))

    analysts = relationship("AnalystData", back_populates="company")