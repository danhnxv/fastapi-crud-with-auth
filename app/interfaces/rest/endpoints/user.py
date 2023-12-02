from fastapi import APIRouter, Body, Depends, Path
from app.domain.user.entity import User, UserInCreate
from app.shared.decorator import response_decorator

from app.use_cases.user.get import (
    GetUserRequestObject,
    GetUserCase,
)
from app.use_cases.user.create import (
    CreateUserRequestObject,
    CreateUserUseCase,
)

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=User,
)
@response_decorator()
def get_user(
        user_id: str = Path(..., title="User id"),
        get_user_use_case: GetUserCase = Depends(GetUserCase),
):
    get_user_request_object = GetUserRequestObject.builder(user_id=user_id)
    response = get_user_use_case.execute(request_object=get_user_request_object)
    return response


@router.post(
    "/",
    response_model=User,
)
@response_decorator()
def create_user(
        payload: UserInCreate = Body(..., title="UserInCreate payload"),
        create_user_use_case: CreateUserUseCase = Depends(CreateUserUseCase),
):
    req_object = CreateUserRequestObject.builder(payload=payload)
    response = create_user_use_case.execute(request_object=req_object)
    return response
