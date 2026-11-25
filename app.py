from flask import Flask, request, redirect, url_for, render_template_string, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "mini_upwork_phase4_v2_secret_key"

# Cấu hình kết nối MySQL 8.0+ tới CSDL mini_upwork
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "acces123@123",  # <-- Điền mật khẩu MySQL của bạn tại đây
    "database": "mini_upwork",
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini-Upwork — Phase 4 Demo Workspace</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; }
        .card { border: none; border-radius: 12px; }
        .stat-card { border-radius: 12px; background: #fff; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .nav-pills .nav-link.active { background-color: #0d6efd; font-weight: 600; }
        .table thead th { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.03em; }
    </style>
</head>
<body>
<nav class="navbar navbar-dark bg-dark py-3 mb-4 shadow-sm">
    <div class="container d-flex flex-wrap justify-content-between align-items-center gap-2">
        <div>
            <span class="navbar-brand fw-bold mb-0">Mini-Upwork Ecosystem</span>
            <span class="badge bg-primary ms-2">Phase 4 Demo v2</span>
        </div>
        <div class="d-flex align-items-center gap-2">
            <span class="text-light small me-2">INT1313 | Nhóm 3 (Khải – Khánh – Long)</span>
            <div class="btn-group btn-group-sm" role="group">
                {% for r in ['All', 'Client', 'Freelancer', 'Auditor'] %}
                    <a href="{{ url_for('index', tab=active_tab, role=r, q=search_q, min_budget=min_budget) }}"
                       class="btn {{ 'btn-warning text-dark fw-semibold' if role_view == r else 'btn-outline-light' }}">
                        {{ r }}
                    </a>
                {% endfor %}
            </div>
        </div>
    </div>
</nav>

<div class="container pb-5">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, msg in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show shadow-sm" role="alert">
            {{ msg }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <!-- KPI SUMMARY -->
    <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
            <div class="stat-card">
                <div class="text-muted small">Job đang mở (View 1)</div>
                <div class="fs-4 fw-bold text-primary">{{ stats.open_jobs }}</div>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="stat-card">
                <div class="text-muted small">Tổng hợp đồng</div>
                <div class="fs-4 fw-bold text-dark">{{ stats.total_contracts }}</div>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="stat-card">
                <div class="text-muted small">Đã thanh toán (Completed)</div>
                <div class="fs-4 fw-bold text-success">${{ "%.2f"|format(stats.total_paid or 0) }}</div>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="stat-card">
                <div class="text-muted small">Freelancer hoạt động</div>
                <div class="fs-4 fw-bold text-info">{{ stats.total_freelancers }}</div>
            </div>
        </div>
    </div>

    {% if role_view == 'Auditor' %}
        <div class="alert alert-info shadow-sm">
            <strong>Chế độ xem Auditor:</strong> Chỉ tập trung theo dõi tiến độ hợp đồng, cột mốc, thanh toán và hồ sơ đánh giá (tương ứng quyền đọc <code>SELECT</code> trên các bảng tài chính và View).
        </div>
    {% endif %}

    <!-- NAVIGATION TABS -->
    <ul class="nav nav-pills mb-4 bg-white p-2 rounded-3 shadow-sm gap-2">
        <li class="nav-item">
            <button class="nav-link {{ 'active' if active_tab == 'jobs' else '' }}" data-bs-toggle="pill" data-bs-target="#tab-jobs" type="button">
                1. Jobs &amp; Proposals
            </button>
        </li>
        <li class="nav-item">
            <button class="nav-link {{ 'active' if active_tab == 'contracts' else '' }}" data-bs-toggle="pill" data-bs-target="#tab-contracts" type="button">
                2. Contracts, Milestones &amp; Payments
            </button>
        </li>
        <li class="nav-item">
            <button class="nav-link {{ 'active' if active_tab == 'freelancers' else '' }}" data-bs-toggle="pill" data-bs-target="#tab-freelancers" type="button">
                3. Freelancers, Skills &amp; Reviews
            </button>
        </li>
    </ul>

    <div class="tab-content">
        <!-- TAB 1: JOBS & PROPOSALS -->
        <div class="tab-pane fade {{ 'show active' if active_tab == 'jobs' else '' }}" id="tab-jobs">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-primary text-white fw-bold d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <span>Công việc đang mở (View: vw_active_jobs_summary)</span>
                    <form method="GET" action="{{ url_for('index') }}" class="d-flex gap-2">
                        <input type="hidden" name="tab" value="jobs">
                        <input type="hidden" name="role" value="{{ role_view }}">
                        <input type="text" name="q" value="{{ search_q }}" class="form-control form-control-sm" placeholder="Tìm tiêu đề / Client...">
                        <input type="number" step="50" name="min_budget" value="{{ min_budget }}" class="form-control form-control-sm" style="width: 140px;" placeholder="Budget >= $">
                        <button type="submit" class="btn btn-light btn-sm fw-semibold">Lọc</button>
                    </form>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>JobID</th>
                                    <th>Tiêu đề</th>
                                    <th>Client / Công ty</th>
                                    <th>Ngân sách</th>
                                    <th>Deadline</th>
                                    <th>Proposals</th>
                                </tr>
                            </thead>
                            <tbody>
                            {% for j in jobs %}
                                <tr>
                                    <td><strong>#{{ j.JobID }}</strong></td>
                                    <td>{{ j.JobTitle }}</td>
                                    <td>{{ j.ClientName }} <span class="text-muted">({{ j.CompanyName or 'N/A' }})</span></td>
                                    <td class="text-success fw-bold">${{ "%.2f"|format(j.Budget) }}</td>
                                    <td>{{ j.Deadline or 'Không giới hạn' }}</td>
                                    <td><span class="badge bg-primary">{{ j.TotalProposals }}</span></td>
                                </tr>
                            {% else %}
                                <tr><td colspan="6" class="text-center text-muted py-3">Không có công việc phù hợp bộ lọc.</td></tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </div>

                    {% if role_view in ['All', 'Freelancer'] %}
                    <hr>
                    <h6 class="fw-bold">Nộp Proposal mới (Kiểm tra FK &amp; UNIQUE (JobID, FreelancerID) - BR-03)</h6>
                    <form method="POST" action="/proposals/create" class="row g-2">
                        <input type="hidden" name="tab" value="jobs">
                        <div class="col-md-3">
                            <select name="job_id" class="form-select" required>
                                <option value="">-- Chọn Job (Open) --</option>
                                {% for j in jobs %}
                                    <option value="{{ j.JobID }}">#{{ j.JobID }} - {{ j.JobTitle }} (${{ "%.0f"|format(j.Budget) }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-3">
                            <select name="freelancer_id" class="form-select" required>
                                <option value="">-- Chọn Freelancer --</option>
                                {% for f in freelancers %}
                                    <option value="{{ f.FreelancerID }}">#{{ f.FreelancerID }} - {{ f.FullName }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-2">
                            <input type="number" step="0.01" name="bid_amount" class="form-control" placeholder="Bid ($)" required>
                        </div>
                        <div class="col-md-2">
                            <input type="text" name="delivery_time" class="form-control" placeholder="VD: 10 days" required>
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-primary w-100">Gửi Proposal</button>
                        </div>
                    </form>
                    {% endif %}

                    {% if role_view in ['All', 'Client'] %}
                    <hr>
                    <h6 class="fw-bold">Đăng Job mới (Client tạo Job)</h6>
                    <form method="POST" action="/jobs/create" class="row g-2">
                        <input type="hidden" name="tab" value="jobs">
                        <div class="col-md-3">
                            <select name="client_id" class="form-select" required>
                                <option value="">-- Chọn Client --</option>
                                {% for c in clients %}
                                    <option value="{{ c.ClientID }}">#{{ c.ClientID }} - {{ c.FullName }} ({{ c.CompanyName or 'Cá nhân' }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <input type="text" name="title" class="form-control" placeholder="Tiêu đề công việc" required>
                        </div>
                        <div class="col-md-2">
                            <input type="number" step="0.01" name="budget" class="form-control" placeholder="Budget ($)" required>
                        </div>
                        <div class="col-md-3">
                            <input type="date" name="deadline" class="form-control">
                        </div>
                        <div class="col-md-9">
                            <input type="text" name="description" class="form-control" placeholder="Mô tả chi tiết công việc..." required>
                        </div>
                        <div class="col-md-3">
                            <button type="submit" class="btn btn-outline-primary w-100">Đăng Job</button>
                        </div>
                    </form>
                    {% endif %}
                </div>
            </div>

            <!-- PROPOSALS LIST & CREATE CONTRACT -->
            <div class="card shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">
                    Danh sách Proposals &amp; Tạo Hợp đồng 1–1 (BR-04)
                </div>
                <div class="card-body">
                    <div class="table-responsive mb-3">
                        <table class="table table-sm table-bordered align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>ProposalID</th>
                                    <th>Job</th>
                                    <th>Freelancer</th>
                                    <th>Giá chào</th>
                                    <th>Thời gian</th>
                                    <th>Trạng thái</th>
                                </tr>
                            </thead>
                            <tbody>
                            {% for p in proposals %}
                                <tr>
                                    <td>#{{ p.ProposalID }}</td>
                                    <td>#{{ p.JobID }} - {{ p.JobTitle }}</td>
                                    <td>#{{ p.FreelancerID }} - {{ p.FreelancerName }}</td>
                                    <td class="fw-semibold">${{ "%.2f"|format(p.BidAmount) }}</td>
                                    <td>{{ p.DeliveryTime or 'N/A' }}</td>
                                    <td><span class="badge bg-secondary">{{ p.Status }}</span></td>
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </div>

                    {% if role_view in ['All', 'Client'] %}
                    <form method="POST" action="/contracts/create" class="row g-2 align-items-center">
                        <input type="hidden" name="tab" value="jobs">
                        <div class="col-md-5">
                            <select name="proposal_id" class="form-select" required>
                                <option value="">-- Chọn Proposal để tạo Contract (1-1) --</option>
                                {% for p in proposals %}
                                    <option value="{{ p.ProposalID }}">Proposal #{{ p.ProposalID }} | Job #{{ p.JobID }} | {{ p.FreelancerName }} (${{ "%.2f"|format(p.BidAmount) }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-2">
                            <input type="number" step="0.01" name="amount" class="form-control" placeholder="Amount ($)" required>
                        </div>
                        <div class="col-md-2">
                            <input type="date" name="start_date" class="form-control" required>
                        </div>
                        <div class="col-md-3">
                            <button type="submit" class="btn btn-dark w-100">Tạo Contract</button>
                        </div>
                    </form>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- TAB 2: CONTRACTS, MILESTONES & PAYMENTS -->
        <div class="tab-pane fade {{ 'show active' if active_tab == 'contracts' else '' }}" id="tab-contracts">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-success text-white fw-bold">
                    Tiến độ Hợp đồng &amp; Thanh toán (View: vw_contract_payment_progress)
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>ContractID</th>
                                    <th>Client</th>
                                    <th>Freelancer</th>
                                    <th>Trạng thái</th>
                                    <th>Giá trị HĐ</th>
                                    <th>Mốc Approved</th>
                                    <th>Đã thanh toán</th>
                                    <th>Còn lại</th>
                                </tr>
                            </thead>
                            <tbody>
                            {% for c in contracts %}
                                <tr>
                                    <td><strong>#{{ c.ContractID }}</strong></td>
                                    <td>{{ c.ClientName }}</td>
                                    <td>{{ c.FreelancerName }}</td>
                                    <td><span class="badge bg-dark">{{ c.ContractStatus }}</span></td>
                                    <td>${{ "%.2f"|format(c.ContractAmount) }}</td>
                                    <td>{{ c.ApprovedMilestones }} / {{ c.TotalMilestones }}</td>
                                    <td class="text-success fw-bold">${{ "%.2f"|format(c.TotalPaidAmount) }}</td>
                                    <td>${{ "%.2f"|format(c.RemainingAmount) }}</td>
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </div>

                    {% if role_view in ['All', 'Client'] %}
                    <hr>
                    <h6 class="fw-bold">Thêm Cột mốc mới (Trigger trg_milestones_before_insert kiểm tra tổng tiền <= Contract.Amount - BR-05)</h6>
                    <form method="POST" action="/milestones/create" class="row g-2">
                        <input type="hidden" name="tab" value="contracts">
                        <div class="col-md-3">
                            <select name="contract_id" class="form-select" required>
                                <option value="">-- Chọn Contract --</option>
                                {% for c in contracts %}
                                    <option value="{{ c.ContractID }}">Contract #{{ c.ContractID }} (${{ "%.2f"|format(c.ContractAmount) }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <input type="text" name="title" class="form-control" placeholder="Tên cột mốc" required>
                        </div>
                        <div class="col-md-2">
                            <input type="number" step="0.01" name="amount" class="form-control" placeholder="Số tiền ($)" required>
                        </div>
                        <div class="col-md-3">
                            <div class="input-group">
                                <input type="date" name="due_date" class="form-control" required>
                                <button type="submit" class="btn btn-success">Thêm Mốc</button>
                            </div>
                        </div>
                    </form>
                    {% endif %}
                </div>
            </div>

            <div class="card shadow-sm">
                <div class="card-header bg-secondary text-white fw-bold">
                    Cột mốc (Milestones) &amp; Thanh toán 1–1 (Payments - BR-09)
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-sm table-bordered align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>MilestoneID</th>
                                    <th>HĐ</th>
                                    <th>Tên cột mốc</th>
                                    <th>Số tiền</th>
                                    <th>Trạng thái Mốc</th>
                                    <th>Thanh toán (1–1)</th>
                                    <th>Thao tác Demo</th>
                                </tr>
                            </thead>
                            <tbody>
                            {% for m in milestones %}
                                <tr>
                                    <td>#{{ m.MilestoneID }}</td>
                                    <td>#{{ m.ContractID }}</td>
                                    <td>{{ m.Title }}</td>
                                    <td>${{ "%.2f"|format(m.Amount) }}</td>
                                    <td>
                                        {% if m.Status == 'Approved' %}
                                            <span class="badge bg-success">Approved</span>
                                        {% elif m.Status == 'In Review' %}
                                            <span class="badge bg-warning text-dark">In Review</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ m.Status }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if m.PaymentStatus %}
                                            <span class="badge bg-primary">{{ m.PaymentStatus }} (${{ "%.2f"|format(m.PaymentAmount) }})</span>
                                        {% else %}
                                            <span class="text-muted">Chưa thanh toán</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if role_view != 'Auditor' %}
                                            {% if m.Status != 'Approved' %}
                                                <a href="{{ url_for('approve_milestone', milestone_id=m.MilestoneID, tab='contracts', role=role_view) }}"
                                                   class="btn btn-sm btn-warning">Approve</a>
                                            {% endif %}
                                            {% if not m.PaymentStatus and role_view in ['All', 'Client'] %}
                                                <form method="POST" action="/payments/create" class="d-inline-flex gap-1 align-items-center">
                                                    <input type="hidden" name="tab" value="contracts">
                                                    <input type="hidden" name="milestone_id" value="{{ m.MilestoneID }}">
                                                    <input type="hidden" name="amount" value="{{ m.Amount }}">
                                                    <select name="method" class="form-select form-select-sm" style="width: 125px;">
                                                        <option value="Bank Transfer">Bank Transfer</option>
                                                        <option value="PayPal">PayPal</option>
                                                        <option value="Credit Card">Credit Card</option>
                                                        <option value="E-Wallet">E-Wallet</option>
                                                    </select>
                                                    <button type="submit" class="btn btn-sm btn-success">Thanh toán</button>
                                                </form>
                                            {% endif %}
                                        {% else %}
                                            <span class="text-muted small">Chỉ đọc</span>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: FREELANCERS, SKILLS & REVIEWS -->
        <div class="tab-pane fade {{ 'show active' if active_tab == 'freelancers' else '' }}" id="tab-freelancers">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-info text-dark fw-bold">
                    Hồ sơ Freelancer &amp; Kỹ năng (View: vw_freelancer_profiles)
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>ID</th>
                                    <th>Họ tên</th>
                                    <th>Chức danh</th>
                                    <th>Kỹ năng</th>
                                    <th>HĐ hoàn thành</th>
                                    <th>AverageRating</th>
                                </tr>
                            </thead>
                            <tbody>
                            {% for f in freelancers %}
                                <tr>
                                    <td><strong>#{{ f.FreelancerID }}</strong></td>
                                    <td>{{ f.FullName }}</td>
                                    <td>{{ f.ProfessionalTitle or 'N/A' }}</td>
                                    <td>{{ f.SkillsList or 'Chưa cập nhật' }}</td>
                                    <td>{{ f.CompletedContracts }}</td>
                                    <td class="fw-bold text-warning bg-dark text-center">★ {{ "%.2f"|format(f.AverageRating or 0) }}</td>
                                </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                    </div>

                    {% if role_view in ['All', 'Freelancer'] %}
                    <hr>
                    <h6 class="fw-bold">Gán kỹ năng cho Freelancer (Freelancer_Skills - BR-08)</h6>
                    <form method="POST" action="/skills/assign" class="row g-2">
                        <input type="hidden" name="tab" value="freelancers">
                        <div class="col-md-5">
                            <select name="freelancer_id" class="form-select" required>
                                <option value="">-- Chọn Freelancer --</option>
                                {% for f in freelancers %}
                                    <option value="{{ f.FreelancerID }}">#{{ f.FreelancerID }} - {{ f.FullName }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <select name="skill_id" class="form-select" required>
                                <option value="">-- Chọn Kỹ năng --</option>
                                {% for s in skills %}
                                    <option value="{{ s.SkillID }}">{{ s.SkillName }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-3">
                            <button type="submit" class="btn btn-info text-dark fw-semibold w-100">Gán Kỹ năng</button>
                        </div>
                    </form>
                    {% endif %}
                </div>
            </div>

            {% if role_view != 'Auditor' %}
            <div class="card shadow-sm">
                <div class="card-header bg-dark text-white fw-bold">
                    Gửi Review cho Hợp đồng đã Completed (Tự động cập nhật Users.AverageRating qua Trigger)
                </div>
                <div class="card-body">
                    <form method="POST" action="/reviews/create" class="row g-2">
                        <input type="hidden" name="tab" value="freelancers">
                        <div class="col-md-2">
                            <select name="contract_id" class="form-select" required>
                                <option value="">-- Contract --</option>
                                {% for c in contracts %}
                                    <option value="{{ c.ContractID }}">#{{ c.ContractID }} ({{ c.ContractStatus }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-2">
                            <select name="reviewer_id" class="form-select" required>
                                <option value="">-- Reviewer --</option>
                                {% for u in users %}
                                    <option value="{{ u.UserID }}">#{{ u.UserID }} - {{ u.FullName }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-2">
                            <select name="reviewee_id" class="form-select" required>
                                <option value="">-- Reviewee --</option>
                                {% for u in users %}
                                    <option value="{{ u.UserID }}">#{{ u.UserID }} - {{ u.FullName }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-2">
                            <input type="number" min="1" max="5" name="rating" class="form-control" placeholder="Sao (1-5)" required>
                        </div>
                        <div class="col-md-2">
                            <input type="text" name="comment" class="form-control" placeholder="Nhận xét...">
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-dark w-100">Gửi Review</button>
                        </div>
                    </form>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@app.route("/")
def index():
    active_tab = request.args.get("tab", "jobs")
    if active_tab not in ("jobs", "contracts", "freelancers"):
        active_tab = "jobs"

    role_view = request.args.get("role", "All")
    if role_view not in ("All", "Client", "Freelancer", "Auditor"):
        role_view = "All"

    search_q = (request.args.get("q") or "").strip()
    min_budget_raw = (request.args.get("min_budget") or "").strip()
    min_budget = ""
    min_budget_val = None
    if min_budget_raw:
        try:
            min_budget_val = float(min_budget_raw)
            min_budget = min_budget_raw
        except ValueError:
            min_budget_val = None

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        # View 1: Open Jobs with optional search & budget filter
        job_sql = "SELECT * FROM vw_active_jobs_summary WHERE 1=1"
        job_params = []
        if search_q:
            job_sql += " AND (JobTitle LIKE %s OR ClientName LIKE %s OR COALESCE(CompanyName, '') LIKE %s)"
            like_q = f"%{search_q}%"
            job_params.extend([like_q, like_q, like_q])
        if min_budget_val is not None:
            job_sql += " AND Budget >= %s"
            job_params.append(min_budget_val)
        job_sql += " ORDER BY JobID ASC"
        cur.execute(job_sql, job_params)
        jobs = cur.fetchall()

        # View 2: Contracts progress
        cur.execute("SELECT * FROM vw_contract_payment_progress ORDER BY ContractID ASC")
        contracts = cur.fetchall()

        # Milestones + Payments (1-1)
        cur.execute("""
            SELECT
                m.MilestoneID,
                m.ContractID,
                m.Title,
                m.Amount,
                m.DueDate,
                m.Status,
                p.Status AS PaymentStatus,
                p.Amount AS PaymentAmount
            FROM Milestones AS m
            LEFT JOIN Payments AS p ON m.MilestoneID = p.MilestoneID
            ORDER BY m.ContractID ASC, m.MilestoneID ASC
        """)
        milestones = cur.fetchall()

        # View 3: Freelancer profiles
        cur.execute("SELECT * FROM vw_freelancer_profiles ORDER BY FreelancerID ASC")
        freelancers = cur.fetchall()

        # Proposals list for selection & contract creation
        cur.execute("""
            SELECT
                p.ProposalID,
                p.JobID,
                j.Title AS JobTitle,
                p.FreelancerID,
                u.FullName AS FreelancerName,
                p.BidAmount,
                p.DeliveryTime,
                p.Status
            FROM Proposals AS p
            INNER JOIN Jobs AS j ON p.JobID = j.JobID
            INNER JOIN Users AS u ON p.FreelancerID = u.UserID
            ORDER BY p.ProposalID ASC
        """)
        proposals = cur.fetchall()

        # Dropdown lookup data
        cur.execute("""
            SELECT c.ClientID, u.FullName, c.CompanyName
            FROM Clients AS c
            INNER JOIN Users AS u ON c.ClientID = u.UserID
            ORDER BY c.ClientID ASC
        """)
        clients = cur.fetchall()

        cur.execute("SELECT UserID, FullName, Role FROM Users ORDER BY UserID ASC")
        users = cur.fetchall()

        cur.execute("SELECT SkillID, SkillName FROM Skills ORDER BY SkillName ASC")
        skills = cur.fetchall()

        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM vw_active_jobs_summary) AS open_jobs,
                (SELECT COUNT(*) FROM Contracts) AS total_contracts,
                (SELECT COALESCE(SUM(Amount), 0.00) FROM Payments WHERE Status = 'Completed') AS total_paid,
                (SELECT COUNT(*) FROM Freelancers) AS total_freelancers
        """)
        stats = cur.fetchone()

        return render_template_string(
            HTML_PAGE,
            active_tab=active_tab,
            role_view=role_view,
            search_q=search_q,
            min_budget=min_budget,
            jobs=jobs,
            contracts=contracts,
            milestones=milestones,
            freelancers=freelancers,
            proposals=proposals,
            clients=clients,
            users=users,
            skills=skills,
            stats=stats,
        )
    except Error as e:
        return f"<h3>Lỗi kết nối MySQL:</h3><pre>{e}</pre>", 500
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/jobs/create", methods=["POST"])
def create_job():
    tab = request.form.get("tab", "jobs")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        deadline_val = request.form.get("deadline") or None
        cur.execute(
            """
            INSERT INTO Jobs (ClientID, Title, Description, Budget, Deadline, Status)
            VALUES (%s, %s, %s, %s, %s, 'Open')
            """,
            (
                request.form["client_id"],
                request.form["title"],
                request.form["description"],
                request.form["budget"],
                deadline_val,
            ),
        )
        conn.commit()
        flash("Đã tạo Job mới thành công!", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"MySQL từ chối tạo Job: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


@app.route("/proposals/create", methods=["POST"])
def create_proposal():
    tab = request.form.get("tab", "jobs")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Proposals (JobID, FreelancerID, BidAmount, DeliveryTime, Status)
            VALUES (%s, %s, %s, %s, 'Pending')
            """,
            (
                request.form["job_id"],
                request.form["freelancer_id"],
                request.form["bid_amount"],
                request.form["delivery_time"],
            ),
        )
        conn.commit()
        flash("Nộp Proposal thành công!", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"MySQL từ chối Proposal: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


@app.route("/contracts/create", methods=["POST"])
def create_contract():
    tab = request.form.get("tab", "jobs")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        proposal_id = request.form["proposal_id"]

        cur.execute("""
            SELECT p.ProposalID, p.FreelancerID, j.ClientID
            FROM Proposals AS p
            INNER JOIN Jobs AS j ON p.JobID = j.JobID
            WHERE p.ProposalID = %s
        """, (proposal_id,))
        row = cur.fetchone()
        if not row:
            flash("Không tìm thấy Proposal được chọn.", "warning")
            return redirect(url_for("index", tab=tab))

        cur.execute(
            """
            INSERT INTO Contracts (ProposalID, ClientID, FreelancerID, Amount, StartDate, Status)
            VALUES (%s, %s, %s, %s, %s, 'Active')
            """,
            (
                row["ProposalID"],
                row["ClientID"],
                row["FreelancerID"],
                request.form["amount"],
                request.form["start_date"],
            ),
        )
        cur.execute("UPDATE Proposals SET Status = 'Accepted' WHERE ProposalID = %s", (proposal_id,))
        conn.commit()
        flash("Đã tạo Contract mới và cập nhật Proposal sang Accepted!", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"MySQL từ chối tạo Contract: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


@app.route("/milestones/create", methods=["POST"])
def create_milestone():
    tab = request.form.get("tab", "contracts")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Milestones (ContractID, Title, Amount, DueDate, Status)
            VALUES (%s, %s, %s, %s, 'Pending')
            """,
            (
                request.form["contract_id"],
                request.form["title"],
                request.form["amount"],
                request.form["due_date"],
            ),
        )
        conn.commit()
        flash("Đã thêm cột mốc mới thành công!", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"Trigger/Ràng buộc chặn thêm Milestone: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


@app.route("/milestones/approve/<int:milestone_id>")
def approve_milestone(milestone_id):
    tab = request.args.get("tab", "contracts")
    role_view = request.args.get("role", "All")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Milestones SET Status = 'Approved' WHERE MilestoneID = %s",
            (milestone_id,),
        )
        conn.commit()
        flash(f"Đã chuyển Milestone #{milestone_id} sang trạng thái Approved.", "info")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"Lỗi cập nhật Milestone: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab, role=role_view))


@app.route("/payments/create", methods=["POST"])
def create_payment():
    tab = request.form.get("tab", "contracts")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Payments (MilestoneID, Amount, PaymentMethod, Status)
            VALUES (%s, %s, %s, 'Completed')
            """,
            (
                request.form["milestone_id"],
                request.form["amount"],
                request.form["method"],
            ),
        )
        conn.commit()
        flash(f"Thanh toán thành công cho Milestone #{request.form['milestone_id']}!", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"Trigger/Ràng buộc MySQL chặn thanh toán: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


@app.route("/skills/assign", methods=["POST"])
def assign_skill():
    tab = request.form.get("tab", "freelancers")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Freelancer_Skills (FreelancerID, SkillID)
            VALUES (%s, %s)
            """,
            (request.form["freelancer_id"], request.form["skill_id"]),
        )
        conn.commit()
        flash("Đã gán kỹ năng cho Freelancer!", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"MySQL từ chối gán kỹ năng: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


@app.route("/reviews/create", methods=["POST"])
def create_review():
    tab = request.form.get("tab", "freelancers")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Reviews (ContractID, ReviewerID, RevieweeID, Rating, Comment)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.form["contract_id"],
                request.form["reviewer_id"],
                request.form["reviewee_id"],
                request.form["rating"],
                request.form.get("comment") or None,
            ),
        )
        conn.commit()
        flash("Gửi Review thành công! Trigger đã tự động cập nhật AverageRating.", "success")
    except Error as e:
        if conn:
            conn.rollback()
        flash(f"Trigger/Ràng buộc MySQL chặn Review: {e.msg} (Code: {e.errno})", "danger")
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index", tab=tab))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)