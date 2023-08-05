from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from .authentication import create_access_token, create_refresh_token, access_token_exp
from .serializer import UserSerializer
from .models import User

# Create your views here.

# 회원가입 에러 처리
class SignupException(APIException):
    status_code = 400
    default_detail = '실패! 입력한 정보를 다시 확인해주세요'
    default_code = 'KeyNotFound'

# 로그인 에러 처리 
class LoginException(APIException):
    status_code = 400
    default_detail = '아이디 혹은 비밀번호를 다시 확인해주세요'
    default_code = 'KeyNotFound'

class EmailException(APIException):
    status_code = 400
    default_detail = '올바른 이메일 형식이 아닙니다. @를 입력해주세요.'
    default_code = 'KeyNotFound'

class PasswordException(APIException):
    status_code = 400
    default_detail = '비밀번호를 8자리 이상 입력해주세요'
    default_code = 'KeyNotFound'

# 로그인시 토큰 생성 함수
def token_create(user):    
    access_token = create_access_token(user.id)
    access_exp = access_token_exp(access_token)
    refresh_token = create_refresh_token(user.id)

    response = Response(status=status.HTTP_201_CREATED)
    response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)         #리프레쉬 토큰 쿠키에 저장
    response.data = {
        'access_token' : access_token,
        'access_exp' : access_exp,
        'refresh_token' : refresh_token
    }
    return response

# 회원가입 API (회원가입시 즉시 로그인)
class SignupAPIView(APIView):
    def post(self, request):
        # email 유효성 검사 : @ 포함 
        if "@" not in request.data['email']:
            raise EmailException()
        # password 유효성 검사 : 8자 이상
        if len(request.data['password']) <= 8 :
            raise PasswordException()
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.filter(email=request.data['email']).first()
            
            # 중복되는 유저가 있는지 확인
            if not user:
                raise SignupException()
            if not user.check_password(request.data['password']):
                raise SignupException()

            # 가입한 유저 토큰 생성 및 로그인
            return token_create(user)

# 로그인 API
class LoginAPIView(APIView):
    def post(self, request):
        # email 유효성 검사 : @ 포함 
        if "@" not in request.data['email']:
            raise EmailException()
        # password 유효성 검사 : 8자 이상
        if len(request.data['password']) <= 8 :
            raise PasswordException()
        
        user = User.objects.filter(email=request.data['email']).first()
        
        # 사용자의 회원 정보가 있는지 확인      
        if not user:
            raise LoginException()
        
        # 사용자의 패스워드가 존재하는지 확인
        if not user.check_password(request.data['password']):
            raise LoginException()
        
        return token_create(user)

# 로그아웃 API
class LogoutAPIView(APIView):
    
    def delete(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'Message' : 'Logout success'
        }
        return response



