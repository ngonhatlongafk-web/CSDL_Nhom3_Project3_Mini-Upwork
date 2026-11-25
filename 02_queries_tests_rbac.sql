USE mini_upwork;

-- 1. Du lieu mau
INSERT INTO Users (FullName, Email, Password, Role) VALUES
    ('Nguyen Minh Tuan',   'tuan.client@techcorp.vn',    '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx1', 'Client'),
    ('Tran Thi Mai',       'mai.client@finhub.vn',       '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx2', 'Client'),
    ('Le Hoang Nam',       'nam.client@ecomstudio.vn',   '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx3', 'Client'),
    ('Nguyen Le Khai',     'khai.dev@freelance.vn',      '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx4', 'Freelancer'),
    ('Huynh Duy Khanh',    'khanh.data@freelance.vn',    '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx5', 'Freelancer'),
    ('Ngo Nhat Long',      'long.uiux@freelance.vn',     '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx6', 'Freelancer'),
    ('System Admin',       'admin@miniupwork.vn',        '$2b$12$KIX9a8b7c6d5e4f3g2h1i0jklmnopqrstuvwx7', 'Admin');

INSERT INTO Clients (ClientID, CompanyName, Location) VALUES
    (1, 'TechCorp Vietnam',  'Ho Chi Minh City'),
    (2, 'FinHub Solutions',  'Ha Noi'),
    (3, 'EcomStudio Co.',    'Da Nang');

INSERT INTO Freelancers (FreelancerID, Title) VALUES
    (4, 'Senior Full-Stack Developer'),
    (5, 'Database & Backend Engineer'),
    (6, 'UI/UX & Frontend Specialist');

INSERT INTO Skills (SkillName) VALUES
    ('MySQL'),
    ('Python'),
    ('ReactJS'),
    ('Node.js'),
    ('UI/UX Design'),
    ('Docker');

INSERT INTO Freelancer_Skills (FreelancerID, SkillID) VALUES
    (4, 1), (4, 3), (4, 4),
    (5, 1), (5, 2), (5, 6),
    (6, 3), (6, 5);

INSERT INTO Jobs (ClientID, Title, Description, Budget, Deadline, Status) VALUES
    (1, 'Xay dung he thong quan ly ban hang',       'Phat trien ung dung web quan ly don hang va ton kho bang ReactJS & Node.js.', 2500.00, '2026-12-30', 'Closed'),
    (2, 'Thiet ke CSDL & API thanh toan',           'Thiet ke luoc do MySQL chuan 3NF/BCNF va viet REST API bao mat.',             1800.00, '2026-12-20', 'Closed'),
    (3, 'Thiet ke giao dien app thuong mai dien tu','Thiet ke Figma UI/UX va cat giao dien React cho nen tang thuong mai dien tu.', 1500.00, '2027-01-15', 'In Progress'),
    (1, 'Toi uu hoa truy van MySQL kho du lieu',    'Phan tich EXPLAIN, danh chi muc va toi uu bao cao doanh thu thoi gian thuc.', 1200.00, '2027-02-01', 'Open');

INSERT INTO Proposals (JobID, FreelancerID, BidAmount, DeliveryTime, Status) VALUES
    (1, 4, 2400.00, '30 days', 'Accepted'),
    (1, 5, 2350.00, '35 days', 'Rejected'),
    (2, 5, 1750.00, '21 days', 'Accepted'),
    (3, 6, 1400.00, '25 days', 'Accepted'),
    (4, 4, 1150.00, '14 days', 'Pending'),
    (4, 5, 1050.00, '10 days', 'Pending');

INSERT INTO Contracts (ProposalID, ClientID, FreelancerID, Amount, StartDate, EndDate, Status) VALUES
    (1, 1, 4, 2400.00, '2026-09-01', '2026-10-01', 'Completed'),
    (3, 2, 5, 1750.00, '2026-09-15', '2026-10-10', 'Completed'),
    (4, 3, 6, 1400.00, '2026-11-01', NULL,         'Active');

