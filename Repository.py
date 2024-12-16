from sqlalchemy.orm import Session

from Model import Produto

class ProdutoRepository:
    @staticmethod
    def find_all(db: Session) -> list[Produto]:
        return db.query(Produto).all()

    @staticmethod
    def save(db: Session, produto: Produto) -> Produto:
        if produto.id:
            db.merge(produto)
        else:
            db.add(produto)
        db.commit()
        return produto

    @staticmethod
    def find_by_id(db: Session, id: int) -> Produto:
        return db.query(Produto).filter(Produto.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Produto).filter(Produto.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        produto = db.query(Produto).filter(Produto.id == id).first()
        if produto is not None:
            db.delete(produto)
            db.commit()