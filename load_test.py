#!/usr/bin/env python3
"""
부하 테스트 스크립트
- 동시 요청 처리 테스트
- 응답 시간 측정
- 에러율 계산
- 메모리 사용량 모니터링
"""

import os
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

import psutil
import requests


class LoadTester:
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.results = []
        self.errors = []
        self.start_time = None
        self.end_time = None

    def make_request(self, request_id: int) -> Dict:
        """단일 요청 실행"""
        start_time = time.time()

        try:
            # 다양한 테스트 데이터
            test_data = [
                {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                },
                {
                    "sepal_length": 6.3,
                    "sepal_width": 3.3,
                    "petal_length": 4.7,
                    "petal_width": 1.6,
                },
                {
                    "sepal_length": 7.7,
                    "sepal_width": 2.6,
                    "petal_length": 6.9,
                    "petal_width": 2.3,
                },
                {
                    "sepal_length": 4.9,
                    "sepal_width": 3.0,
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                },
                {
                    "sepal_length": 6.7,
                    "sepal_width": 3.1,
                    "petal_length": 4.4,
                    "petal_width": 1.4,
                },
            ]

            # 랜덤하게 테스트 데이터 선택
            import random

            data = random.choice(test_data)

            response = requests.post(f"{self.base_url}/predict", json=data, timeout=10)

            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # ms로 변환

            if response.status_code == 200:
                return {
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "success": True,
                    "data": data,
                }
            else:
                return {
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                }

        except requests.exceptions.RequestException as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return {
                "request_id": request_id,
                "status_code": None,
                "response_time": response_time,
                "success": False,
                "error": str(e),
            }

    def run_load_test(self, num_requests: int, concurrent_users: int) -> Dict:
        """부하 테스트 실행"""
        print(
            f"START 부하 테스트 시작: {num_requests}개 요청, {concurrent_users}개 동시 사용자"
        )
        print(f"INFO 테스트 대상: {self.base_url}")
        print("-" * 50)

        self.start_time = time.time()
        self.results = []
        self.errors = []

        # ThreadPoolExecutor로 동시 요청 실행
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # 모든 요청 제출
            future_to_request = {
                executor.submit(self.make_request, i): i for i in range(num_requests)
            }

            # 결과 수집
            completed = 0
            for future in as_completed(future_to_request):
                result = future.result()
                self.results.append(result)

                if not result["success"]:
                    self.errors.append(result)

                completed += 1
                if completed % 10 == 0:
                    progress = completed / num_requests * 100
                    print(f"진행률: {completed}/{num_requests} ({progress:.1f}%)")

        self.end_time = time.time()
        return self.analyze_results()

    def analyze_results(self) -> Dict:
        """결과 분석"""
        if not self.results:
            return {"error": "결과가 없습니다"}

        total_requests = len(self.results)
        successful_requests = len([r for r in self.results if r["success"]])
        failed_requests = len(self.errors)

        # 응답 시간 통계
        response_times = [r["response_time"] for r in self.results if r["success"]]

        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            if len(response_times) >= 20:
                p95_response_time = statistics.quantiles(response_times, n=20)[18]
            else:
                p95_response_time = max_response_time
        else:
            avg_response_time = median_response_time = min_response_time = (
                max_response_time
            ) = p95_response_time = 0

        # 처리량 계산
        total_time = self.end_time - self.start_time
        requests_per_second = total_requests / total_time if total_time > 0 else 0

        # 성공률 계산
        success_rate = (
            (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        )

        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": success_rate,
            "total_time": total_time,
            "requests_per_second": requests_per_second,
            "response_times": {
                "average": avg_response_time,
                "median": median_response_time,
                "min": min_response_time,
                "max": max_response_time,
                "p95": p95_response_time,
            },
            "errors": self.errors[:10],  # 처음 10개 에러만 표시
        }

    def print_results(self, results: Dict):
        """결과 출력"""
        print("\n" + "=" * 60)
        print("INFO 부하 테스트 결과")
        print("=" * 60)

        print(f"총 요청 수: {results['total_requests']:,}")
        print(f"성공 요청: {results['successful_requests']:,}")
        print(f"실패 요청: {results['failed_requests']:,}")
        print(f"성공률: {results['success_rate']:.2f}%")
        print(f"총 소요 시간: {results['total_time']:.2f}초")
        print(f"초당 처리량: {results['requests_per_second']:.2f} req/s")

        print("\nTIME 응답 시간 통계 (ms):")
        rt = results["response_times"]
        print(f"  평균: {rt['average']:.2f}")
        print(f"  중간값: {rt['median']:.2f}")
        print(f"  최소: {rt['min']:.2f}")
        print(f"  최대: {rt['max']:.2f}")
        print(f"  95%ile: {rt['p95']:.2f}")

        if results["errors"]:
            print("\nERROR 에러 요약 (처음 10개):")
            for error in results["errors"]:
                print(
                    f"  요청 {error['request_id']}: {error.get('error', 'Unknown error')}"
                )

        print("=" * 60)


def get_memory_usage():
    """메모리 사용량 확인"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return {
        "rss": memory_info.rss / 1024 / 1024,  # MB
        "vms": memory_info.vms / 1024 / 1024,  # MB
    }


def main():
    """메인 함수"""
    print("🧪 MLOps 파이프라인 부하 테스트")
    print("=" * 50)

    # 메모리 사용량 확인
    try:
        initial_memory = get_memory_usage()
        print(f"초기 메모리 사용량: {initial_memory['rss']:.2f} MB (RSS)")
    except ImportError:
        print("psutil이 설치되지 않았습니다. 메모리 모니터링을 건너뜁니다.")
        initial_memory = None

    # 부하 테스트 실행
    tester = LoadTester()

    # 테스트 시나리오들
    test_scenarios = [
        {"name": "가벼운 부하", "requests": 50, "concurrent": 5},
        {"name": "중간 부하", "requests": 200, "concurrent": 20},
        {"name": "높은 부하", "requests": 500, "concurrent": 50},
    ]

    all_results = {}

    for scenario in test_scenarios:
        print(f"\nTARGET {scenario['name']} 테스트 시작")
        print(
            f"   요청 수: {scenario['requests']}, 동시 사용자: {scenario['concurrent']}"
        )

        results = tester.run_load_test(scenario["requests"], scenario["concurrent"])
        tester.print_results(results)
        all_results[scenario["name"]] = results

        # 테스트 간 간격
        if scenario != test_scenarios[-1]:
            print("\nWAIT 다음 테스트까지 5초 대기...")
            time.sleep(5)

    # 최종 요약
    print("\n" + "=" * 20)
    print("최종 테스트 요약")
    print("=" * 20)

    for name, results in all_results.items():
        print(f"\n{name}:")
        print(f"  성공률: {results['success_rate']:.1f}%")
        print(f"  처리량: {results['requests_per_second']:.1f} req/s")
        print(f"  평균 응답시간: {results['response_times']['average']:.1f} ms")

    # 메모리 사용량 변화 확인
    if initial_memory:
        try:
            final_memory = get_memory_usage()
            memory_diff = final_memory["rss"] - initial_memory["rss"]
            print(f"\nMEMORY 메모리 사용량 변화: {memory_diff:+.2f} MB")
        except Exception:
            pass

    print("\nCOMPLETE 부하 테스트 완료!")


if __name__ == "__main__":
    main()
