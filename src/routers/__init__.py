from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


from src.schemas.activity_type_template import ActivityType
from src.querys.activity_types_query import activity_types_query

from src.database import Database

router = APIRouter()

@router.get(""