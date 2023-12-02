from typing import Optional
from fastapi import Depends
from app.shared import request_object, response_object, use_case
from app.infra.database.models.job import Jobs as JobModel
from app.infra.job.job_repository import JobRepository
from bson import ObjectId


class DeleteJobRequestObject(request_object.ValidRequestObject):
    def __init__(self, id: str):
        self.id = id

    @classmethod
    def builder(cls, id: str) -> request_object.RequestObject:
        invalid_req = request_object.InvalidRequestObject()
        if not id:
            invalid_req.add_error("id", "Invalid")

        if invalid_req.has_errors():
            return invalid_req

        return DeleteJobRequestObject(id=id)


class DeleteJobUseCase(use_case.UseCase):
    def __init__(self, job_repository: JobRepository = Depends(JobRepository)):
        self.job_repository = job_repository

    def process_request(self, req_object: DeleteJobRequestObject):
        job: Optional[JobModel] = self.job_repository.get_by_id(id=req_object.id)
        if not job:
            return response_object.ResponseFailure.build_not_found_error(message="Job does not exist.")

        # Convert str ID to ObjectId
        object_id = ObjectId(req_object.id)
        self.job_repository.delete(object_id)
        return {"success": True}
