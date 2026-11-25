# ĐỒ ÁN MÔN HỌC CƠ SỞ DỮ LIỆU (INT1313)

## Đề tài #3: Freelance Marketplace Ecosystem (Mini-Upwork)

### 1. Thông tin chung & Thành viên thực hiện

* **Đơn vị đào tạo:** Học viện Công nghệ Bưu chính Viễn thông – Cơ sở tại TP. Hồ Chí Minh (PTITHCM)
* **Môn học:** Cơ sở dữ liệu (`INT1313`)
* **Lớp / Khóa học:** D24CQCN01, D24CQCN02 – Khóa D24
* **Giảng viên hướng dẫn:** ThS. Lê Hà Thanh (`lehathanh@ptithcm.edu.vn`)
* **Nhóm thực hiện:** Nhóm 3 (Bơ vơ)
* **Liên kết Repository:https://github.com/ngonhatlongafk-web/CSDL_Nhom3_Project3_Mini-Upwork/tree/database

| STT | Họ và tên sinh viên | Mã số sinh viên | Email sinh viên | Vai trò & Phụ trách chính |
| :-: | :--- | :---: | :--- | :--- |
| 1 | **Nguyễn Lê Khải** | `N24DCCN128` | `n24dccn128@student.ptithcm.edu.vn` | Thiết kế mô hình EER, ánh xạ lược đồ 11 bảng, chứng minh chuẩn hóa 1NF–BCNF |
| 2 | **Huỳnh Duy Khánh** | `N24DCCN040` | `n24dccn040@student.ptithcm.edu.vn` | Xây dựng mã nguồn DDL/Triggers/Views, phát triển ứng dụng Demo Web (Flask + MySQL) |
| 3 | **Ngô Nhật Long** | `N24DCCN138` | `ngonhatlongafk@gmail.com` | Xây dựng tập dữ liệu mẫu, 5 truy vấn nâng cao, kiểm thử `EXPLAIN`, Negative Testing & RBAC |

---

### 2. Tổng quan dự án (Project Overview)

**Mini-Upwork** là hệ thống cơ sở dữ liệu mô phỏng sàn giao dịch việc làm tự do trực tuyến, kết nối **Khách hàng (Clients)** và **Người làm tự do (Freelancers)** xuyên suốt vòng đời dự án:

1. **Đăng tuyển & Đấu thầu:** Khách hàng đăng tin tuyển dụng (`Jobs`) và Freelancer nộp hồ sơ chào giá (`Proposals`).
2. **Xác lập Hợp đồng & Tiến độ:** Chuyển đổi đề xuất được chấp nhận thành hợp đồng chính thức (`Contracts`) và phân chia thành các cột mốc tiến độ (`Milestones`).
3. **Nghiệm thu & Thanh toán 1–1:** Nghiệm thu từng cột mốc (`Approved`) và ghi nhận thanh toán trực tiếp theo quan hệ 1–1 trong bảng `Payments` (không sử dụng thực thể ký quỹ trung gian `Escrow`).
4. **Đánh giá uy tín tự động:** Thực hiện đánh giá hai chiều sau khi hoàn tất hợp đồng (`Reviews`) và tự động tính toán lại điểm trung bình (`Users.AverageRating`) thông qua hệ thống Trigger.

#### Thông số kỹ thuật Cơ sở dữ liệu

* **Hệ quản trị CSDL:** MySQL 8.0+ (Storage Engine: `InnoDB`, Character Set: `utf8mb4`, Collation: `utf8mb4_unicode_ci`)
* **Kiến trúc lược đồ:** 11 bảng quan hệ đạt chuẩn **3NF / BCNF** (kèm 2 điểm phi chuẩn hóa có kiểm soát: `Contracts.ClientID/FreelancerID` để bảo toàn lịch sử pháp lý và `Users.AverageRating` để tối ưu hiệu năng đọc)
* **Đối tượng lập trình & Tối ưu:**
  * **8 Secondary Indexes:** Tối ưu lọc việc làm theo ngân sách/trạng thái, tiến độ cột mốc, báo cáo thanh toán và xếp hạng đánh giá.
  * **3 Business Views:** `vw_active_jobs_summary`, `vw_contract_payment_progress`, `vw_freelancer_profiles`.
  * **6 Triggers:** 3 Trigger tự động cập nhật `Users.AverageRating` (`INSERT`/`UPDATE`/`DELETE` trên `Reviews`) và 3 Trigger kiểm tra toàn vẹn nghiệp vụ (`BR-05`, `BR-06`/`BR-07`, `BR-09`).
  * **4 RBAC Roles:** `role_admin`, `role_client`, `role_freelancer`, `role_auditor` tuân thủ nguyên tắc đặc quyền tối thiểu.

---

### 3. Cấu trúc thư mục, Tài liệu & Tập dữ liệu


