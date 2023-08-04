from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from .authentication import create_access_token, create_refresh_token, decode_refresh_token, access_token_exp
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

class TokenErrorException(APIException):
    status_code = 403
    if status_code == 403:
        status_code = 401
    default_detail = 'unauthenticated'

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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.filter(username=request.data['email']).first()
            
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
        user = User.objects.filter(username=request.data['username']).first()
        if not user:
            raise LoginException()
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


# refresh login
class RefreshAPIView(APIView):
    def post(self, request):
        token = request.data['refresh_token']
        
        byt_token = bytes(token, 'utf-8')

        id = decode_refresh_token(byt_token)
        access_token = create_access_token(id)
        access_exp = access_token_exp(access_token)
        return Response({
            'access_token': access_token,
            'access_exp': access_exp
        })