INSERT INTO Milestones (ContractID, Title, Amount, DueDate, Status) VALUES
    (1, 'Giai doan 1: Thiet ke kien truc & CSDL', 1000.00, '2026-09-15', 'Approved'),
    (1, 'Giai doan 2: Hoan thien Web & Ban giao', 1400.00, '2026-10-01', 'Approved'),
    (2, 'Giai doan 1: Luoc do CSDL & DDL',         750.00, '2026-09-25', 'Approved'),
    (2, 'Giai doan 2: API & Kiem thu bao mat',    1000.00, '2026-10-10', 'Approved'),
    (3, 'Giai doan 1: Wireframe & Prototype',      500.00, '2026-11-15', 'Approved'),
    (3, 'Giai doan 2: Giao dien React trang chu',  500.00, '2026-12-01', 'In Review'),
    (3, 'Giai doan 3: Hoan thien & Ban giao',      400.00, '2026-12-15', 'Pending');

INSERT INTO Payments (MilestoneID, Amount, PaymentMethod, PaidAt, Status) VALUES
    (1, 1000.00, 'Bank Transfer', '2026-09-16 10:00:00', 'Completed'),
    (2, 1400.00, 'Bank Transfer', '2026-10-02 14:30:00', 'Completed'),
    (3,  750.00, 'Credit Card',   '2026-09-26 09:15:00', 'Completed'),
    (4, 1000.00, 'PayPal',        '2026-10-11 16:45:00', 'Completed'),
    (5,  500.00, 'E-Wallet',      '2026-11-16 11:20:00', 'Completed');

INSERT INTO Reviews (ContractID, ReviewerID, RevieweeID, Rating, Comment) VALUES
    (1, 1, 4, 5, 'Hoan thanh dung han, ma nguon sach va de bao tri.'),
    (1, 4, 1, 5, 'Khach hang trao doi ro rang, thanh toan nhanh chong.'),
    (2, 2, 5, 4, 'Thiet ke CSDL chat che, giai thich ky thuat tot.'),
    (2, 5, 2, 5, 'Yeu cau chi tiet, nghiem thu dung tien do.');

SELECT UserID, FullName, Role, AverageRating FROM Users;
SELECT * FROM vw_active_jobs_summary;
SELECT * FROM vw_contract_payment_progress;
SELECT * FROM vw_freelancer_profiles;

-- 2. Truy van nang cao
-- Cau 1: Tong hop dong va tong tien da thanh toan cua tung Khach hang
SELECT
    c.ClientID,
    u.FullName AS ClientName,
    c.CompanyName,
    COUNT(DISTINCT ct.ContractID) AS TotalContracts,
    COALESCE(SUM(CASE WHEN py.Status = 'Completed' THEN py.Amount ELSE 0 END), 0.00) AS TotalPaid
FROM Clients AS c
INNER JOIN Users AS u ON c.ClientID = u.UserID
LEFT JOIN Contracts AS ct ON c.ClientID = ct.ClientID
LEFT JOIN Milestones AS m ON ct.ContractID = m.ContractID
LEFT JOIN Payments AS py ON m.MilestoneID = py.MilestoneID
GROUP BY c.ClientID, u.FullName, c.CompanyName
ORDER BY TotalPaid DESC;

-- Cau 2: Freelancer co tu 2 ky nang tro len va diem danh gia >= 4.00
SELECT
    f.FreelancerID,
    u.FullName AS FreelancerName,
    f.Title,
    u.AverageRating,
    COUNT(DISTINCT fs.SkillID) AS SkillCount,
    COALESCE(SUM(CASE WHEN py.Status = 'Completed' THEN py.Amount ELSE 0 END), 0.00) AS TotalEarned
