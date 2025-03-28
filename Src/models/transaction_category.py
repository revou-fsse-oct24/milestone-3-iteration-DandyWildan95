from src.models.base import db, Base

class TransactionCategory(Base):
    __tablename__ = 'transaction_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
