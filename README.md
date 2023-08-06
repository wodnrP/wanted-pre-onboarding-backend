# wanted-pre-onboarding-backend 사전과제
### 지원자: 박재욱
### 🛠️ 사용기술
- Python3.9, Django4.2, MySQL8.0, Docker-compose, Django-UnitTest
---

### 📌 실행 방법
#### 기본 환경 셋팅
- python3.9X 설치
- (Mac 기준) brew 설치 및
  ```
  $ brew update
  ```
- 패키지 설치를 위해 pip 설치
  ```
  $ sudo easy_install pip
  ```
- [Docker 설치](https://www.docker.com/)
- Docer-compose 설치

  ```
  $ sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  ```
- Docker-compose에 권한 설정

  ```
  $ sudo chmod +x /usr/local/bin/docker-compose
  ```
- 심볼릭 링크 설정
  ```
  $ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
  ```
- 가상 환경 생성 및 실행
  ```
  $ python3 -m venv ./{your venv name}    가상환경 생성
  $ source {your venv name}/bin/activate  가상환경 실행
  ```
- 프로젝트 git clone
  ```
  $ git clone https://github.com/wodnrP/wanted-pre-onboarding-backend.git
  ```
  - clone 받은 폴더에서 root 디렉토리로 모든 파일 및 폴더 이동 후, clone 받은 폴더 삭제
 
- MySQL 서버 실행
  ```
  $ mysql.server start
  ```
- MySQL root 계정으로 접속
  ```
  $ mysql -u root -p
  ```
- DB 생성
  ```
  mysql> CREATE DATABASE DB이름 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
  ```
- 헤당 DB 적용 후 show tables로 확인 
  ```
  mysql> use DB이름;
  Database changed

  mysql> show tables;
  Empty set (0.00 sec)
  ```
- DB 사용자 생성 후 권한 부여
  ```
  mysql> CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
  mysql> GRANT ALL PRIVILEGES ON 적용할 DB이름 TO 'newuser'@'localhost' WITH GRANT OPTION;
  mysql> FLUSH PRIVILEGES;
  ```
- Docker-compose.yml과 같은 위치에 .env 파일 생성
  ```
  # .env
  # docker compose db password
  MYSQL_DB=wantedDB                  // 생성한 DB이름
  MYSQL_HOST=localhost               // local server
  MYSQL_USER=wantedAdmin             // 생성한 사용자
  MYSQL_PASSWORD=Parkjaeouk7#        // 생성한 사용자 비밀번호
  MYSQL_ROOT_PASSWORD=parkjaeouk7!   // root 계정 비밀번호
  ```
- app 디렉토리 내부에 .env 파일 생성
  - https://djecrety.ir/ 에서 django secret_key 생성 후 .env file에 적용   
  ```
  DEBUG=true or false
  SECRET_KEY=...
  ```
- config (project 디렉토리) 폴더 안, settings.py와 같은 위치에 my_settings.py 생성
  ```
  # my_settings.py
  DATABASES = {
      'default' : {
          'ENGINE': 'django.db.backends.mysql',    
          'NAME': 'wantedDB',                    # 사용할 DB이름
          'USER': 'wantedAdmin',                 # DB 사용자      
          'PASSWORD': 'Parkjaeouk7#',            # 사용자 비밀번호      
          'HOST': 'mysql',                       # .yml mysql의 container_name
          'PORT': '3306',                        # mysql port번호
      }
  }
  ```
- Django에 MySQL 마이그레이션
  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```
  #### 실행
- docker-compose 실행
  ```
  docker-compose up -d —build
  ```
- ⚠️ 다음과 같은 에러 발생
  ```
  django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on 'mysql' (115)")
  ```
  - my_settings.py ‘HOST’:’localhost’로 수정 후 docker-compose up -d —build
  
  - 에러 재발생
  ```
  django.db.utils.OperationalError: (2002, "Can't connect to local MySQL server through socket '/run/mysqld/mysqld.sock' (2)")
  ```
  - 다시 my_settings.py ‘HOST’:’mysql’로 수정 후 ```docker-compose up -d —build```
  - **127.0.0.1:8000/boards 접속으로 정상 작동 확인**
 
- ⚠️ 두번째 회원의 회원가입 API 작동 시 (1062, "Duplicate entry '' for key 'user_user.username'") 발생할 경우
  - docker-compose 컨테이너 내부에 admin 계정 생성
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
  - **127.0.0.1:8000/admin**으로 접속하여 User 페이지에서 이미 생성된 회원들의 username을 각각 다르게 수정 후 다시 회원가입 진행 가능 

- ### 📂 (참고) 셋팅된 디렉토리 구조
  > #### root 디렉토리
  > - app
  >   - config 
  >   - boards
  >   - user
  >   - staticfiles
  >   - manage.py
  >   - .env (Secret_key)
  > - db
  >   - conf.d
  >   - data
  > - Dockerfile 
  > - docker-compose.yml
  > - requirements.txt
  > - .gitignore
  > - README.md
  > - .env (docker-compose db env) 
---

### 🖨️ 데이터베이스 테이블 구조 [ERD]
<center><img src="https://velog.velcdn.com/images/wodnr_09/post/ea16a295-730f-4745-b1b2-cd571de2dc08/image.png" width="600" height="600"></center>

---

### 🖥️ API 동작 데모 영상
[API 동작 데모 영상 링크 : docker-compose local server postman 동작](https://drive.google.com/file/d/1c9l6MqxHXVfoUZ1I5adGdPsa6Q6rC9VG/view?usp=drive_link)
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

