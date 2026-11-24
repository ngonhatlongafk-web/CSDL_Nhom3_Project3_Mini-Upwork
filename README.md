# ĐỒ ÁN MÔN HỌC CƠ SỞ DỮ LIỆU (INT1313)
## Đề tài #3: Freelance Marketplace Ecosystem (Mini-Upwork)

### 1. Thông tin chung & Thành viên thực hiện
* **Trường:** Học viện Công nghệ Bưu chính Viễn thông – Cơ sở tại TP. Hồ Chí Minh (PTITHCM)
* **Môn học:** Cơ sở dữ liệu (INT1313)
* **Lớp / Khóa học:** [D24CQCN01,02] – Khóa D24
* **Giảng viên hướng dẫn:** ThS. Lê Hà Thanh (`lehathanh@ptithcm.edu.vn`)
* **Nhóm thực hiện:** Nhóm 3

| STT | Họ và tên sinh viên | Mã số sinh viên | Email sinh viên | Vai trò & Phụ trách chính |

| 1 | **Nguyễn Lê Khải** | `N24DCCN128` | `n24dccn128@student.ptithcm.edu.vn` | Thiết kế EER, ánh xạ lược đồ 11 bảng, chứng minh chuẩn hóa 1NF–BCNF |

| 2 | **Huỳnh Duy Khánh** | `N24DCCN040` | `n24dccn040@student.ptithcm.edu.vn` | Xây dựng DDL/Triggers/Views, phát triển ứng dụng Demo Web (Flask + MySQL) |

| 3 | **Ngô Nhật Long** | `N24DCCN138` | `n24dccn138@student.ptithcm.edu.vn` | Dữ liệu mẫu, truy vấn nâng cao, kiểm thử `EXPLAIN`, Negative Testing & RBAC |

---

### 2. Tổng quan dự án (Project Overview)
**Mini-Upwork** là hệ thống cơ sở dữ liệu mô phỏng sàn giao dịch việc làm tự do trực tuyến, kết nối **Khách hàng (Clients)** và **Người làm tự do (Freelancers)** xuyên suốt vòng đời dự án:
1. Đăng tin tuyển dụng (`Jobs`) & nộp hồ sơ chào giá (`Proposals`).
2. Ký kết hợp đồng (`Contracts`) & phân chia các cột mốc tiến độ (`Milestones`).
3. Nghiệm thu cột mốc (`Approved`) và thanh toán trực tiếp 1–1 theo từng cột mốc (`Payments`, không dùng thực thể ký quỹ trung gian `Escrow`).
4. Đánh giá chéo hai chiều (`Reviews`) và tự động cập nhật điểm uy tín (`Users.AverageRating`) thông qua hệ thống Trigger.

**Thông số kỹ thuật CSDL:**
* **Hệ quản trị CSDL:** MySQL 8.0+ (`InnoDB`, bảng mã `utf8mb4_unicode_ci`)
* **Kiến trúc logic:** 11 bảng quan hệ đạt chuẩn **3NF / BCNF** (kèm 2 điểm phi chuẩn hóa có kiểm soát: `Contracts.ClientID/FreelancerID` và `Users.AverageRating`)
* **Thành phần lập trình CSDL:** 8 Secondary Indexes, 3 Views, 6 Triggers, 4 RBAC Roles (`role_admin`, `role_client`, `role_freelancer`, `role_auditor`)

---

### 3. Cấu trúc thư mục Repository

```text
mini-upwork-database/
├── README.md                          # Tài liệu hướng dẫn tổng quan dự án
├── docs/
│   ├── BaoCao_MiniUpwork_Nhom3.pdf    # Báo cáo chi tiết đồ án (bản PDF hoàn chỉnh)
│   └── schema.dbml                    # Mã nguồn Lược đồ Quan hệ (dbdiagram.io)
├── database/
│   ├── 01_ddl_script.sql              # Khởi tạo DB, 11 bảng, Indexes, Views và 6 Triggers
│   └── 02_queries_tests_rbac.sql      # Dữ liệu mẫu, 5 truy vấn nâng cao, EXPLAIN, 10 Negative Tests & RBAC
└── app/
    └── app.py                         # Ứng dụng Web Demo (Python Flask) kết nối trực tiếp MySQL
