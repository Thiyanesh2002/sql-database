from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


engine = create_engine('sqlite:///stock_market.db', echo=True)
Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ticker = Column(String, unique=True)
    description = Column(String)

class StockPrice(Base):
    __tablename__ = 'stock_prices'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref='prices')
    date = Column(DateTime, default=datetime.utcnow)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


apple = Company(name='Apple Inc.', ticker='AAPL', description='Technology company')
session.add(apple)

price_data = StockPrice(
    company=apple,
    date=datetime(2023, 1, 1),
    open_price=150.0,
    high_price=155.0,
    low_price=149.5,
    close_price=153.0,
    volume=1000000
)
session.add(price_data)


session.commit()


query_result = session.query(Company).filter_by(ticker='AAPL').first()
if query_result:
    print(f"Company Name: {query_result.name}, Ticker: {query_result.ticker}")
    for price in query_result.prices:
        print(f"Date: {price.date}, Close Price: {price.close_price}")


session.close()
