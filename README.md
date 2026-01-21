# game-lifecycle-analytics
Gamelytics-Mobile-Growth/
│
├── data/                   # (Tùy chọn) Chứa file CSV mẫu nếu data nhỏ. 
│   ├── raw/                # Dữ liệu gốc tải từ Kaggle
│   └── processed/          # Dữ liệu đã sạch (nếu xử lý local)
│
├── sql/                    # Chứa các file câu lệnh SQL
│   ├── 01_cleaning.sql     # Làm sạch, đổi timestamp
│   ├── 02_retention.sql    # Logic tính Retention
│   └── 03_monetization.sql # Logic tính doanh thu/A-B Test
│
├── src/                    # Source code Python (nếu tách hàm)
│   └── data_loader.py      # Script đẩy data lên BigQuery (nếu cần)
│
├── app.py                  # File chính chạy Streamlit
├── requirements.txt        # Danh sách thư viện (pandas, streamlit, google-cloud-bigquery...)
├── .gitignore              # Quan trọng: Loại bỏ file hệ thống và file cấu hình mật khẩu
└── README.md               # "Bộ mặt" của dự án (Giới thiệu, Hướng dẫn chạy, Insight chính)