from datetime import datetime
from typing import Optional, List
from pydantic import ConfigDict
from app.domain.shared.entity import BaseEntity, IDModelMixin, DateTimeModelMixin, Pagination
from app.domain.user.field import PydanticUserType


class JobBase(BaseEntity):
    name: str
    description: str
    is_completed: Optional[bool] = False


class JobInDB(IDModelMixin, DateTimeModelMixin, JobBase):
    model_config = ConfigDict(from_attributes=True)
    owner: PydanticUserType


class JobInCreate(JobBase):
    pass


class JobInUpdate(BaseEntity):
    name: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = False


class Job(JobBase):
    id: str
    created_at: datetime
    updated_at: datetime


class ManyJobsInResponse(BaseEntity):
    pagination: Optional[Pagination] = None
    data: Optional[List[Job]] = None