FROM Freelancers AS f
INNER JOIN Users AS u ON f.FreelancerID = u.UserID
INNER JOIN Freelancer_Skills AS fs ON f.FreelancerID = fs.FreelancerID
LEFT JOIN Contracts AS ct ON f.FreelancerID = ct.FreelancerID
LEFT JOIN Milestones AS m ON ct.ContractID = m.ContractID
LEFT JOIN Payments AS py ON m.MilestoneID = py.MilestoneID
GROUP BY f.FreelancerID, u.FullName, f.Title, u.AverageRating
HAVING COUNT(DISTINCT fs.SkillID) >= 2
   AND u.AverageRating >= 4.00
ORDER BY u.AverageRating DESC, TotalEarned DESC;

-- Cau 3: Xep hang Freelancer theo doanh thu va ty trong doanh thu toan san
WITH FreelancerRevenue AS (
    SELECT
        f.FreelancerID,
        u.FullName AS FreelancerName,
        COALESCE(SUM(CASE WHEN py.Status = 'Completed' THEN py.Amount ELSE 0 END), 0.00) AS TotalRevenue
    FROM Freelancers AS f
    INNER JOIN Users AS u ON f.FreelancerID = u.UserID
    LEFT JOIN Contracts AS ct ON f.FreelancerID = ct.FreelancerID
    LEFT JOIN Milestones AS m ON ct.ContractID = m.ContractID
    LEFT JOIN Payments AS py ON m.MilestoneID = py.MilestoneID
    GROUP BY f.FreelancerID, u.FullName
)
SELECT
    FreelancerID,
    FreelancerName,
    TotalRevenue,
    DENSE_RANK() OVER (ORDER BY TotalRevenue DESC) AS RevenueRank,
    ROUND(TotalRevenue * 100.0 / NULLIF(SUM(TotalRevenue) OVER (), 0), 2) AS RevenueSharePct
FROM FreelancerRevenue
ORDER BY RevenueRank, FreelancerID;

-- Cau 4: Tien do nghiem thu cot moc va thanh toan cua tung Hop dong
WITH MilestoneStats AS (
    SELECT
        m.ContractID,
        COUNT(m.MilestoneID) AS TotalMilestones,
        SUM(CASE WHEN m.Status = 'Approved' THEN 1 ELSE 0 END) AS ApprovedMilestones,
        COALESCE(SUM(CASE WHEN py.Status = 'Completed' THEN py.Amount ELSE 0 END), 0.00) AS PaidAmount
    FROM Milestones AS m
    LEFT JOIN Payments AS py ON m.MilestoneID = py.MilestoneID
    GROUP BY m.ContractID
)
SELECT
    ct.ContractID,
    ct.Status AS ContractStatus,
    ct.Amount AS ContractAmount,
    ms.TotalMilestones,
    ms.ApprovedMilestones,
    ROUND(ms.ApprovedMilestones * 100.0 / NULLIF(ms.TotalMilestones, 0), 2) AS CompletionPct,
    ms.PaidAmount,
    ct.Amount - ms.PaidAmount AS RemainingBalance
FROM Contracts AS ct
INNER JOIN MilestoneStats AS ms ON ct.ContractID = ms.ContractID
ORDER BY CompletionPct DESC, ct.ContractID;

-- Cau 5: De xuat co muc gia thap nhat cho moi cong viec dang mo
WITH RankedProposals AS (
    SELECT
        j.JobID,
        j.Title AS JobTitle,
        j.Budget AS ClientBudget,
        p.ProposalID,
        u.FullName AS FreelancerName,
        p.BidAmount,
        p.DeliveryTime,
        ROW_NUMBER() OVER (
            PARTITION BY j.JobID
            ORDER BY p.BidAmount ASC, p.ProposalID ASC
        ) AS BidRank
    FROM Jobs AS j
    INNER JOIN Proposals AS p ON j.JobID = p.JobID
    INNER JOIN Users AS u ON p.FreelancerID = u.UserID
    WHERE j.Status = 'Open'
)
SELECT
    JobID,
    JobTitle,
    ClientBudget,
    ProposalID,
    FreelancerName,
    BidAmount,
    DeliveryTime
FROM RankedProposals
WHERE BidRank = 1;

