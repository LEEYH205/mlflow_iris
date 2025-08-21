# 🚀 MLOps Quickstart with MLflow

**완벽한 MLOps 파이프라인을 빠르게 구축하고 학습할 수 있는 프로젝트입니다!**

## ✨ **주요 기능**

- 🧪 **MLflow**: 실험 추적 및 모델 관리
- 🚀 **FastAPI**: 고성능 ML 모델 서빙 API
- 🐳 **Docker**: 컨테이너화 및 배포
- 🔄 **CI/CD**: GitHub Actions 자동화
- 🐘 **DVC**: 데이터 및 모델 버전 관리
- 📊 **Prometheus**: 실시간 메트릭 수집
- 📈 **Grafana**: 시각화 및 모니터링 대시보드
- 🧪 **자동화된 테스트**: 단위 테스트, 통합 테스트, 부하 테스트

## 🎯 **프로젝트 상태**

### ✅ **완료된 기능**
- [x] Python 가상환경 및 의존성 관리
- [x] MLflow 실험 추적 시스템
- [x] FastAPI ML 모델 서빙 API
- [x] Docker 컨테이너화
- [x] GitHub Actions CI/CD 파이프라인
- [x] DVC 데이터 및 모델 버전 관리
- [x] 부하 테스트 및 성능 측정
- [x] **Prometheus + Grafana 실시간 모니터링 시스템**

### 🔄 **진행 중인 기능**
- [ ] Grafana 대시보드 구성 (API 성능, ML 예측 통계)
- [ ] 알림 시스템 설정 (성능 저하 시 자동 알림)

### 📋 **계획된 기능**
- [ ] 고급 메트릭 및 비즈니스 KPI
- [ ] 클라우드 배포 (AWS/GCP/Azure)
- [ ] A/B 테스트 프레임워크
- [ ] 모델 성능 자동 모니터링

## 🚀 **빠른 시작**

### **1. 환경 설정**
```bash
# 저장소 클론
git clone https://github.com/LEEYH205/mlflow_iris.git
cd mlflow_iris

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### **2. 모델 훈련 및 실험 추적**
```bash
# 가상환경 활성화
source .venv/bin/activate

# 모델 훈련 및 MLflow 실험 추적
python src/train.py

# MLflow UI 실행
mlflow ui
# 브라우저에서 http://localhost:5000 접속
```

### **3. FastAPI 서버 실행**
```bash
# 가상환경 활성화
source .venv/bin/activate

# FastAPI 서버 실행
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
# 브라우저에서 http://127.0.0.1:8000/docs 접속
```

### **4. Docker Compose로 전체 스택 실행**
```bash
# 모든 서비스 실행 (MLflow, FastAPI, Prometheus, Grafana)
docker compose up -d

# 서비스 상태 확인
docker compose ps

# 서비스 중지
docker compose down
```

### **5. 모니터링 시스템 접속**
| 서비스 | URL | 설명 |
|--------|-----|------|
| **FastAPI** | `http://localhost:8001` | ML 모델 API |
| **MLflow** | `http://localhost:5001` | 실험 관리 |
| **Prometheus** | `http://localhost:9090` | 메트릭 수집 |
| **Grafana** | `http://localhost:3000` | 시각화 대시보드 |

**Grafana 로그인**: `admin` / `admin`

## 📊 **API 사용법**

### **예측 API 호출**
```bash
# 헬스 체크
curl http://localhost:8001/health

# 예측 요청
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'

# 메트릭 확인 (Prometheus 형식)
curl http://localhost:8001/metrics
```

### **Swagger UI**
- 브라우저에서 `http://localhost:8001/docs` 접속
- API 문서 및 테스트 인터페이스 제공

## 🧪 **테스트 및 검증**

### **자동화된 테스트**
```bash
# 가상환경 활성화
source .venv/bin/activate

# 단위 테스트 실행
pytest

# 코드 품질 검사
black .
isort .
flake8 .
```

### **부하 테스트**
```bash
# 가상환경 활성화
source .venv/bin/activate

# 부하 테스트 실행
python load_test.py
```

## 📈 **모니터링 및 관찰성**

