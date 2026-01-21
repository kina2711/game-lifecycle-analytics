import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# --- CẤU HÌNH ---
# Đường dẫn đến file JSON Key
KEY_PATH = "../key.json"

# Tên Project và Dataset trên BigQuery
PROJECT_ID = "game-lifecycle-analytics"
DATASET_ID = "game_lifecycle_analytics"

# Đường dẫn chứa file CSV data
DATA_DIR = "../data/raw"

# Mapping: Tên file CSV -> Tên bảng muốn lưu trên BigQuery
FILES_TO_LOAD = {
    "reg_data.csv": "reg_data",
    "auth_data.csv": "auth_data",
    "ab_test.csv": "ab_test"
}

def get_client():
    """Khởi tạo BigQuery Client xác thực bằng Service Account"""
    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(f"Không tìm thấy file Key tại: {KEY_PATH}")

    client = bigquery.Client.from_service_account_json(KEY_PATH)
    return client

def create_dataset_if_not_exists(client):
    """Tạo dataset nếu chưa tồn tại"""
    dataset_ref = f"{client.project}.{DATASET_ID}"
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset '{DATASET_ID}' đã tồn tại.")
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # Hoặc khu vực bạn chọn
        client.create_dataset(dataset)
        print(f"Đã tạo mới Dataset: '{DATASET_ID}'")

def upload_csv_to_bq(client, csv_file, table_name):
    """Đẩy file CSV lên BigQuery"""
    file_path = os.path.join(DATA_DIR, csv_file)

    if not os.path.exists(file_path):
        print(f"Bỏ qua: Không tìm thấy file {file_path}")
        return

    table_id = f"{client.project}.{DATASET_ID}.{table_name}"

    # Cấu hình Job: Tự động detect schema, Ghi đè nếu bảng đã có, Bỏ qua dòng Header
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        field_delimiter=";",
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    print(f"Đang upload '{csv_file}' vào bảng '{table_name}'...")

    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    job.result()

    # Lấy thông tin bảng vừa tạo để confirm
    table = client.get_table(table_id)
    print(f"Thành công! Bảng '{table_name}' hiện có {table.num_rows} dòng.")

def main():
    print("BẮT ĐẦU ETL PIPELINE...")

    try:
        # 1. Kết nối
        client = get_client()

        # 2. Kiểm tra/Tạo Dataset
        create_dataset_if_not_exists(client)

        # 3. Loop qua danh sách file và upload
        for csv_file, table_name in FILES_TO_LOAD.items():
            upload_csv_to_bq(client, csv_file, table_name)

        print("\nETL PIPELINE HOÀN TẤT! Dữ liệu đã sẵn sàng trên BigQuery.")

    except Exception as e:
        print(f"\nLỖI NGHIÊM TRỌNG: {e}")

if __name__ == "__main__":
    main()