-- 3. Kiem tra hieu nang chi muc (EXPLAIN)
EXPLAIN
SELECT JobID, Title, Budget, Deadline
FROM Jobs
WHERE Status = 'Open' AND Budget >= 1000.00;

EXPLAIN
SELECT MilestoneID, Title, Amount, DueDate
FROM Milestones
WHERE ContractID = 3 AND Status = 'Approved';

EXPLAIN
SELECT PaymentID, MilestoneID, Amount, PaidAt
FROM Payments
WHERE Status = 'Completed' AND PaidAt >= '2026-09-01 00:00:00';

-- 4. Kiem thu rang buoc (chay tung cau lenh rieng le)
/*
-- TC-01: Rating ngoai khoang 1..5
INSERT INTO Reviews (ContractID, ReviewerID, RevieweeID, Rating, Comment)
VALUES (1, 1, 4, 6, 'Diem khong hop le');

-- TC-02: Tu danh gia chinh minh
INSERT INTO Reviews (ContractID, ReviewerID, RevieweeID, Rating, Comment)
VALUES (1, 4, 4, 5, 'Tu danh gia');

-- TC-03: Nop trung de xuat cho cung 1 cong viec
INSERT INTO Proposals (JobID, FreelancerID, BidAmount, DeliveryTime, Status)
VALUES (4, 5, 990.00, '7 days', 'Pending');

-- TC-04: Tao 2 hop dong tu cung 1 de xuat
INSERT INTO Contracts (ProposalID, ClientID, FreelancerID, Amount, StartDate, Status)
VALUES (1, 1, 4, 2400.00, '2026-10-05', 'Active');

-- TC-05: Thanh toan trung lap tren cung 1 cot moc
INSERT INTO Payments (MilestoneID, Amount, PaymentMethod, Status)
VALUES (1, 1000.00, 'Bank Transfer', 'Completed');

-- TC-06: Thanh toan cot moc chua Approved
INSERT INTO Payments (MilestoneID, Amount, PaymentMethod, Status)
VALUES (6, 500.00, 'Bank Transfer', 'Completed');

-- TC-07: Tong tien cot moc vuot gia tri hop dong
INSERT INTO Milestones (ContractID, Title, Amount, DueDate, Status)
VALUES (3, 'Cot moc phat sinh vuot ngan sach', 500.00, '2026-12-25', 'Pending');

-- TC-08: Xoa cot moc da co thanh toan
DELETE FROM Milestones WHERE MilestoneID = 1;

-- TC-09: Trang thai Milestone khong hop le
INSERT INTO Milestones (ContractID, Title, Amount, DueDate, Status)
VALUES (3, 'Cot moc trang thai sai', 100.00, '2026-12-20', 'Held');

-- TC-10: Cung 1 nguoi danh gia 2 lan tren 1 hop dong
INSERT INTO Reviews (ContractID, ReviewerID, RevieweeID, Rating, Comment)
VALUES (1, 1, 4, 4, 'Danh gia lan thu hai');
*/

-- 5. Phan quyen RBAC
CREATE ROLE IF NOT EXISTS
    'role_admin',
    'role_client',
    'role_freelancer',
    'role_auditor';

GRANT ALL PRIVILEGES ON mini_upwork.* TO 'role_admin';

GRANT SELECT ON mini_upwork.Users TO 'role_client';
GRANT SELECT, UPDATE ON mini_upwork.Clients TO 'role_client';
GRANT SELECT ON mini_upwork.Freelancers TO 'role_client';
GRANT SELECT ON mini_upwork.Skills TO 'role_client';
GRANT SELECT ON mini_upwork.Freelancer_Skills TO 'role_client';
GRANT SELECT, INSERT, UPDATE, DELETE ON mini_upwork.Jobs TO 'role_client';
GRANT SELECT, UPDATE ON mini_upwork.Proposals TO 'role_client';
GRANT SELECT, INSERT, UPDATE ON mini_upwork.Contracts TO 'role_client';
GRANT SELECT, INSERT, UPDATE, DELETE ON mini_upwork.Milestones TO 'role_client';
GRANT SELECT, INSERT ON mini_upwork.Payments TO 'role_client';
GRANT SELECT, INSERT ON mini_upwork.Reviews TO 'role_client';
GRANT SELECT ON mini_upwork.vw_active_jobs_summary TO 'role_client';
GRANT SELECT ON mini_upwork.vw_contract_payment_progress TO 'role_client';
GRANT SELECT ON mini_upwork.vw_freelancer_profiles TO 'role_client';

