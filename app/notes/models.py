from .. import db


class NoteModel(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024), unique=False, nullable=False)
    body = db.Column(db.String(8192), unique=False, nullable=True)
    owner = db.Column(db.Integer, unique=False, nullable=False)

    @classmethod 
    def find_by_id(cls, id, owner):
        return cls.query.filter_by(id=id).filter_by(owner=owner).first()

    @classmethod
    def find_by_owner(cls, owner):
        return cls.query.filter_by(owner=owner).all()

    @classmethod
    def get_paginated_notes(cls, owner, limit=10, offset=0):
        """Get paginated notes for an owner.
        
        Args:
            owner (int): The owner ID
            limit (int): Maximum number of notes to return
            offset (int): Number of notes to skip
            
        Returns:
            List of NoteModel objects sorted by ID
        """
        return cls.query.filter_by(owner=owner)\
            .order_by(cls.id)\
            .limit(limit)\
            .offset(offset)\
            .all()

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
