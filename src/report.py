from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def main():
    data = load_iris(as_frame=True)
    df = data.frame
    target = data.target

    train_df, test_df, _, _ = train_test_split(
        df, target, test_size=0.2, random_state=42, stratify=target
    )

    # reports 디렉토리 생성
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # 간단한 데이터 품질 보고서 생성
    print("Creating data quality report...")

    # 기본 통계 정보 출력
    print(f"Training data shape: {train_df.shape}")
    print(f"Test data shape: {test_df.shape}")
    columns_list = list(train_df.columns)
    print("Training data columns:", columns_list)

    # 데이터 품질 기본 정보
    print("\nData Quality Summary:")
    missing_train = train_df.isnull().sum().sum()
    missing_test = test_df.isnull().sum().sum()
    print(f"Missing values in training: {missing_train}")
    print(f"Missing values in test: {missing_test}")
    dtypes_dict = train_df.dtypes.to_dict()
    print(f"Training data types: {dtypes_dict}")

    # 간단한 HTML 보고서 생성
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data Quality Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .section {{
                margin: 20px 0;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            .metric {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>Data Quality Report</h1>

        <div class="section">
            <h2>Dataset Overview</h2>
            <div class="metric">
                <strong>Training data shape:</strong> {train_df.shape}
            </div>
            <div class="metric">
                <strong>Test data shape:</strong> {test_df.shape}
            </div>
            <div class="metric">
                <strong>Features:</strong> {list(train_df.columns)}
            </div>
        </div>

        <div class="section">
            <h2>Data Quality Metrics</h2>
            <div class="metric">
                <strong>Missing values in training:</strong>
                {train_df.isnull().sum().sum()}
            </div>
            <div class="metric">
                <strong>Missing values in test:</strong>
                {test_df.isnull().sum().sum()}
            </div>
        </div>

        <div class="section">
            <h2>Feature Statistics</h2>
            {train_df.describe().to_html()}
        </div>
    </body>
    </html>
    """

    report_path = "reports/data_quality_report.html"
    with open(report_path, "w") as f:
        f.write(html_content)

    print(f"\nSaved simple data quality report to {report_path}")
    print("Open this file in your browser to view the report")


if __name__ == "__main__":
    main()