### **Prometheus 메트릭**
- **HTTP 요청 메트릭**: 요청 수, 응답 시간, 상태 코드
- **ML 예측 메트릭**: 예측 수, 예측 클래스별 분류, 예측 시간
- **시스템 메트릭**: CPU, 메모리, 프로세스 정보
- **자동 수집**: 5초마다 FastAPI 서버에서 메트릭 수집

### **Grafana 대시보드**
- **API 성능 모니터링**: 요청 처리량, 응답 시간, 에러율
- **ML 모델 성능**: 예측 통계, 클래스별 분포, 성능 트렌드
- **실시간 시각화**: Prometheus 데이터를 활용한 동적 차트

## 🔧 **개발 도구**

### **코드 품질**
- **Black**: Python 코드 포맷터
- **isort**: import 문 정렬
- **Flake8**: 코드 린팅 및 스타일 검사
- **Pre-commit**: Git 커밋 전 자동 코드 품질 검사

### **의존성 관리**
- **requirements.txt**: 핀된 버전으로 안정성 확보
- **Docker**: 일관된 실행 환경
- **DVC**: 대용량 데이터 및 모델 버전 관리

## 🚀 **CI/CD 파이프라인**

### **GitHub Actions 워크플로우**
1. **코드 품질 검사**: Black, isort, Flake8
2. **테스트 실행**: pytest, 단위 테스트
3. **MLflow 테스트**: 모델 훈련 및 로깅 검증
4. **Docker 빌드**: 이미지 빌드 및 검증
5. **통합 테스트**: API 엔드포인트 테스트
6. **결과 요약**: 모든 단계 결과 통합 보고

## 📊 **성능 지표**

### **부하 테스트 결과**
| 부하 수준 | 요청 수 | 동시 사용자 | 성공률 | 처리량 | 평균 응답시간 |
|-----------|---------|-------------|--------|--------|---------------|
| **가벼운** | 50 | 5 | 100% | 64.47 req/s | 76.85 ms |
| **중간** | 200 | 20 | 100% | 55.48 req/s | 351.72 ms |
| **높은** | 500 | 50 | 100% | 58.85 req/s | 825.08 ms |

### **모델 성능**
- **정확도**: 100% (테스트 데이터셋 기준)
- **예측 일관성**: 동일 입력에 대해 100% 일관된 결과
- **응답 시간**: 평균 28ms (단일 요청)

## 🐘 **DVC 데이터 관리**

### **데이터 파이프라인**
```bash
# DVC 초기화
dvc init

# 데이터 및 모델 추가
dvc add artifacts/
dvc add reports/

# 파이프라인 실행
dvc repro

# 원격 저장소에 푸시
dvc push
```

### **버전 관리**
- **artifacts/**: 훈련된 모델 파일
- **reports/**: 데이터 품질 보고서
- **dvc.lock**: 파이프라인 의존성 잠금

## 🔍 **문제 해결**

### **일반적인 문제들**
1. **포트 충돌**: macOS에서 5000번 포트 사용 시 `docker-compose.yml`에서 포트 변경
2. **의존성 충돌**: `requirements.txt`의 핀된 버전 사용
3. **Docker 빌드 실패**: `docker compose up -d --build`로 재빌드

### **로그 확인**
```bash
# 서비스별 로그 확인
docker compose logs api
docker compose logs mlflow
docker compose logs prometheus
docker compose logs grafana
```

## 🌟 **프로젝트 특징**

- **🎯 학습 중심**: MLOps 개념을 실제로 구현하며 학습
- **🔧 실용적**: 프로덕션 환경에서 사용할 수 있는 도구들
- **📊 관찰 가능**: Prometheus + Grafana로 실시간 모니터링
- **🚀 확장 가능**: 클라우드 배포 및 팀 협업 준비
- **🔄 자동화**: CI/CD로 개발부터 배포까지 자동화

## 🤝 **기여하기**

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 **라이선스**

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 **연락처**

프로젝트 링크: [https://github.com/LEEYH205/mlflow_iris](https://github.com/LEEYH205/mlflow_iris)

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요! ⭐**
