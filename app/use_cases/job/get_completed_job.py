from typing import List, Union

from app.shared.response_object import ResponseFailure
from fastapi import Depends
from app.shared import request_object, response_object, use_case
from app.infra.database.models.user import User as UserModel
from app.infra.database.models.job import Jobs as JobModel
from app.domain.job.entity import Job, JobInDB
from app.infra.job.job_repository import JobRepository


class GetCompletedJobRequestObject(request_object.ValidRequestObject):
    def __init__(self, current_user: UserModel):
        self.current_user = current_user

    @classmethod
    def builder(cls, current_user: UserModel) -> request_object.RequestObject:
        return GetCompletedJobRequestObject(current_user=current_user)


class GetCompletedJobUseCase(use_case.UseCase):
    def __init__(self, job_repository: JobRepository = Depends(JobRepository)):
        self.job_repository = job_repository

    def process_request(self, req_object: GetCompletedJobRequestObject) -> Union[ResponseFailure, list[Job]]:
        completed_jobs: List[JobModel] = self.job_repository.find({
            "owner": req_object.current_user.id,
            "is_completed": True
        })

        if not completed_jobs:
            return response_object.ResponseFailure.build_not_found_error(message="No completed jobs found.")

        return [Job(**JobInDB.model_validate(job).model_dump()) for job in completed_jobs]
