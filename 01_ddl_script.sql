DROP DATABASE IF EXISTS mini_upwork;

CREATE DATABASE mini_upwork
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE mini_upwork;

-- SECTION 1: Tao cac bang
CREATE TABLE Users (
    UserID        INT           NOT NULL AUTO_INCREMENT,
    FullName      VARCHAR(255)  NOT NULL,
    Email         VARCHAR(255)  NOT NULL,
    Password      VARCHAR(255)  NOT NULL,
    Role          VARCHAR(20)   NOT NULL,
    AverageRating DECIMAL(3,2)  NULL DEFAULT 0.00,
    CONSTRAINT pk_users PRIMARY KEY (UserID),
    CONSTRAINT uq_users_email UNIQUE (Email),
    CONSTRAINT chk_users_role CHECK (Role IN ('Client', 'Freelancer', 'Admin')),
    CONSTRAINT chk_users_avg_rating CHECK (AverageRating >= 0.00 AND AverageRating <= 5.00)
) ENGINE = InnoDB;

CREATE TABLE Clients (
    ClientID    INT          NOT NULL,
    CompanyName VARCHAR(255) NULL,
    Location    VARCHAR(255) NULL,
    CONSTRAINT pk_clients PRIMARY KEY (ClientID),
    CONSTRAINT fk_clients_user FOREIGN KEY (ClientID)
        REFERENCES Users (UserID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE Freelancers (
    FreelancerID INT          NOT NULL,
    Title        VARCHAR(255) NULL,
    CONSTRAINT pk_freelancers PRIMARY KEY (FreelancerID),
    CONSTRAINT fk_freelancers_user FOREIGN KEY (FreelancerID)
        REFERENCES Users (UserID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE Skills (
    SkillID   INT          NOT NULL AUTO_INCREMENT,
    SkillName VARCHAR(255) NOT NULL,
    CONSTRAINT pk_skills PRIMARY KEY (SkillID),
    CONSTRAINT uq_skills_name UNIQUE (SkillName)
) ENGINE = InnoDB;

CREATE TABLE Freelancer_Skills (
    FreelancerID INT NOT NULL,
    SkillID      INT NOT NULL,
    CONSTRAINT pk_freelancer_skills PRIMARY KEY (FreelancerID, SkillID),
    CONSTRAINT fk_fs_freelancer FOREIGN KEY (FreelancerID)
        REFERENCES Freelancers (FreelancerID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_fs_skill FOREIGN KEY (SkillID)
        REFERENCES Skills (SkillID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE Jobs (
    JobID       INT           NOT NULL AUTO_INCREMENT,
    ClientID    INT           NOT NULL,
    Title       VARCHAR(255)  NOT NULL,
    Description TEXT          NOT NULL,
    Budget      DECIMAL(18,2) NOT NULL,
    Deadline    DATE          NULL,
    Status      VARCHAR(50)   NOT NULL DEFAULT 'Open',
    CONSTRAINT pk_jobs PRIMARY KEY (JobID),
    CONSTRAINT fk_jobs_client FOREIGN KEY (ClientID)
        REFERENCES Clients (ClientID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_jobs_budget CHECK (Budget > 0),
    CONSTRAINT chk_jobs_status CHECK (Status IN ('Open', 'In Progress', 'Closed', 'Cancelled'))
) ENGINE = InnoDB;

CREATE TABLE Proposals (
    ProposalID   INT           NOT NULL AUTO_INCREMENT,
    JobID        INT           NOT NULL,
    FreelancerID INT           NOT NULL,
    BidAmount    DECIMAL(18,2) NOT NULL,
    DeliveryTime VARCHAR(100)  NULL,
    Status       VARCHAR(50)   NOT NULL DEFAULT 'Pending',
    CONSTRAINT pk_proposals PRIMARY KEY (ProposalID),
    CONSTRAINT uq_proposals_job_freelancer UNIQUE (JobID, FreelancerID),
    CONSTRAINT fk_proposals_job FOREIGN KEY (JobID)
        REFERENCES Jobs (JobID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_proposals_freelancer FOREIGN KEY (FreelancerID)
        REFERENCES Freelancers (FreelancerID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_proposals_bid CHECK (BidAmount > 0),
    CONSTRAINT chk_proposals_status CHECK (Status IN ('Pending', 'Accepted', 'Rejected', 'Withdrawn'))
) ENGINE = InnoDB;

CREATE TABLE Contracts (
    ContractID   INT           NOT NULL AUTO_INCREMENT,
    ProposalID   INT           NOT NULL,
    ClientID     INT           NOT NULL,
    FreelancerID INT           NOT NULL,
    Amount       DECIMAL(18,2) NOT NULL,
    StartDate    DATE          NOT NULL,
    EndDate      DATE          NULL,
    Status       VARCHAR(50)   NOT NULL DEFAULT 'Active',
    CONSTRAINT pk_contracts PRIMARY KEY (ContractID),
    CONSTRAINT uq_contracts_proposal UNIQUE (ProposalID),
    CONSTRAINT fk_contracts_proposal FOREIGN KEY (ProposalID)
        REFERENCES Proposals (ProposalID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_contracts_client FOREIGN KEY (ClientID)
        REFERENCES Clients (ClientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_contracts_freelancer FOREIGN KEY (FreelancerID)
        REFERENCES Freelancers (FreelancerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_contracts_amount CHECK (Amount > 0),
    CONSTRAINT chk_contracts_dates CHECK (EndDate IS NULL OR EndDate >= StartDate),
    CONSTRAINT chk_contracts_status CHECK (Status IN ('Active', 'Completed', 'Terminated'))
) ENGINE = InnoDB;

CREATE TABLE Milestones (
    MilestoneID INT           NOT NULL AUTO_INCREMENT,
    ContractID  INT           NOT NULL,
    Title       VARCHAR(255)  NOT NULL,
    Amount      DECIMAL(18,2) NOT NULL,
    DueDate     DATE          NOT NULL,
    Status      VARCHAR(50)   NOT NULL DEFAULT 'Pending',
    CONSTRAINT pk_milestones PRIMARY KEY (MilestoneID),
    CONSTRAINT fk_milestones_contract FOREIGN KEY (ContractID)
        REFERENCES Contracts (ContractID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_milestones_amount CHECK (Amount > 0),
    CONSTRAINT chk_milestones_status CHECK (Status IN ('Pending', 'Active', 'In Review', 'Approved'))
) ENGINE = InnoDB;

CREATE TABLE Payments (
    PaymentID     INT           NOT NULL AUTO_INCREMENT,
    MilestoneID   INT           NOT NULL,
    Amount        DECIMAL(18,2) NOT NULL,
    PaymentMethod VARCHAR(50)   NOT NULL,
    PaidAt        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Status        VARCHAR(50)   NOT NULL DEFAULT 'Pending',
    CONSTRAINT pk_payments PRIMARY KEY (PaymentID),
    CONSTRAINT uq_payments_milestone UNIQUE (MilestoneID),
    CONSTRAINT fk_payments_milestone FOREIGN KEY (MilestoneID)
        REFERENCES Milestones (MilestoneID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_payments_amount CHECK (Amount > 0),
    CONSTRAINT chk_payments_method CHECK (PaymentMethod IN ('Bank Transfer', 'Credit Card', 'E-Wallet', 'PayPal')),
    CONSTRAINT chk_payments_status CHECK (Status IN ('Pending', 'Completed', 'Failed', 'Refunded'))
) ENGINE = InnoDB;

CREATE TABLE Reviews (
    ReviewID   INT       NOT NULL AUTO_INCREMENT,
    ContractID INT       NOT NULL,
    ReviewerID INT       NOT NULL,
    RevieweeID INT       NOT NULL,
    Rating     INT       NOT NULL,
    Comment    TEXT      NULL,
    CreatedAt  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_reviews PRIMARY KEY (ReviewID),
    CONSTRAINT uq_reviews_contract_reviewer UNIQUE (ContractID, ReviewerID),
    CONSTRAINT fk_reviews_contract FOREIGN KEY (ContractID)
        REFERENCES Contracts (ContractID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_reviews_reviewer FOREIGN KEY (ReviewerID)
        REFERENCES Users (UserID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_reviews_reviewee FOREIGN KEY (RevieweeID)
        REFERENCES Users (UserID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_reviews_rating CHECK (Rating BETWEEN 1 AND 5)
) ENGINE = InnoDB;

-- SECTION 2: Chi muc (Indexes)
CREATE INDEX idx_jobs_status_budget ON Jobs (Status, Budget);
CREATE INDEX idx_jobs_client_status ON Jobs (ClientID, Status);
CREATE INDEX idx_proposals_job_status ON Proposals (JobID, Status);
CREATE INDEX idx_contracts_client_status ON Contracts (ClientID, Status);
CREATE INDEX idx_contracts_freelancer_status ON Contracts (FreelancerID, Status);
CREATE INDEX idx_milestones_contract_status ON Milestones (ContractID, Status);
CREATE INDEX idx_payments_status_paidat ON Payments (Status, PaidAt);
CREATE INDEX idx_reviews_reviewee_rating ON Reviews (RevieweeID, Rating);

-- SECTION 3: Views
CREATE VIEW vw_active_jobs_summary AS
SELECT
    j.JobID,
    j.Title AS JobTitle,
    j.Budget,
    j.Deadline,
    j.Status AS JobStatus,
    u.FullName AS ClientName,
    c.CompanyName,
    c.Location,
    COUNT(p.ProposalID) AS TotalProposals
FROM Jobs AS j
INNER JOIN Clients AS c ON j.ClientID = c.ClientID
INNER JOIN Users AS u ON c.ClientID = u.UserID
LEFT JOIN Proposals AS p ON j.JobID = p.JobID
WHERE j.Status = 'Open'
GROUP BY
    j.JobID, j.Title, j.Budget, j.Deadline, j.Status,
    u.FullName, c.CompanyName, c.Location;

CREATE VIEW vw_contract_payment_progress AS
SELECT
    ct.ContractID,
    uc.FullName AS ClientName,
    uf.FullName AS FreelancerName,
    ct.Amount AS ContractAmount,
    ct.Status AS ContractStatus,
    COUNT(m.MilestoneID) AS TotalMilestones,
    SUM(CASE WHEN m.Status = 'Approved' THEN 1 ELSE 0 END) AS ApprovedMilestones,
    COALESCE(SUM(CASE WHEN py.Status = 'Completed' THEN py.Amount ELSE 0 END), 0.00) AS TotalPaidAmount,
    ct.Amount - COALESCE(SUM(CASE WHEN py.Status = 'Completed' THEN py.Amount ELSE 0 END), 0.00) AS RemainingAmount
FROM Contracts AS ct
INNER JOIN Users AS uc ON ct.ClientID = uc.UserID
INNER JOIN Users AS uf ON ct.FreelancerID = uf.UserID
LEFT JOIN Milestones AS m ON ct.ContractID = m.ContractID
LEFT JOIN Payments AS py ON m.MilestoneID = py.MilestoneID
GROUP BY
    ct.ContractID, uc.FullName, uf.FullName, ct.Amount, ct.Status;

CREATE VIEW vw_freelancer_profiles AS
SELECT
    f.FreelancerID,
    u.FullName,
    u.Email,
    f.Title AS ProfessionalTitle,
    u.AverageRating,
    GROUP_CONCAT(DISTINCT s.SkillName ORDER BY s.SkillName SEPARATOR ', ') AS SkillsList,
    COUNT(DISTINCT CASE WHEN ct.Status = 'Completed' THEN ct.ContractID END) AS CompletedContracts
FROM Freelancers AS f
INNER JOIN Users AS u ON f.FreelancerID = u.UserID
LEFT JOIN Freelancer_Skills AS fs ON f.FreelancerID = fs.FreelancerID
LEFT JOIN Skills AS s ON fs.SkillID = s.SkillID
LEFT JOIN Contracts AS ct ON f.FreelancerID = ct.FreelancerID
GROUP BY
    f.FreelancerID, u.FullName, u.Email, f.Title, u.AverageRating;

-- SECTION 4: Triggers
DELIMITER //

CREATE TRIGGER trg_reviews_after_insert
AFTER INSERT ON Reviews
FOR EACH ROW
BEGIN
    UPDATE Users
    SET AverageRating = COALESCE(
        (SELECT ROUND(AVG(Rating), 2)
         FROM Reviews
         WHERE RevieweeID = NEW.RevieweeID),
        0.00
    )
    WHERE UserID = NEW.RevieweeID;
END //

CREATE TRIGGER trg_reviews_after_update
AFTER UPDATE ON Reviews
FOR EACH ROW
BEGIN
    IF OLD.RevieweeID <> NEW.RevieweeID THEN
        UPDATE Users
        SET AverageRating = COALESCE(
            (SELECT ROUND(AVG(Rating), 2)
             FROM Reviews
             WHERE RevieweeID = OLD.RevieweeID),
            0.00
        )
        WHERE UserID = OLD.RevieweeID;
    END IF;

    UPDATE Users
    SET AverageRating = COALESCE(
        (SELECT ROUND(AVG(Rating), 2)
         FROM Reviews
         WHERE RevieweeID = NEW.RevieweeID),
        0.00
    )
    WHERE UserID = NEW.RevieweeID;
END //

CREATE TRIGGER trg_reviews_after_delete
AFTER DELETE ON Reviews
FOR EACH ROW
BEGIN
    UPDATE Users
    SET AverageRating = COALESCE(
        (SELECT ROUND(AVG(Rating), 2)
         FROM Reviews
         WHERE RevieweeID = OLD.RevieweeID),
        0.00
    )
    WHERE UserID = OLD.RevieweeID;
END //

CREATE TRIGGER trg_payments_before_insert
BEFORE INSERT ON Payments
FOR EACH ROW
BEGIN
    DECLARE v_milestone_status VARCHAR(50);
    DECLARE v_milestone_amount DECIMAL(18,2);

    SELECT Status, Amount
    INTO v_milestone_status, v_milestone_amount
    FROM Milestones
    WHERE MilestoneID = NEW.MilestoneID;

    IF v_milestone_status <> 'Approved' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-09): Payment can only be made for an Approved milestone.';
    END IF;

    IF NEW.Amount <> v_milestone_amount THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-09): Payment amount must exactly match the Milestone amount.';
    END IF;
END //

CREATE TRIGGER trg_milestones_before_insert
BEFORE INSERT ON Milestones
FOR EACH ROW
BEGIN
    DECLARE v_contract_amount DECIMAL(18,2);
    DECLARE v_current_total   DECIMAL(18,2);

    SELECT Amount
    INTO v_contract_amount
    FROM Contracts
    WHERE ContractID = NEW.ContractID;

    SELECT COALESCE(SUM(Amount), 0.00)
    INTO v_current_total
    FROM Milestones
    WHERE ContractID = NEW.ContractID;

    IF (v_current_total + NEW.Amount) > v_contract_amount THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-05): Total milestone amount exceeds the Contract amount.';
    END IF;
END //

CREATE TRIGGER trg_reviews_before_insert
BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    DECLARE v_contract_status VARCHAR(50);
    DECLARE v_client_id       INT;
    DECLARE v_freelancer_id   INT;

    IF NEW.ReviewerID = NEW.RevieweeID THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-06): ReviewerID cannot be the same as RevieweeID.';
    END IF;

    SELECT Status, ClientID, FreelancerID
    INTO v_contract_status, v_client_id, v_freelancer_id
    FROM Contracts
    WHERE ContractID = NEW.ContractID;

    IF v_contract_status <> 'Completed' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-07): Reviews can only be submitted for Completed contracts.';
    END IF;

    IF NOT (
        (NEW.ReviewerID = v_client_id AND NEW.RevieweeID = v_freelancer_id)
        OR (NEW.ReviewerID = v_freelancer_id AND NEW.RevieweeID = v_client_id)
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-07): Reviewer and Reviewee must be the Client and Freelancer of the contract.';
    END IF;
END //

CREATE TRIGGER trg_reviews_before_update
BEFORE UPDATE ON Reviews
FOR EACH ROW
BEGIN
    DECLARE v_contract_status VARCHAR(50);
    DECLARE v_client_id       INT;
    DECLARE v_freelancer_id   INT;

    IF NEW.ReviewerID = NEW.RevieweeID THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-06): ReviewerID cannot be the same as RevieweeID.';
    END IF;

    SELECT Status, ClientID, FreelancerID
    INTO v_contract_status, v_client_id, v_freelancer_id
    FROM Contracts
    WHERE ContractID = NEW.ContractID;

    IF v_contract_status <> 'Completed' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-07): Reviews can only belong to Completed contracts.';
    END IF;

    IF NOT (
        (NEW.ReviewerID = v_client_id AND NEW.RevieweeID = v_freelancer_id)
        OR (NEW.ReviewerID = v_freelancer_id AND NEW.RevieweeID = v_client_id)
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Business Rule Violation (BR-07): Reviewer and Reviewee must be the Client and Freelancer of the contract.';
    END IF;
END //

DELIMITER ;
