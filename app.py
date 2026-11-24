from flask import Flask, request, redirect, url_for, render_template_string, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "mini_upwork_phase4_secret_key"

# Cấu hình kết nối MySQL 8.0+ tới CSDL mini_upwork
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "acces123@123",  # <-- Điền mật khẩu root MySQL của bạn tại đây
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
    <title>Mini-Upwork — Phase 4 Demo (INT1313 Databases)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-dark bg-dark mb-4 shadow-sm">
    <div class="container">
        <span class="navbar-brand fw-bold">Mini-Upwork Ecosystem — Phase 4 Demo</span>
        <span class="text-light small">INT1313_Databases | Nhóm 3 (Khải – Khánh – Long)</span>
    </div>
</nav>

<div class="container pb-5">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, msg in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
            {{ msg }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <!-- 1. OPEN JOBS & SUBMIT PROPOSAL -->
    <div class="card mb-4 shadow-sm">
        <div class="card-header bg-primary text-white fw-bold">
            1. Công việc đang mở &amp; Nộp Proposal (View: vw_active_jobs_summary)
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered table-hover align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>JobID</th>
                            <th>Tiêu đề công việc</th>
                            <th>Client / Công ty</th>
                            <th>Ngân sách ($)</th>
                            <th>Deadline</th>
                            <th>Số Proposal</th>
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
                            <td><span class="badge bg-secondary">{{ j.TotalProposals }}</span></td>
                        </tr>
                    {% else %}
                        <tr><td colspan="6" class="text-center text-muted">Không có công việc nào ở trạng thái Open.</td></tr>
                    {% endfor %}
                    </tbody>
                </table>
            </div>

            <hr>
            <h6 class="fw-bold">Nộp Proposal mới cho Job (Kiểm tra FK &amp; UNIQUE (JobID, FreelancerID) - BR-03)</h6>
            <form method="POST" action="/proposals/create" class="row g-2">
                <div class="col-md-2">
                    <input type="number" name="job_id" class="form-control" placeholder="JobID (vd: 4)" required>
                </div>
                <div class="col-md-2">
                    <input type="number" name="freelancer_id" class="form-control" placeholder="FreelancerID (vd: 6)" required>
                </div>
                <div class="col-md-2">
                    <input type="number" step="0.01" name="bid_amount" class="form-control" placeholder="BidAmount ($)" required>
                </div>
                <div class="col-md-3">
                    <input type="text" name="delivery_time" class="form-control" placeholder="DeliveryTime (vd: 12 days)" required>
                </div>
                <div class="col-md-3">
                    <button type="submit" class="btn btn-primary w-100">Gửi Proposal</button>
                </div>
            </form>

            <hr>
            <h6 class="fw-bold">Đăng Job mới (Client tạo Job)</h6>
            <form method="POST" action="/jobs/create" class="row g-2">
                <div class="col-md-2">
                    <input type="number" name="client_id" class="form-control" placeholder="ClientID (1-3)" required>
                </div>
                <div class="col-md-3">
                    <input type="text" name="title" class="form-control" placeholder="Tiêu đề Job" required>
                </div>
                <div class="col-md-2">
                    <input type="number" step="0.01" name="budget" class="form-control" placeholder="Budget ($)" required>
                </div>
                <div class="col-md-2">
                    <input type="date" name="deadline" class="form-control">
                </div>
                <div class="col-md-3">
                    <button type="submit" class="btn btn-outline-primary w-100">Đăng Job</button>
                </div>
                <div class="col-12">
                    <input type="text" name="description" class="form-control" placeholder="Mô tả chi tiết công việc..." required>
                </div>
            </form>
        </div>
    </div>

    <!-- 2. CONTRACTS, MILESTONES & PAYMENTS (1-1) -->
    <div class="card mb-4 shadow-sm">
        <div class="card-header bg-success text-white fw-bold">
            2. Tiến độ Hợp đồng, Nghiệm thu Milestone &amp; Thanh toán 1–1 (View: vw_contract_payment_progress)
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>ContractID</th>
                            <th>Client</th>
                            <th>Freelancer</th>
                            <th>Trạng thái HĐ</th>
                            <th>Giá trị HĐ ($)</th>
                            <th>Mốc Approved</th>
                            <th>Đã thanh toán ($)</th>
                            <th>Còn lại ($)</th>
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

            <h6 class="fw-bold mt-3">Danh sách Cột mốc (Milestones) &amp; Thanh toán (Payments)</h6>
            <div class="table-responsive">
                <table class="table table-sm table-bordered align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>MilestoneID</th>
                            <th>HĐ</th>
                            <th>Tên cột mốc</th>
                            <th>Số tiền ($)</th>
                            <th>Trạng thái Mốc</th>
                            <th>Thanh toán (BR-09)</th>
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
                                {% if m.Status != 'Approved' %}
                                    <a href="/milestones/approve/{{ m.MilestoneID }}" class="btn btn-sm btn-warning">Approve Mốc</a>
                                {% endif %}
                                {% if not m.PaymentStatus %}
                                    <form method="POST" action="/payments/create" class="d-inline-flex gap-1 align-items-center">
                                        <input type="hidden" name="milestone_id" value="{{ m.MilestoneID }}">
                                        <input type="hidden" name="amount" value="{{ m.Amount }}">
                                        <select name="method" class="form-select form-select-sm" style="width: 130px;">
                                            <option value="Bank Transfer">Bank Transfer</option>
                                            <option value="PayPal">PayPal</option>
                                            <option value="Credit Card">Credit Card</option>
                                            <option value="E-Wallet">E-Wallet</option>
                                        </select>
                                        <button type="submit" class="btn btn-sm btn-success">Thanh toán</button>
                                    </form>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- 3. FREELANCER PROFILES & SUBMIT REVIEW -->
    <div class="card shadow-sm">
        <div class="card-header bg-secondary text-white fw-bold">
            3. Hồ sơ Freelancer &amp; Đánh giá chéo (View: vw_freelancer_profiles &amp; Trigger AverageRating)
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>FreelancerID</th>
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

            <hr>
            <h6 class="fw-bold">Gửi Review cho Hợp đồng đã Completed (Tự động cập nhật Users.AverageRating qua Trigger)</h6>
            <form method="POST" action="/reviews/create" class="row g-2">
                <div class="col-md-2">
                    <input type="number" name="contract_id" class="form-control" placeholder="ContractID (vd: 1)" required>
                </div>
                <div class="col-md-2">
                    <input type="number" name="reviewer_id" class="form-control" placeholder="ReviewerID" required>
                </div>
                <div class="col-md-2">
                    <input type="number" name="reviewee_id" class="form-control" placeholder="RevieweeID" required>
                </div>
                <div class="col-md-2">
                    <input type="number" min="1" max="5" name="rating" class="form-control" placeholder="Rating (1-5)" required>
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
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@app.route("/")
def index():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM vw_active_jobs_summary ORDER BY JobID ASC")
        jobs = cur.fetchall()

        cur.execute("SELECT * FROM vw_contract_payment_progress ORDER BY ContractID ASC")
        contracts = cur.fetchall()

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

        cur.execute("SELECT * FROM vw_freelancer_profiles ORDER BY FreelancerID ASC")
        freelancers = cur.fetchall()

        return render_template_string(
            HTML_PAGE,
            jobs=jobs,
            contracts=contracts,
            milestones=milestones,
            freelancers=freelancers,
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
    return redirect(url_for("index"))


@app.route("/proposals/create", methods=["POST"])
def create_proposal():
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
    return redirect(url_for("index"))


@app.route("/milestones/approve/<int:milestone_id>")
def approve_milestone(milestone_id):
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
    return redirect(url_for("index"))


@app.route("/payments/create", methods=["POST"])
def create_payment():
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
    return redirect(url_for("index"))


@app.route("/reviews/create", methods=["POST"])
def create_review():
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
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)