from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import os

# Инициализация БД
DATABASE_URL = "sqlite:///./hisob.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель БД
class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String, nullable=True)
    icon = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Pydantic модель
class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: str = None
    icon: str
    date: datetime = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str = None
    icon: str
    date: datetime

    class Config:
        from_attributes = True

# FastAPI приложение
app = FastAPI(title="Хисобчи API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints
@app.get("/api/transactions", response_model=dict)
def get_transactions(db: Session = Depends(get_db)):
    """Получить все транзакции"""
    transactions = db.query(TransactionModel).all()
    return {
        "transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "category": t.category,
                "description": t.description,
                "icon": t.icon,
                "date": t.date.isoformat()
            }
            for t in transactions
        ]
    }

@app.post("/api/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Создать новую транзакцию"""
    db_transaction = TransactionModel(
        user_id="default",
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
        icon=transaction.icon,
        date=transaction.date or datetime.utcnow()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/api/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Удалить транзакцию"""
    db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@app.get("/api/stats", response_model=dict)
def get_stats(db: Session = Depends(get_db)):
    """Получить статистику"""
    transactions = db.query(TransactionModel).all()
    total_spent = sum(t.amount for t in transactions)
    
    # Статистика по категориям
    category_stats = {}
    for t in transactions:
        if t.category not in category_stats:
            category_stats[t.category] = 0
        category_stats[t.category] += t.amount
    
    return {
        "total_spent": total_spent,
        "transactions_count": len(transactions),
        "category_stats": category_stats
    }

@app.get("/health")
def health_check():
    """Проверка здоровья"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)