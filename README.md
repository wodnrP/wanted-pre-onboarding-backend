# wanted-pre-onboarding-backend 사전과제
### 지원자: 박재욱
### 🛠️ 사용기술
- Python3.9, Django4.2, MySQL8.0, Docker-compose, Django-UnitTest
---

### 📌 실행 방법

---

### 🖨️ 데이터베이스 테이블 구조 [ERD]
<center><img src="https://velog.velcdn.com/images/wodnr_09/post/ea16a295-730f-4745-b1b2-cd571de2dc08/image.png" width="600" height="600"></center>

---

### 🖥️ API 동작 데모 영상

---

### ❓ 구현 방법 및 이유
- django app을 굵은 기능 단위로 분리 (board, user) : 개발 편의성 & 유지보수성을 위함
  
- authentication.py에 jwt 토큰 생성 함수 구현, 이후 생성된 함수를 호출하여 회원가입, 로그인시 유효성 검사 후 jwt 토큰을 반환하도록 구현
  > 코드 복잡성을 낮추어 코드 가독성 위해 토큰 생성 함수 views.py에서 분리,
  >
  > 코드 중복성을 줄이기 위해 회원가입과 로그인시 같은 역할을 하는 코드를 함수화
  
- Authorization header에서 토큰이 존재하는지 검증하여 로그인한 사용자만 정보를 받을 수 있도록 구현 (게시글 작성, 수정, 삭제)
  > 사용자 인증을 jwt 토큰방식으로 구현했기 때문, 기밀성, 무결성, 가용성을 지키기 위함
  
- 게시글 전체 조회 API는 drf의 PageNumberPagination 모듈을 활용, page와 item 쿼리 스트링을 통해 한 페이지 별로 불러오는 items 수를 동적으로 제한
  > 클라이언트에서 페이지별로 불러 오는 items 수를 정함에 따라 API 호출 시 부하를 줄이기 위함
  
- try except 구문으로 에러처리 및 drf의 APIException 모듈로 에러 핸들링
  > 오류발생시 예외 사항을 최대한 줄이기 위함
  
- 툭정 게시글 수정 및 삭제 API에서 access_token을 decode하여 사용자 id를 추출하고, 해당 게시글을 작성한 사용자 id를 조회하여 서로 비교 후 해당 게시글을 작성한 사용자인지 판단 하도록 구현
  
- Django의 UnitTest를 활용하여 테스트 코드 구현
  > 테스트를 자동화하여 단위 테스트 시간을 줄이고자 함
  
- Docker-compose를 활용하여 어떤 환경에서든 배포를 간편화 하여 각 배포된 가상 컨테이너를 쉽게 조작하기 위함 

---

### 📝 API 명세 
| API | HTTP Method | End Point | Query String | Request Header | Request Body | Response | Description |
|--- |--- |--- |--- |--- |--- |--- |--- | 
| SignupAPIView  | POST | /users/signup |   |   | {"email":"string", "password":"string", "nickname":"string"} | {"access_token":"string", "access_exp":int, "refresh_token":"string"} | 회원가입 |
| LoginAPIView | POST | /users/login |   |   | {"email":"string", "password":"string"} | {"access_token":"string", "access_exp":int, "refresh_token":"string"} | 로그인 |
| BoardAPIView | POST | /boards/ |   | Authorization Bearer <access_toekn> | {"user":int, "title":"string", "contents":"string"} | {"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"} |  게시글 작성  | 
| BoardAPIView | GET | /boards | ?page=1&items=5  |   |   | [{"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"}..] |  전체 게시글 조회 (페이지 수 와 한 페이지 당 item 갯수 지정 가능) | 
| BoardDetailAPIView | GET | /boards/board_id |   |   |   | {"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"} |  특정 게시글 조회 (End Point에 게시글 ID 지정) | 
| BoardDetailAPIView | PATCH | /boards/board_id |   | Authorization Bearer <access_toekn> | {"title":"string", "contents":"string"} | 200:{"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"}, 400:{'Message':'해당 게시글 작성자가 아닙니다.'} |  특정 게시글 수정 (End Point에 게시글 ID 지정) | 
| BoardDetailAPIView | DELETE | /boards/board_id |   | Authorization Bearer <access_toekn> |   | 200:{'Message':'Success'}, 400:{'Message':'해당 게시글 작성자가 아닙니다.'} | 특정 게시글 삭제 (End Point에 게시글 ID 지정) | 

