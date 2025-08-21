# MLOps Quickstart: MLflow + FastAPI + DVC

🚀 **Iris 꽃 분류 모델**을 활용한 MLOps 파이프라인 템플릿입니다.

**실험 추적(MLflow)**, **모델 서빙(FastAPI)**, **데이터 버전관리(DVC)**를 포함한 완전한 예제로,
로컬 환경에서 바로 실행할 수 있습니다.

## ✨ 주요 기능

- 🧪 **MLflow**: 모델 실험 추적 및 관리
- 🚀 **FastAPI**: 실시간 모델 예측 REST API
- 📊 **Docker**: 컨테이너화된 배포
- 📈 **DVC**: 데이터 및 모델 버전 관리
- 🔧 **CI/CD**: GitHub Actions 자동화

## 구성(Structure)
```
mlops-quickstart-mlflow/
├─ app/
│  └─ main.py                 # FastAPI 추론 서버
├─ src/
│  ├─ train.py                # 학습 + MLflow 로깅
│  └─ report.py               # 데이터 리포트 생성
├─ tests/
│  └─ test_train.py           # 간단 테스트
├─ artifacts/                 # 학습 산출물 (model.pkl 등)
├─ reports/                   # 리포트 출력 (HTML)
├─ dvc.yaml                   # DVC 파이프라인 예시
├─ params.yaml                # 학습 하이퍼파라미터
├─ Dockerfile                 # API 서버용 Dockerfile
├─ docker-compose.yml         # MLflow UI + API 로컬 실행
├─ requirements.txt           # Python 3.12 호환 의존성
├─ .github/workflows/ci.yml   # GitHub Actions CI
├─ artifacts.dvc              # DVC 아티팩트 추적
├─ reports.dvc                # DVC 리포트 추적
├─ .vscode/settings.json      # VS Code 자동 포맷팅 설정
├─ .pre-commit-config.yaml    # Git pre-commit 훅
├─ pyproject.toml            # Python 도구 설정
├─ load_test.py              # 부하 테스트 스크립트
└─ .dvc/                      # DVC 설정 파일
```

## 빠른 시작(Quickstart)

### 0) 환경 준비
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

### 1) 모델 훈련 + MLflow 실험 추적
```bash
python src/train.py
# 🎯 RandomForest 모델 훈련 (정확도: 96.67%)
# ✅ MLflow에 메트릭, 파라미터, 아티팩트 자동 로깅
```

### 2) MLflow UI 실행
```bash
source .venv/bin/activate && mlflow ui
# 🌐 http://127.0.0.1:5000 에서 실험 결과 확인
```

### 3) FastAPI 모델 서빙
```bash
source .venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
# 🚀 http://127.0.0.1:8000/docs 에서 Swagger UI 확인
# 🔍 http://127.0.0.1:8000/health 에서 헬스체크

# 예시 요청
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

### 4) 데이터 리포트 생성
```bash
python src/report.py
# 📊 reports/data_quality_report.html 생성
# 🔍 데이터 통계, 품질 지표, 특성 분석 포함
```

### 5) Docker / Compose
```bash
# API 서버 이미지 빌드
docker build -t mlops-quickstart-api:latest .

# 로컬 통합 실행(MLflow UI + API)
docker compose up
# MLflow: http://localhost:5000
# API:    http://localhost:8000
```

### 6) DVC 데이터 버전 관리 설정
```bash
# DVC 초기화 및 로컬 저장소 설정
dvc init
mkdir -p ~/dvc-storage
dvc remote add local ~/dvc-storage
dvc remote default local

# 데이터 및 모델 파일 DVC 추적
dvc add artifacts/     # 모델 파일들
dvc add reports/       # 리포트 파일들

# Git에 .dvc 파일 추가
git add *.dvc
git commit -m "setup DVC tracking for artifacts and reports"
```

## 🐘 DVC (Data Version Control) 사용법

### DVC란?
**DVC**는 Git과 유사한 방식으로 **데이터와 모델을 버전 관리**하는 도구입니다.

#### 주요 장점
- ✅ **대용량 파일 관리**: 모델, 데이터셋 등
- ✅ **Git 저장소 크기 유지**: 작고 빠름
- ✅ **데이터 파이프라인**: 자동화된 워크플로우
- ✅ **협업**: 팀원들과 데이터 공유

### DVC 명령어
```bash
# 상태 확인
dvc status

# 파일 목록
dvc list .

# 데이터 추가
dvc add 폴더명/

# 데이터 동기화
dvc push    # 로컬 → 원격
dvc pull    # 원격 → 로컬

# 원격 저장소 관리
dvc remote list
dvc remote add myremote s3://mybucket/dvc
```

### 현재 DVC 구조
```
프로젝트/
├── artifacts.dvc          # 모델 파일들 추적
├── reports.dvc            # 리포트 파일들 추적
├── .dvc/                  # DVC 설정
└── ~/dvc-storage/        # 로컬 데이터 저장소
```

### DVC 원격 저장소 옵션
1. **로컬 폴더** (현재 설정): `~/dvc-storage`
2. **GitHub**: Git LFS 사용
3. **클라우드**: AWS S3, Google Cloud, Azure 등

## 🎯 모델 성능 결과

- **모델**: RandomForest Classifier
- **정확도**: 96.67%
- **특성**: Iris 꽃의 꽃받침/꽃잎 길이/너비 (4개)
- **클래스**: setosa, versicolor, virginica (3개)

## 📁 생성되는 파일들

- `artifacts/model.pkl`: 훈련된 모델 파일
- `artifacts/classification_report.csv`: 성능 보고서
- `artifacts/confusion_matrix.csv`: 혼동 행렬
- `reports/data_quality_report.html`: 데이터 품질 보고서
- `mlruns/`: MLflow 실험 기록
- `artifacts.dvc`: DVC 아티팩트 추적 파일
- `reports.dvc`: DVC 리포트 추적 파일

## 🔧 API 엔드포인트

- **GET /health**: API 상태 확인
- **POST /predict**: 모델 예측
- **GET /docs**: Swagger UI
- **GET /redoc**: ReDoc 문서

## 🚀 CI/CD 파이프라인

**GitHub Actions를 통한 자동화된 CI/CD 파이프라인이 포함되어 있습니다:**

### ✅ **모든 테스트 통과!** (총 소요시간: ~2분)

- **🔍 code-quality**: flake8, black, isort
- **🧪 test**: pytest, 코드 커버리지
- **🧪 mlflow-test**: 모델 훈련, 아티팩트 검증
- **🐳 docker-build**: 이미지 빌드 및 기본 테스트
- **🚀 integration-test**: FastAPI 서버 시작 및 API 테스트
- **📊 summary**: CI/CD 파이프라인 결과 요약

### CI/CD 워크플로우 특징
- **자동 트리거**: main/develop 브랜치 푸시 시 자동 실행
- **의존성 체인**: 순차적 실행으로 안정성 보장
- **상태 확인**: 각 단계별 성공/실패 명확히 표시
- **결과 요약**: 전체 파이프라인 상태 한눈에 확인

## 🧪 부하 테스트 (Load Testing)

**FastAPI 서버의 성능과 안정성을 검증하는 부하 테스트가 포함되어 있습니다:**

### 📊 **부하 테스트 결과 요약**

| 테스트 시나리오 | 요청 수 | 동시 사용자 | 성공률 | 처리량 | 평균 응답시간 |
|----------------|---------|-------------|--------|--------|---------------|
| **가벼운 부하** | 50 | 5 | 100% | 41.1 req/s | 120.1 ms |
| **중간 부하** | 200 | 20 | 100% | 68.9 req/s | 285.1 ms |
| **높은 부하** | 500 | 50 | 100% | 60.2 req/s | 804.4 ms |

### 🎯 **성능 특성**

- ✅ **100% 성공률**: 모든 부하 레벨에서 에러 없음
- 🚀 **최적 부하**: 20 동시 사용자 (68.9 req/s)
- ⚡ **응답시간**: 가벼운 부하에서 120ms, 높은 부하에서 800ms
- 💾 **메모리 효율성**: 테스트 중 메모리 사용량 안정적

### 🔧 **부하 테스트 실행**

```bash
# 부하 테스트 스크립트 실행
python load_test.py

# 또는 Docker 환경에서
docker compose up -d
python load_test.py
```

### 📈 **테스트 시나리오**

1. **가벼운 부하**: 50 요청, 5 동시 사용자
2. **중간 부하**: 200 요청, 20 동시 사용자  
3. **높은 부하**: 500 요청, 50 동시 사용자

각 시나리오는 **응답시간**, **처리량**, **에러율**, **메모리 사용량**을 측정합니다.

## 🛠️ 개발 환경 설정

### 자동 코드 포맷팅
프로젝트에는 VS Code와 pre-commit 훅을 통한 자동 코드 포맷팅이 설정되어 있습니다:

```bash
# pre-commit 훅 설치
pre-commit install

# 모든 파일에 대해 포맷팅 실행
pre-commit run --all-files
```

### VS Code 설정
`.vscode/settings.json`에 다음 설정이 포함되어 있습니다:
- **Black**: Python 코드 포맷터
- **isort**: import 문 정렬
- **자동 저장 시 포맷팅**: `formatOnSave: true`

## 💡 참고사항

- **Python 3.12.10** 호환성 확인됨 ✅
- MLflow는 기본적으로 **로컬 파일 기반**으로 기록합니다
- 프로덕션 환경에서는 S3/MinIO + PostgreSQL 구성을 권장합니다
- 모든 서비스는 가상환경에서 실행해야 합니다
- DVC는 대용량 파일을 Git과 별도로 관리하여 저장소 크기를 유지합니다
- 로컬 DVC 저장소는 `~/dvc-storage`에 설정되어 있습니다
- **의존성 충돌 해결**: requirements.txt에서 호환성 문제가 있는 패키지 제거 ✅
- **Docker 호환성**: MockModel을 통한 CI/CD 환경 지원 ✅
- **CI/CD 파이프라인**: 모든 단계 성공적으로 완료 ✅

## 🔄 최근 업데이트

- ✅ **의존성 충돌 해결**: Python 3.12 호환성 확보
- ✅ **Docker MockModel 버그 수정**: CI/CD 환경에서 정상 동작
- ✅ **자동 코드 포맷팅**: Black, isort, flake8 통합
- ✅ **pre-commit 훅**: Git 커밋 전 자동 검사
- ✅ **VS Code 설정**: 개발 환경 최적화
- ✅ **CI/CD 파이프라인 완성**: 모든 작업 성공적으로 완료
- ✅ **evidently 제거**: 의존성 충돌 해결로 CI/CD 오류 방지
- ✅ **코드 품질 검사**: 모든 linting 이슈 해결
- ✅ **부하 테스트 완성**: 성능 및 안정성 검증 완료

## 🎯 프로젝트 상태

### **현재 상태: 모든 핵심 기능 완성!** 🎉

- ✅ **로컬 환경**: 가상환경, 의존성 설치, 모든 기능 테스트 통과
- ✅ **MLflow**: 모델 훈련, 실험 추적, 아티팩트 관리
- ✅ **FastAPI**: REST API 서버, 예측 엔드포인트, 헬스체크
- ✅ **Docker**: 이미지 빌드, 컨테이너 실행, CI/CD 환경 지원
- ✅ **DVC**: 데이터 버전 관리, 로컬 저장소 설정
- ✅ **CI/CD**: GitHub Actions 파이프라인, 모든 단계 성공
- ✅ **코드 품질**: 자동 포맷팅, linting 검사, pre-commit 훅
- ✅ **부하 테스트**: 성능 및 안정성 검증 완료

### **다음 단계 옵션:**
1. 🚀 **프로덕션 배포**: 클라우드 환경 배포
2. 📊 **모니터링 추가**: 로깅, 메트릭, 알림 시스템
3. 🔧 **성능 최적화**: 응답시간 개선 및 확장성 향상
4. ☁️ **클라우드 서비스**: AWS/GCP/Azure 배포
