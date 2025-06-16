from sqlalchemy import event
from sqlalchemy.orm import Query
from sqlalchemy.orm.util import AliasedInsp

from app.modules.common.dependencies import get_global_company_id

def has_company_id_filter(query, company_id):
    for desc in query._where_criteria:
        if hasattr(desc, 'left') and hasattr(desc.left, 'name') and desc.left.name == 'company_id':
            return True
    return False

@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    company_id = get_global_company_id()
    if not company_id:
        return query

    
    try:
        entities = [
            ent.entity_zero.class_
            for ent in query._compile_state()._entities
            if hasattr(ent, 'entity_zero') and ent.entity_zero and not isinstance(ent.entity_zero, AliasedInsp)
        ]
    except Exception:
        return query

    for model in entities:
        # Case 1: has company_id column directly
        if hasattr(model, 'company_id'):
            if not has_company_id_filter(query):
                query = query.filter(model.company_id == company_id)

        # Case 2: model has many-to-many relation
        elif hasattr(model, '__company_filter__'):
            relation_attr = getattr(model, '__company_filter__')
            relation = getattr(model, relation_attr, None)
            if relation:
                query = query.join(relation).filter_by(id=company_id)

    return query
