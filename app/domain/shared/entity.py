from datetime import datetime, date
from pydantic import BaseModel, field_validator, Field, ConfigDict
from fastapi import Query
from typing import Optional

from app.domain.shared.field import PydanticObjectId


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    @classmethod
    def from_mongo(cls, data: dict, id_str=False):
        """We must convert _id into "id"."""
        if not data:
            return data
        job_id = data.pop("_id", None) if not id_str else str(data.pop("_id", None))
        return cls(**dict(data, id=job_id))

    def to_mongo(self, **kwargs):
        exclude_unset = kwargs.pop("exclude_unset", True)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = parsed.pop("id")

        return parsed


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("created_at", "updated_at", mode="after")
    def set_datetime_now(cls, value: datetime) -> datetime:
        return value or datetime.utcnow()


class IDModelMixin(BaseModel):
    id: Optional[PydanticObjectId] = None


class Pagination(BaseModel):
    total: Optional[int] = 0
    page_index: Optional[int] = 1
    page_size: Optional[int] = 5
    total_pages: Optional[int] = None


class SearchRequest(BaseModel):
    start_date: Optional[date] = Field(
        Query(
            None,
            title="From date: YYYY-MM-DD",
        ),
    )
    end_date: Optional[date] = Field(Query(None, title="End Date: YYYY-MM-DD"))


class CustomDocument:
    @classmethod
    def from_mongo(cls, data: dict, id_str=False):
        """We must convert _id into "id". """
        if not data:
            return data
        data.pop("_id", None) if not id_str else str(data.pop("_id", None))
        if "_cls" in data:
            data.pop("_cls", None)
        return cls()
