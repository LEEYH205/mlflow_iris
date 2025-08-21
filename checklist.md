# 🚀 MLOps CI/CD 체크리스트

이 문서는 MLOps 프로젝트의 CI/CD 파이프라인에서 체크해야 할 모든 사항들을 정리한 것입니다.

## 📋 **1. 환경 설정 체크리스트**

### **1.1 Python 환경**
- [ ] Python 가상환경 생성 (`.venv`)
- [ ] `requirements.txt` 파일 존재 및 최신화
- [ ] 모든 의존성 패키지 설치 확인
- [ ] Python 버전 호환성 확인 (3.10+)

### **1.2 개발 도구 설치**
- [ ] `git` 설치 및 설정
- [ ] `docker` 설치 및 실행 권한
- [ ] `dvc` 설치 (데이터 버전 관리용)

## 🔧 **2. 코드 품질 도구 체크리스트**

### **2.1 필수 도구 설치**
- [ ] `pytest` - 테스트 실행
- [ ] `pytest-cov` - 코드 커버리지
- [ ] `black` - 코드 포맷팅
- [ ] `isort` - import 정렬
- [ ] `flake8` - 코드 스타일 검사
- [ ] `bandit` - 보안 검사
- [ ] `safety` - 보안 취약점 검사

### **2.2 도구 설정 파일**
- [ ] `pyproject.toml` - black/isort 설정 통합
- [ ] `.vscode/settings.json` - VS Code 자동 포맷팅
- [ ] `.pre-commit-config.yaml` - Git hooks 설정

### **2.3 코드 품질 검사**
- [ ] `black --check` - 코드 포맷팅 검사 통과
- [ ] `isort --check-only` - import 정렬 검사 통과
- [ ] `flake8` - 코드 스타일 검사 통과
- [ ] `bandit` - 보안 검사 통과
- [ ] `safety check` - 취약점 검사 통과

## 🧪 **3. 테스트 체크리스트**

### **3.1 테스트 환경**
- [ ] `tests/` 폴더 존재
- [ ] `test_*.py` 파일들 작성
- [ ] `pytest` 실행 가능

### **3.2 테스트 실행**
- [ ] `pytest tests/` - 단위 테스트 통과
- [ ] `pytest --cov` - 코드 커버리지 측정
- [ ] 테스트 커버리지 80% 이상 달성

## 🐘 **4. DVC (Data Version Control) 체크리스트**

### **4.1 DVC 초기화**
- [ ] `dvc init` 실행
- [ ] `.dvc/` 폴더 생성 확인
- [ ] `.dvcignore` 파일 설정

### **4.2 원격 저장소 설정**
- [ ] 로컬 저장소 설정 (`~/dvc-storage`)
- [ ] `dvc remote add local ~/dvc-storage`
- [ ] `dvc remote default local`

### **4.3 데이터 추적**
- [ ] `artifacts/` 폴더 DVC 추적
- [ ] `reports/` 폴더 DVC 추적
- [ ] `.dvc` 파일 Git에 추가
- [ ] `artifacts.dvc`, `reports.dvc` 파일 생성

### **4.4 DVC 상태 확인**
- [ ] `dvc status` - 상태 확인
- [ ] `dvc list .` - 추적 파일 목록
- [ ] `dvc push` - 원격 저장소 동기화

## 🐳 **5. Docker 체크리스트**

### **5.1 Dockerfile 검사**
- [ ] `Dockerfile` 존재 및 문법 검사
- [ ] 베이스 이미지 설정 (`python:3.10-slim`)
- [ ] 의존성 설치 순서 최적화
- [ ] 멀티스테이지 빌드 고려

### **5.2 Docker 빌드 테스트**
- [ ] `docker build -t test-image .` 성공
- [ ] 이미지 크기 최적화 확인
- [ ] 보안 취약점 검사

### **5.3 Docker 실행 테스트**
- [ ] `docker run` 컨테이너 시작 성공
- [ ] 포트 매핑 확인 (8000)
- [ ] 헬스체크 엔드포인트 응답 확인

## 🚀 **6. CI/CD 파이프라인 체크리스트**

### **6.1 GitHub Actions 설정**
- [ ] `.github/workflows/ci.yml` 파일 존재
- [ ] 트리거 설정 (`on: push`, `on: pull_request`)
- [ ] 환경 변수 설정 (`PYTHON_VERSION`, `DOCKER_IMAGE`)

### **6.2 CI/CD Job 구성**
- [ ] **code-quality**: 코드 품질 검사
- [ ] **test**: 단위 테스트 실행
- [ ] **mlflow-test**: MLflow 모델 훈련 테스트
- [ ] **docker-build**: Docker 이미지 빌드
- [ ] **integration-test**: 통합 테스트
- [ ] **summary**: 결과 요약