```text
mini-upwork-database/
├── README.md                          # Tài liệu tổng quan dự án và hướng dẫn cài đặt, vận hành
├── docs/
│   ├── BaoCao_MiniUpwork_Nhom3.pdf    # Báo cáo chi tiết thiết kế & triển khai CSDL (PDF)
│   └── schema.dbml                    # Mã nguồn Lược đồ Quan hệ chuẩn DBML (dbdiagram.io)
├── database/
│   ├── 01_ddl_script.sql              # Kịch bản DDL khởi tạo CSDL, 11 bảng, Indexes, Views & Triggers
│   └── 02_queries_tests_rbac.sql      # Tập dữ liệu mẫu (DML), 5 truy vấn nâng cao, EXPLAIN, 10 Negative Tests & RBAC
└── app/
    └── app.py                         # Ứng dụng Web Demo (Python Flask) kết nối trực tiếp MySQL
```

* **Tập dữ liệu mẫu (Mock Dataset):** Được tích hợp sẵn tại **SECTION 1** của tệp `database/02_queries_tests_rbac.sql`, bao gồm dữ liệu khởi tạo đầy đủ cho cả 11 bảng (7 người dùng thuộc 3 vai trò, 6 kỹ năng, 4 công việc, 6 đề xuất, 3 hợp đồng, 7 cột mốc tiến độ, 5 giao dịch thanh toán và 4 đánh giá chéo).

---

### 4. Hướng dẫn cài đặt, triển khai và vận hành

#### 4.1 Yêu cầu môi trường

* **MySQL Server 8.0+** và **MySQL Workbench** (hoặc MySQL CLI)
* **Python 3.10+** (khuyến nghị Python 3.11+) cùng trình quản lý gói `pip`
* Trình duyệt web hiện đại (Chrome, Edge, Firefox)

#### 4.2 Triển khai Cơ sở dữ liệu (MySQL)

1. Khởi động dịch vụ **MySQL80** và mở **MySQL Workbench**, kết nối vào máy chủ cục bộ (`localhost`, cổng `3306`).
2. Mở tệp `database/01_ddl_script.sql` và chạy toàn bộ kịch bản (`Ctrl + Shift + Enter`) để:
   * Khởi tạo database `mini_upwork` và 11 bảng quan hệ.
   * Thiết lập 8 chỉ mục phụ, 3 khung nhìn (`Views`) và 6 bộ kích hoạt (`Triggers`).
3. Mở tệp `database/02_queries_tests_rbac.sql` và thực thi lần lượt các phần:
   * **SECTION 1 (DML):** Nạp tập dữ liệu mẫu cho toàn bộ 11 bảng và kiểm tra tự động tính điểm `AverageRating`.
   * **SECTION 2 & 3 (Queries & Performance):** Thực thi 5 câu truy vấn phân tích nâng cao (`JOIN`, `GROUP BY/HAVING`, `CTE`, `Window Functions`) và 3 lệnh `EXPLAIN` kiểm tra chỉ mục.
   * **SECTION 5 (RBAC):** Khởi tạo 4 vai trò (`role_admin`, `role_client`, `role_freelancer`, `role_auditor`), cấp/thu hồi quyền (`GRANT`/`REVOKE`) và tạo 4 tài khoản người dùng tương ứng (`mu_admin`, `mu_client`, `mu_freelancer`, `mu_auditor`).
   * *(Tùy chọn kiểm thử)* **SECTION 4 (Negative Testing):** Bôi đen và chạy từng lệnh `TC-01` đến `TC-10` để kiểm chứng cơ chế chặn dữ liệu vi phạm ràng buộc của MySQL (`Error 3819`, `1062`, `1644`, `1451`).

#### 4.3 Vận hành ứng dụng Web Demo (Python Flask)

1. Mở tệp `app/app.py` và cấu hình thông tin kết nối MySQL cục bộ trong biến `DB_CONFIG` (thay đổi mật khẩu tương ứng với máy chủ của bạn):
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "root",
       "password": "YOUR_MYSQL_PASSWORD",
       "database": "mini_upwork",
   }
   ```
2. Mở Terminal / PowerShell tại thư mục gốc của dự án và cài đặt các thư viện cần thiết:
   ```bash
   pip install flask mysql-connector-python
   ```
3. Khởi chạy máy chủ web demo:
   ```bash
   python app/app.py
   ```
4. **Xác minh vận hành:** Mở trình duyệt và truy cập địa chỉ **`http://127.0.0.1:5000`**. Hệ thống hoạt động thành công khi giao diện hiển thị đầy đủ 3 phân khu dữ liệu từ CSDL:
   * Danh sách công việc đang mở (`vw_active_jobs_summary`), chức năng đăng việc mới và nộp báo giá (`Proposals`).
   * Tiến độ thanh toán hợp đồng (`vw_contract_payment_progress`), nghiệm thu cột mốc (`Approve`) và thanh toán trực tiếp 1–1 (`Payments`).
   * Bảng xếp hạng kỹ năng và điểm đánh giá trung bình tự động (`vw_freelancer_profiles`).

---

### 5. Ghi chú nộp bài & Phân quyền Repository

* **Phân quyền Giảng viên:** Repository đã được thêm thành viên (Collaborator) với địa chỉ email giảng viên hướng dẫn: **`lehathanh@ptithcm.edu.vn`**.
* **Tài liệu báo cáo:** Bản báo cáo chi tiết định dạng **PDF** được lưu trữ tại `docs/BaoCao_MiniUpwork_Nhom3.pdf` trong repository và đồng thời được nộp riêng theo biểu mẫu quy định của môn học.
