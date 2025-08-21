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
└─ .github/workflows/ci.yml   # GitHub Actions CI
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

### 6) DVC 파이프라인 (선택사항)
```bash
dvc init
dvc repro   # dvc.yaml의 파이프라인 실행
```

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

## 🔧 API 엔드포인트

- **GET /health**: API 상태 확인
- **POST /predict**: 모델 예측
- **GET /docs**: Swagger UI
- **GET /redoc**: ReDoc 문서

## 💡 참고사항

- MLflow는 기본적으로 **로컬 파일 기반**으로 기록합니다
- 프로덕션 환경에서는 S3/MinIO + PostgreSQL 구성을 권장합니다
- 모든 서비스는 가상환경에서 실행해야 합니다
