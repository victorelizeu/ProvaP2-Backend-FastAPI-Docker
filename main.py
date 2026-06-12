import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:admin123@localhost:5432/mydatabase"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome não pode ser vazio")
    preco: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    estoque: int = 0
    ativo: bool = True


class ProdutoResponse(ProdutoCreate):
    id: int

    class Config:
        from_attributes = True


app = FastAPI(title="API E-commerce do Jones- Prova Backend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"msg": "TA RODANDOOO!"}


@app.post(
    "/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED
)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


@app.get(
    "/produtos", response_model=List[ProdutoResponse], status_code=status.HTTP_200_OK
)
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@app.get(
    "/produtos/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK
)
def buscar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    return produto


@app.delete("/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )
    db.delete(produto)
    db.commit()
    return None
