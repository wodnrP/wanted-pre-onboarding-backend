# wanted-pre-onboarding-backend 사전과제
### 지원자: 박재욱

### 실행 방법

---

### 데이터베이스 테이블 구조 [ERD]

---

### API 동작 데모 영상

---

### 구현 방법 및 이유

---

### API 명세 
| API | HTTP Method | End Point | Query String | Request Header | Request Body | Response | Description |
|--- |--- |--- |--- |--- |--- |--- |--- | 
| SignupAPIView  | POST | /users/signup |   |   | {"email":"string", "password":"string", "nickname":"string"} | {"access_token":"string", "access_exp":int, "refresh_token":"string"} | 회원가입 |
| LoginAPIView | POST | /users/login |   |   | {"email":"string", "password":"string"} | {"access_token":"string", "access_exp":int, "refresh_token":"string"} | 로그인 |
| BoardAPIView | POST | /boards/ |   | Authorization Bearer <access_toekn> | {"user":int, "title":"string", "contents":"string"} | {"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"} |  게시글 작성  | 
| BoardAPIView | GET | /boards | ?page=1&items=5  |   |   | [{"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"}..] |  전체 게시글 조회 (페이지 수 와 한 페이지 당 item 갯수 지정 가능) | 
| BoardDetailAPIView | GET | /boards/board_id |   |   |   | {"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"} |  특정 게시글 조회 (End Point에 게시글 ID 지정) | 
| BoardDetailAPIView | PATCH | /boards/board_id |   | Authorization Bearer <access_toekn> | {"title":"string", "contents":"string"} | 200:{"id":int, "user":int, "title":"string", "contents":"string", "create_time":"string", "update_time":"string"}, 400:{'Message':'해당 게시글 작성자가 아닙니다.'} |  특정 게시글 수정 (End Point에 게시글 ID 지정) | 
| BoardDetailAPIView | DELETE | /boards/board_id |   | Authorization Bearer <access_toekn> |   | 200:{'Message':'Success'}, 400:{'Message':'해당 게시글 작성자가 아닙니다.'} | 특정 게시글 삭제 (End Point에 게시글 ID 지정) | 

