from sqlalchemy import Column, Date, Integer, String, Boolean, BigInteger

from database import Base


class Counterparties(Base):
    """The model of counterparties. Common info about counterparties."""
    __tablename__ = "counterparties"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    conclusion_contract_date = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    inn = Column(BigInteger, nullable=False)
    active = Column(Boolean, nullable=False)