GRANT SELECT ON mini_upwork.Users TO 'role_freelancer';
GRANT SELECT ON mini_upwork.Clients TO 'role_freelancer';
GRANT SELECT, UPDATE ON mini_upwork.Freelancers TO 'role_freelancer';
GRANT SELECT ON mini_upwork.Skills TO 'role_freelancer';
GRANT SELECT, INSERT, DELETE ON mini_upwork.Freelancer_Skills TO 'role_freelancer';
GRANT SELECT ON mini_upwork.Jobs TO 'role_freelancer';
GRANT SELECT, INSERT, UPDATE, DELETE ON mini_upwork.Proposals TO 'role_freelancer';
GRANT SELECT ON mini_upwork.Contracts TO 'role_freelancer';
GRANT SELECT, UPDATE ON mini_upwork.Milestones TO 'role_freelancer';
GRANT SELECT ON mini_upwork.Payments TO 'role_freelancer';
GRANT SELECT, INSERT ON mini_upwork.Reviews TO 'role_freelancer';
GRANT SELECT ON mini_upwork.vw_active_jobs_summary TO 'role_freelancer';
GRANT SELECT ON mini_upwork.vw_contract_payment_progress TO 'role_freelancer';

GRANT SELECT ON mini_upwork.Contracts TO 'role_auditor';
GRANT SELECT ON mini_upwork.Milestones TO 'role_auditor';
GRANT SELECT ON mini_upwork.Payments TO 'role_auditor';
GRANT SELECT ON mini_upwork.Reviews TO 'role_auditor';
GRANT SELECT ON mini_upwork.vw_contract_payment_progress TO 'role_auditor';
GRANT SELECT ON mini_upwork.vw_freelancer_profiles TO 'role_auditor';

REVOKE DELETE ON mini_upwork.Milestones FROM 'role_client';
REVOKE UPDATE ON mini_upwork.Milestones FROM 'role_freelancer';
GRANT UPDATE (Status) ON mini_upwork.Milestones TO 'role_freelancer';

CREATE USER IF NOT EXISTS 'mu_admin'@'localhost'      IDENTIFIED BY 'Admin@MiniUpwork2026!';
CREATE USER IF NOT EXISTS 'mu_client'@'localhost'     IDENTIFIED BY 'Client@MiniUpwork2026!';
CREATE USER IF NOT EXISTS 'mu_freelancer'@'localhost' IDENTIFIED BY 'Freelancer@MiniUpwork2026!';
CREATE USER IF NOT EXISTS 'mu_auditor'@'localhost'    IDENTIFIED BY 'Auditor@MiniUpwork2026!';

GRANT 'role_admin'      TO 'mu_admin'@'localhost';
GRANT 'role_client'     TO 'mu_client'@'localhost';
GRANT 'role_freelancer' TO 'mu_freelancer'@'localhost';
GRANT 'role_auditor'    TO 'mu_auditor'@'localhost';

SET DEFAULT ROLE 'role_admin'      TO 'mu_admin'@'localhost';
SET DEFAULT ROLE 'role_client'     TO 'mu_client'@'localhost';
SET DEFAULT ROLE 'role_freelancer' TO 'mu_freelancer'@'localhost';
SET DEFAULT ROLE 'role_auditor'    TO 'mu_auditor'@'localhost';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'role_client';
SHOW GRANTS FOR 'role_freelancer';
SHOW GRANTS FOR 'role_auditor';
