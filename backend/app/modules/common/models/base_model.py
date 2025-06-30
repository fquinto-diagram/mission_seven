from sqlalchemy import DateTime
from datetime import datetime, UTC
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.config.database import Base

class BaseModel(Base):
    __abstract__ = True
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)
    
    def to_dict(self, include_relations: list = None) -> dict:
        """
        Convert the BaseModel to a dictionary
        
        Args:
            include_relations (list): List of relations to include in the dictionary
            
        Returns:
            dict: The dictionary representation of the BaseModel
        """
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime):
                result[c.name] = value.isoformat()
            else:
                result[c.name] = value
                
        if include_relations:
            for relation in include_relations:
                if hasattr(self, relation):
                    value = getattr(self, relation)
                    if isinstance(value, list):
                        result[relation] = [item.to_dict() for item in value]
                    elif hasattr(value, 'to_dict'):
                        result[relation] = value.to_dict()
                    else:
                        result[relation] = value
                        
        return result

class SoftDeleteMixin:
    """Mixin to add soft delete functionality to models"""
    
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    def soft_delete(self):
        """Marks the record as deleted by setting deleted_at"""
        self.deleted_at = datetime.now(UTC)
    
    @classmethod
    def get_active(cls, session):
        """Gets all active records (not deleted)"""
        return session.query(cls).filter(cls.deleted_at.is_(None)).all()
    
    @classmethod
    def get_deleted(cls, session):
        """Gets all deleted records"""
        return session.query(cls).filter(cls.deleted_at.isnot(None)).all()
    
    @classmethod
    def get_all(cls, session):
        """Gets all records, including deleted ones"""
        return session.query(cls).all() 