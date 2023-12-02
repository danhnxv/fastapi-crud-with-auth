from typing import Optional
from fastapi import Depends
from app.infra.database.models.job import Jobs as JobModel
from app.shared import request_object, use_case, response_object

from app.domain.job.entity import JobInUpdate, JobInDB, Job
from app.infra.job.job_repository import JobRepository


class UpdateJobRequestObject(request_object.ValidRequestObject):
    def __init__(self, id: str, obj_in: JobInUpdate) -> None:
        self.id = id
        self.obj_in = obj_in

    # Custom builder method for UpdateJobRequestObject
    @classmethod
    def build(cls, id: str, payload: Optional[JobInUpdate]):
        invalid_req = request_object.InvalidRequestObject()
        if id is None:
            invalid_req.add_error("id", "Invalid job id")

        if payload is None:
            invalid_req.add_error("payload", "Invalid payload")

        if invalid_req.has_errors():
            return invalid_req

        return UpdateJobRequestObject(id=id, obj_in=payload)


class UpdateJobUseCase(use_case.UseCase):
    def __init__(self, client_repository: JobRepository = Depends(JobRepository)):
        self.client_repository = client_repository

    def process_request(self, req_object: UpdateJobRequestObject):
        job: Optional[JobModel] = self.client_repository.get_by_id(id=req_object.id)
        if not job:
            return response_object.ResponseFailure.build_not_found_error("Client does not exist")

        self.client_repository.update(id=job.id, data=req_object.obj_in)
        job.reload()
        return Job(**JobInDB.model_validate(job).model_dump())
