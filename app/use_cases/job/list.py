import math
from fastapi import Depends
from typing import Optional, List
from app.infra.job.job_repository import JobRepository
from app.domain.job.entity import ManyJobsInResponse, Job, JobInDB
from app.domain.shared.entity import Pagination
from app.infra.database.models.job import Jobs as JobModel
from app.shared import request_object, use_case
from app.infra.database.models.user import User


class ListJobRequestObject(request_object.ValidRequestObject):
    def __init__(self, current_user: User, page_index: int = 1, page_size: int = 5):
        self.current_user = current_user
        self.page_index = (page_index,)
        self.page_size = page_size

    @classmethod
    def builder(cls, current_user: User, page_index: int = 1, page_size: int = 5) -> request_object.RequestObject:
        return ListJobRequestObject(current_user=current_user, page_index=page_index, page_size=page_size)


class ListJobUseCase(use_case.UseCase):
    def __init__(
            self,
            job_repository: JobRepository = Depends(JobRepository),
    ):
        self.job_repository = job_repository

    def process_request(self, req_object: ListJobRequestObject):
        job: Optional[List[JobModel]] = self.job_repository.list(
            owner=req_object.current_user,
            page_index=req_object.page_index[0],
            page_size=req_object.page_size,
        )
        total = self.job_repository.count({"owner": req_object.current_user.id})
        print(req_object)
        return ManyJobsInResponse(
            pagination=Pagination(
                total=total,
                page_index=req_object.page_index[0],
                page_size=req_object.page_size,
                total_pages=math.ceil(total / req_object.page_size)
            ),
            data=[Job(**JobInDB.model_validate(ns).model_dump()) for ns in job],
        )
