from typing import Dict
from fastapi import APIRouter, Depends, Body, Path, Query
from app.shared.decorator import response_decorator
from app.domain.job.entity import Job, JobInCreate, JobInUpdate, ManyJobsInResponse
from app.infra.security.security_service import get_current_user
from app.infra.database.models.user import User
from app.use_cases.job import (ListJobUseCase,
                               ListJobRequestObject, CreateJobUseCase, CreateJobRequestObject,
                               GetJobRequestObject, GetJobUseCase, UpdateJobUseCase, UpdateJobRequestObject,
                               DeleteJobUseCase, DeleteJobRequestObject, GetCompletedJobUseCase,
                               GetCompletedJobRequestObject)

router = APIRouter()


@router.get("/", response_model=ManyJobsInResponse)
@response_decorator()
def list_job(
        page_index: int = Query(default=1, title="Page index"),
        page_size: int = Query(default=5, title="Page size"),
        current_user: User = Depends(get_current_user),
        get_list_job_use_case: ListJobUseCase = Depends(ListJobUseCase)
):
    req_object = ListJobRequestObject.builder(
        current_user=current_user, page_index=page_index, page_size=page_size
    )
    response = get_list_job_use_case.execute(request_object=req_object)
    return response


@router.post("/", response_model=Job)
@response_decorator()
def create_job(
        payload: JobInCreate = Body(..., title="JobInCreate payload"),
        current_user: User = Depends(get_current_user),
        create_job_use_case: CreateJobUseCase = Depends(CreateJobUseCase),
):
    req_object = CreateJobRequestObject.builder(payload=payload, current_user=current_user)
    response = create_job_use_case.execute(request_object=req_object)
    return response


@router.get(
    "/completed-jobs",
    response_model=Job,
)
@response_decorator()
def get_completed_job(
        current_user: User = Depends(get_current_user),
        get_active_client_use_case: GetCompletedJobUseCase = Depends(GetCompletedJobUseCase),
):
    req_object = GetCompletedJobRequestObject.builder(current_user=current_user)
    response = get_active_client_use_case.execute(request_object=req_object)
    return response


@router.get(
    "/{job_id}",
    dependencies=[Depends(get_current_user)],  # auth route
    response_model=Job,
)
@response_decorator()
def get_job(
        job_id: str = Path(..., title="Job Id"),
        get_job_use_case: GetJobUseCase = Depends(GetJobUseCase),
):
    req_object = GetJobRequestObject.builder(id=job_id)
    response = get_job_use_case.execute(request_object=req_object)
    return response


@router.put(
    "/{job_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Job,
)
@response_decorator()
def update_job(
        job_id: str = Path(..., title="Job Id"),
        payload: JobInUpdate = Body(..., title="Job updated payload"),
        update_job_use_case: UpdateJobUseCase = Depends(UpdateJobUseCase),
):
    req_object = UpdateJobRequestObject.build(id=job_id, payload=payload)
    response = update_job_use_case.execute(request_object=req_object)
    return response


@router.delete(
    "/{job_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Dict[str, bool],
)
@response_decorator()
def delete_account(
        job_id: str = Path(..., title="Job Id"),
        delete_job: DeleteJobUseCase = Depends(DeleteJobUseCase),
):
    req_object = DeleteJobRequestObject.builder(id=job_id)
    response = delete_job.execute(request_object=req_object)
    return response
