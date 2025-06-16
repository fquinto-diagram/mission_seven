from datetime import datetime, timedelta
import math
import json
from typing import TypeVar, Generic, List
from app.modules.common.models.base_model import BaseModel
from sqlalchemy.orm import Session, Query, joinedload
from app.libraries.http.exception_library import ExceptionLibrary
from app.modules.common.helpers.model_helper import update_model_attributes
from app.libraries.date_formatter import DateFormatter
from pydantic import BaseModel as BaseSchema
from fastapi.exceptions import RequestValidationError
from app.config.translations.i18n import get_translation
from app.config.settings import settings
from sqlalchemy import or_
from app.modules.common.helpers.pluralize import pluralize

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: ModelType):
        self.db = db
        self.model = model
        
    def _base_query(self, include_deleted: bool = False) -> Query:
        query = self.db.query(self.model)
        if hasattr(self.model, "deleted_at") and not include_deleted:
            query = query.filter(self.model.deleted_at.is_(None))
        if hasattr(self.model, "DEFAULT_ORDER_BY"):
            query = query.order_by(getattr(self.model, self.model.DEFAULT_ORDER_BY))
        return query
    
    def _get_unique_fields(self) -> List[str]:
        return [
            field.name
            for field in self.model.__table__.columns
            if field.unique and field.name != "id"
        ]
        
    def _validate_unique_fields(self, data: dict, id: int = None) -> None:
        """
        Validate unique fields
        
        Args:
            data (dict): The data to validate
            id (int): The id of the model to exclude
        """
        for field in self._get_unique_fields():
            if data.get(field):
                query = self.db.query(self.model).filter(getattr(self.model, field) == data[field])
                if id:
                    query = query.filter(self.model.id != id)
                if query.first():
                    raise RequestValidationError([
                        {
                            "type": "unique",
                            "loc": ["body", field],
                            "msg": get_translation("validation.unique", params={"field": field}),
                            "input": data[field]
                        }
                    ])
                    
    def _handle_unique_fields(self, input: dict) -> ModelType | None:
        """
        Handle unique fields validation and restoration
        
        Args:
            input (dict): The input data to validate
            
        Returns:
            ModelType | None: The restored model if found and deleted, None otherwise
        """
        for field in self._get_unique_fields():
            if input.get(field):
                existing_item = self.db.query(self.model).filter(
                    getattr(self.model, field) == input[field]
                ).first()
                
                if existing_item:
                    if existing_item.deleted_at is not None:
                        return self.restore(existing_item.id, input)
                    raise RequestValidationError([
                        {
                            "type": "unique",
                            "loc": ["body", field],
                            "msg": get_translation("validation.unique", params={"field": field}),
                            "input": input[field]
                        }
                    ])
        return None
    
    def _include_relations(self, query: Query, include_relations: list) -> Query:
        if include_relations:
            for relation in include_relations:
                query = query.options(joinedload(getattr(self.model, relation)))
        return query
    
    def _parse_date_range(self, values: list[str]) -> tuple[datetime, datetime]:
        start = datetime.strptime(values[0], "%Y-%m-%d") if values[0] else None
        if len(values) > 1:
            end = datetime.strptime(values[1], "%Y-%m-%d") + timedelta(days=1) if values[1] else None
        else:
            end = datetime.strptime(values[0], "%Y-%m-%d") + timedelta(days=1) if values[0] else None
        return start, end

    def _apply_filters(self, query: Query, filters: list[dict]) -> Query:
        if isinstance(filters, str):
            filters = json.loads(filters)
        for filter in filters:
            if filter['type'] == 'equal':
                query = query.filter(getattr(self.model, filter['field']).like(f"%{filter['values'][0]}%"))
            elif filter['type'] == 'range':
                start, end = self._parse_date_range(filter['values'])
                if start and end:
                    query = query.filter(getattr(self.model, filter['field']).between(start, end))
                elif filter['values'][0] and not filter['values'][1]:
                    query = query.filter(getattr(self.model, filter['field']) >= start)
                elif not filter['values'][0] and filter['values'][1]:
                    query = query.filter(getattr(self.model, filter['field']) <= end)
            elif filter['type'] == 'gt':
                query = query.filter(getattr(self.model, filter['field']) > filter['values'][0])
            elif filter['type'] == 'gte':
                query = query.filter(getattr(self.model, filter['field']) >= filter['values'][0])
            elif filter['type'] == 'lt':
                query = query.filter(getattr(self.model, filter['field']) < filter['values'][0])
            elif filter['type'] == 'lte':
                query = query.filter(getattr(self.model, filter['field']) <= filter['values'][0])
        return query
        
    def find(self, id: int, include_relations: list = None, include_deleted: bool = False) -> ModelType:
        """
        Find a model by id
        
        Args:
            id (int): The id of the model to find
            include_deleted (bool): Whether to include deleted models
            locale (str): The locale to use for translations
            
        Returns:
            ModelType: The found model
        """
        query = self._base_query(include_deleted)
        query = self._include_relations(query, include_relations)
        item = query.filter(self.model.id == id).first()
        ExceptionLibrary.throw_404_if(not item, f"{pluralize(self.model.__name__.lower())}.not_found")
        return item
    
    def find_many(self, ids: List[int], include_relations: list = None, include_deleted: bool = False) -> List[ModelType]:
        query = self._base_query(include_deleted)
        query = self._include_relations(query, include_relations)
        return query.filter(self.model.id.in_(ids)).all()
    
    def find_by_fields(self, fields: dict, include_relations: list = None, include_deleted: bool = False) -> ModelType:
        query = self._base_query(include_deleted)
        query = self._include_relations(query, include_relations)
        for field, value in fields.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.first()
    
    def find_by_unique_fields(self, fields: dict, include_relations: list = None, include_deleted: bool = False) -> ModelType:
        query = self._base_query(include_deleted)
        query = self._include_relations(query, include_relations)
        for field, value in fields.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.first()
    
    def scope_date_range(self, query: Query, from_date: str, to_date: str, limit: int = None, page: int = 1) -> list | None:
        from_date = f"{from_date} 00:00:00"
        to_date = f"{to_date} 23:59:59"
        
        query = query.filter(self.model.created_at >= from_date).filter(self.model.created_at <= to_date)
        if limit:
            total = query.count()
            if (page - 1) * limit >= total:
                return None
            query = query.limit(limit).offset((page - 1) * limit)
        
        results = query.all()
        return results
    
    def all(self, include_relations: list = None, include_deleted: bool = False) -> List[ModelType]:
        """
        Get all models
        
        Args:
            include_deleted (bool): Whether to include deleted models
            
        Returns:
            list[ModelType]: The list of models
        """
        query = self._base_query(include_deleted)
        query = self._include_relations(query, include_relations)
        return query.all()


    def list(self, filter: BaseSchema, search_fields: list[str] = ['name'], filters: list[dict] = None, include_deleted: bool = False) -> dict:
        """
        List all models
        
        Args:
            filter (BaseSchema): The filter to apply to the query
            include_deleted (bool): Whether to include deleted models
            
        Returns:
            list[ModelType]: The list of models
        """
        query = self._base_query(include_deleted)
        query = self._include_relations(query, filter.include)
        if filter.search:
            conditions = [getattr(self.model, field).like(f"%{filter.search}%") for field in search_fields]
            query = query.filter(or_(*conditions))
        if filters:
            query = self._apply_filters(query, filters)
        if filter.limit:
            return self.paginate(query, filter.page, filter.limit, filter.include, filter.search, include_deleted, search_fields)
        else:
            result = query.all()
        return {
            "data": [item.to_dict(include_relations=filter.include) for item in result],
        }
        
        
        
    def to_dict(self, items: List[ModelType] = None, include_deleted: bool = False, include_relations: list = None) -> List[dict]:
        items = items or self.all(include_deleted)
        return [item.to_dict(include_relations=include_relations) for item in items]
    
    
    def paginate(self, query: Query = None, page: int = 1, limit: int = None, include_relations: list = None, search: str = None, include_deleted: bool = False, search_fields: List[str] = ['name']) -> dict:
        if query is None:
            query = self._base_query(include_deleted)
        if limit is None:
            limit = settings.PROJECT_PAGINATION_LIMIT

        base_query = query
        total_query = self._base_query(include_deleted)
        if search:
            conditions = [getattr(self.model, field).like(f"%{search}%") for field in search_fields]
            total_query = total_query.filter(or_(*conditions))
            
        total = total_query.count()
        total_pages = math.ceil(total / limit) if total > 0 else 0
        page = min(page, total_pages) if total_pages else 1
        page = max(page, 1)

        query = base_query.offset((page - 1) * limit).limit(limit)
        data = self.db.execute(query).scalars().all()

        if not data and page > 1:
            page -= 1
            query = base_query.offset((page - 1) * limit).limit(limit)
            data = self.db.execute(query).scalars().all()

        return {
            "data": [item.to_dict(include_relations=include_relations) for item in data],
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }

    def create(self, input: BaseSchema) -> ModelType:
        """
        Create a new model or restore if it exists
        
        Args:
            input (dict): The input to create the model with
            
        Returns:
            ModelType: The created or restored model
        """
        input = input.model_dump(exclude_unset=True)
        
        restored_item = self._handle_unique_fields(input)
        if restored_item:
            return restored_item
            
        item = self.model(**input)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    
    def update(self, id: int, input: BaseSchema) -> ModelType:
        """
        Update a model by id
        
        Args:
            id (int): The id of the model to update
            input (dict): The input to update the model with
            
        Returns:
            ModelType: The updated model
        """
        item = self.find(id, include_deleted=True)
        input = input.model_dump(exclude_unset=True)
        self._validate_unique_fields(input, id=id)
        update_model_attributes(item, input)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete(self, id: int) -> ModelType:
        """
        Delete a model by id
        
        Args:
            id (int): The id of the model to delete
            
        Returns:
            ModelType: The deleted model
        """
        item = self.find(id)
        item.deleted_at = DateFormatter.current_datetime()
        self.db.commit()
        return item
    
    def restore(self, id: int, input: BaseSchema) -> ModelType:
        """
        Restore a model by id
        
        Args:
            id (int): The id of the model to restore
            input (dict): The input to restore the model with
        Returns:
            ModelType: The restored model
        """
        item = self.find(id, include_deleted=True)
        item.deleted_at = None
        update_model_attributes(item, input)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_many(self, ids: List[int]) -> None:
        """
        Delete multiple models by ids
        
        Args:
            ids (list[int]): The ids of the models to delete
            
        Returns:
            None
        """
        self.db.query(self.model).filter(self.model.id.in_(ids)).update({"deleted_at": DateFormatter.current_datetime()})
        self.db.commit()
    
    