from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.auth.entity import AuthInfoInResponse
from app.shared.decorator import response_decorator
from app.infra.security.security_service import _get_current_user
from app.use_cases.auth.login import LoginRequestObject, LoginUseCase

router = APIRouter()


@router.post("/login", response_model=AuthInfoInResponse)
@response_decorator()
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_use_case: LoginUseCase = Depends(LoginUseCase),
):
    """Get access token from credentials

    Args:
        form_data (OAuth2PasswordRequestForm, required): contains email, password for login
    Returns:
        access_token: str
        :param form_data:
        :param login_use_case:
    """
    login_request_object = LoginRequestObject.builder(
        data=dict(username=form_data.username, password=form_data.password),
    )
    response = login_use_case.execute(request_object=login_request_object)
    return response


@router.post("/logout", dependencies=[Depends(_get_current_user)])
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return True
