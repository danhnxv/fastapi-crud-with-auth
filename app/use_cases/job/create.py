from typing import Optional, Dict
from fastapi import Depends

from app.shared import request_object, use_case, response_object
from app.infra.database.models.job import Jobs as JobModel
from app.infra.database.models.user import User as UserModel
from app.domain.job.entity import JobInCreate, JobInDB, Job
from app.infra.job.job_repository import JobRepository


class CreateJobRequestObject(request_object.ValidRequestObject):
    def __init__(self, obj_in: JobInCreate = None, current_user: UserModel = None) -> None:
        self.obj_in = obj_in
        self.current_user = current_user

    @classmethod
    def builder(cls, payload: Optional[JobInCreate], current_user: UserModel) -> request_object.RequestObject:
        invalid_req = request_object.InvalidRequestObject()
        if payload is None:
            invalid_req.add_error("payload", "Invalid payload")

        if invalid_req.has_errors():
            return invalid_req

        return CreateJobRequestObject(obj_in=payload, current_user=current_user)


class CreateJobUseCase(use_case.UseCase):
    def __init__(
            self,
            job_repository: JobRepository = Depends(JobRepository),
    ):
        self.job_repository = job_repository

    def process_request(self, req_object: CreateJobRequestObject):
        job_in: JobInCreate = req_object.obj_in
        job: Optional[JobInDB] = self.job_repository.get_by_name(name=job_in.name)
        if job:
            return response_object.ResponseFailure.build_system_error("Job already existed")

        obj_in: JobInDB = JobInDB(**job_in.model_dump(), owner=req_object.current_user)
        job: JobModel = self.job_repository.create(obj_in=obj_in)

        # Update client
        data: Dict[str, bool] = {}
        self.job_repository.update(id=job.id, data=data)
        return Job(**JobInDB.model_validate(job).model_dump())
