from fastapi import APIRouter, status, HTTPException, Query

from account.adapter.input.web.request.UserRequest import UserRegisterRequest
from account.adapter.input.web.response.UserResponse import UserProfileResponse

from account.application.usecase.user_usecase import UserUseCase

from account.domain.user_enums import ProviderType
from account.infrastructure.repository.user_repository_impl import UserRepositoryImpl
from account.application.service.impl.password_hash_impl import BcryptHasher
from account.domain.exceptions.user_exceptions import UserAlreadyExistsError, InvalidUserDataError, \
    UserNotFoundException

user_router = APIRouter()
usecase = UserUseCase(UserRepositoryImpl())

hasher = BcryptHasher()

@user_router.post("/register",response_model=UserProfileResponse,status_code=status.HTTP_201_CREATED,summary="로컬 계정 회원가입")
def register_user_endpoint(request: UserRegisterRequest):
    try:
        hashed_password = hasher.hash(request.password)
        user_domain = usecase.register_user(
            email=request.email,
            hashed_password=hashed_password,
            name=request.name,
            nickname=request.nickname,
            agree_yn=request.agree_marketing,
            provider=ProviderType.LOCAL
        )
        return UserProfileResponse.from_domain(user_domain)

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except InvalidUserDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@user_router.get("/id/{user_id}", response_model=UserProfileResponse, summary="회원 정보 조회")
def get_user_by_id(user_id: int):
    try:
        user_domain = usecase.get_user_by_id(user_id)
        return UserProfileResponse.from_domain(user_domain)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@user_router.get("/email", response_model=UserProfileResponse, summary="회원 정보 조회")
def get_user_by_email(email: str = Query(..., description="조회할 사용자 이메일")):
    try:
        user_domain = usecase.get_user_by_email(email)
        return UserProfileResponse.from_domain(user_domain)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )