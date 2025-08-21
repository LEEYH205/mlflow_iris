# MLOps Quickstart: MLflow + FastAPI + DVC + Evidently

🚀 **Iris 꽃 분류 모델**을 활용한 MLOps 파이프라인 템플릿입니다.

**실험 추적(MLflow)**, **모델 서빙(FastAPI)**, **데이터 버전관리(DVC)**, **데이터 품질 모니터링(Evidently)**를 포함한 완전한 예제로,
로컬 환경에서 바로 실행할 수 있습니다.

## ✨ 주요 기능

- 🧪 **MLflow**: 모델 실험 추적 및 관리
- 🚀 **FastAPI**: 실시간 모델 예측 REST API
- 📊 **Evidently**: 데이터 품질 및 드리프트 모니터링
- 🐳 **Docker**: 컨테이너화된 배포
- 📈 **DVC**: 데이터 및 모델 버전 관리

## 구성(Structure)
```
mlops-quickstart-mlflow/
├─ app/
│  └─ main.py                 # FastAPI 추론 서버
├─ src/
│  ├─ train.py                # 학습 + MLflow 로깅
│  └─ report.py               # Evidently 데이터/성능 리포트
├─ tests/
│  └─ test_train.py           # 간단 테스트
├─ artifacts/                 # 학습 산출물 (model.pkl 등)
├─ reports/                   # 리포트 출력 (HTML)
├─ dvc.yaml                   # DVC 파이프라인 예시
├─ params.yaml                # 학습 하이퍼파라미터
├─ Dockerfile                 # API 서버용 Dockerfile
├─ docker-compose.yml         # MLflow UI + API 로컬 실행
├─ requirements.txt
├─ .github/workflows/ci.yml   # GitHub Actions CI
├─ artifacts.dvc              # DVC 아티팩트 추적
├─ reports.dvc                # DVC 리포트 추적
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

### 4) 데이터 품질 리포트 생성
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

GitHub Actions를 통한 자동화된 CI/CD 파이프라인이 포함되어 있습니다:

- **코드 품질**: flake8, black, isort, bandit, safety
- **테스트**: pytest, 코드 커버리지
- **MLflow 테스트**: 모델 훈련, 아티팩트 검증
- **Docker 빌드**: 이미지 빌드 및 기본 테스트
- **통합 테스트**: FastAPI 서버 시작 및 API 테스트

## 💡 참고사항

- MLflow는 기본적으로 **로컬 파일 기반**으로 기록합니다
- 프로덕션 환경에서는 S3/MinIO + PostgreSQL 구성을 권장합니다
- 모든 서비스는 가상환경에서 실행해야 합니다
- DVC는 대용량 파일을 Git과 별도로 관리하여 저장소 크기를 유지합니다
- 로컬 DVC 저장소는 `~/dvc-storage`에 설정되어 있습니다