### **6.3 CI/CD 실행 확인**
- [ ] GitHub Actions 워크플로우 실행
- [ ] 모든 Job 성공 (초록색 체크마크)
- [ ] 실패한 Job 로그 분석 및 수정
- [ ] CI/CD 파이프라인 완료 시간 최적화

## 📊 **7. MLflow 체크리스트**

### **7.1 MLflow 설정**
- [ ] `mlflow` 패키지 설치
- [ ] MLflow UI 실행 가능 (`mlflow ui`)
- [ ] 실험 추적 설정

### **7.2 모델 훈련 및 로깅**
- [ ] `python src/train.py` 실행 성공
- [ ] MLflow에 실험 로깅
- [ ] 메트릭, 파라미터, 아티팩트 저장
- [ ] 모델 파일 생성 (`artifacts/model.pkl`)

### **7.3 MLflow UI 확인**
- [ ] `http://127.0.0.1:5000` 접속 가능
- [ ] 실험 결과 확인
- [ ] 모델 아티팩트 다운로드 가능

## 🔌 **8. FastAPI 체크리스트**

### **8.1 FastAPI 앱 설정**
- [ ] `app/main.py` 파일 존재
- [ ] FastAPI 인스턴스 생성
- [ ] 모델 로딩 함수 구현
- [ ] 에러 핸들링 구현

### **8.2 API 엔드포인트**
- [ ] `GET /health` - 헬스체크
- [ ] `POST /predict` - 모델 예측
- [ ] `GET /docs` - Swagger UI
- [ ] `GET /redoc` - ReDoc 문서

### **8.3 API 테스트**
- [ ] `uvicorn app.main:app --reload` 실행
- [ ] `http://127.0.0.1:8000` 접속 가능
- [ ] Swagger UI에서 API 테스트
- [ ] `curl` 명령어로 API 호출 테스트

## 📈 **9. 데이터 품질 체크리스트**

### **9.1 Evidently 리포트**
- [ ] `python src/report.py` 실행 성공
- [ ] `reports/data_quality_report.html` 생성
- [ ] 데이터 품질 지표 확인
- [ ] HTML 리포트 브라우저에서 확인

### **9.2 데이터 검증**
- [ ] 훈련 데이터와 테스트 데이터 분할
- [ ] 데이터 타입 및 범위 검증
- [ ] 결측값 및 이상치 확인
- [ ] 특성 분포 분석

## 🔍 **10. 최종 검증 체크리스트**

### **10.1 전체 워크플로우 테스트**
- [ ] 모델 훈련 → MLflow 로깅 → FastAPI 서빙 → API 테스트
- [ ] Docker 빌드 → 컨테이너 실행 → API 테스트
- [ ] DVC 데이터 관리 → Git 커밋 → CI/CD 실행

### **10.2 성능 및 안정성**
- [ ] API 응답 시간 측정
- [ ] 모델 예측 정확도 확인
- [ ] 에러 핸들링 테스트
- [ ] 로그 및 모니터링 확인

### **10.3 문서화**
- [ ] `README.md` 업데이트
- [ ] API 문서 자동 생성
- [ ] 설정 파일 주석 추가
- [ ] 트러블슈팅 가이드 작성

## 🎯 **11. CI/CD 성공 기준**

### **11.1 모든 Job 성공**
- [ ] `code-quality`: ✅ 성공
- [ ] `test`: ✅ 성공  
- [ ] `mlflow-test`: ✅ 성공
- [ ] `docker-build`: ✅ 성공
- [ ] `integration-test`: ✅ 성공
- [ ] `summary`: ✅ 성공

### **11.2 최종 결과**
- [ ] GitHub Actions에서 모든 Job 초록색 체크마크
- [ ] CI/CD 파이프라인 완료 시간 < 5분
- [ ] 코드 커버리지 > 80%
- [ ] 보안 검사 통과
- [ ] Docker 이미지 빌드 성공
- [ ] API 통합 테스트 성공

---

## 📝 **체크리스트 사용법**

1. **개발 시작 전**: 1-4번 항목 체크
2. **코드 작성 중**: 2-3번 항목 지속 체크
3. **커밋 전**: 2-5번 항목 체크
4. **CI/CD 실행 후**: 6-11번 항목 체크
5. **배포 전**: 전체 항목 최종 체크

## 🚨 **문제 발생 시 대응**

- **CI/CD 실패**: 로그 분석 → 문제 파악 → 수정 → 재실행
- **코드 품질 실패**: `black`, `isort` 자동 수정 → 재검사
- **테스트 실패**: 테스트 코드 수정 → 재실행
- **Docker 빌드 실패**: Dockerfile 수정 → 재빌드
- **API 테스트 실패**: FastAPI 코드 수정 → 재테스트

---

**마지막 업데이트**: 2025-08-21  
**버전**: 1.0.0  
**작성자**: MLOps Quickstart Team
