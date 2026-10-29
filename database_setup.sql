-- =====================================================================
-- DISASTER RELIEF RESOURCE MANAGEMENT SYSTEM (DRRMS)
-- ADBMS Project Database Initialization Script
-- Target Database: DRRMS_DB (MySQL 8.0+)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS DRRMS_DB;
USE DRRMS_DB;

-- Disable foreign key checks for clean teardown/rebuild if needed
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS DISTRIBUTION;
DROP TABLE IF EXISTS REQUEST;
DROP TABLE IF EXISTS RESOURCE;
DROP TABLE IF EXISTS SHELTER;
DROP TABLE IF EXISTS VOLUNTEER;
DROP TABLE IF EXISTS DONOR;
DROP TABLE IF EXISTS DISASTER_EVENT;
DROP VIEW IF EXISTS Shelter_Resource_Summary;
DROP FUNCTION IF EXISTS GetShelterRequestCount;
DROP PROCEDURE IF EXISTS AddDistribution;

SET FOREIGN_KEY_CHECKS = 1;

-- ---------------------------------------------------------------------
-- 1. DISASTER_EVENT TABLE
-- ---------------------------------------------------------------------
CREATE TABLE DISASTER_EVENT (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(40) NOT NULL,
    location VARCHAR(60) NOT NULL,
    start_date DATE NOT NULL,
    severity VARCHAR(15) NOT NULL CHECK (severity IN ('Low', 'Medium', 'High', 'Critical'))
);

-- ---------------------------------------------------------------------
-- 2. DONOR TABLE
-- ---------------------------------------------------------------------
CREATE TABLE DONOR (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_name VARCHAR(60) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(80) NOT NULL UNIQUE,
    donor_type VARCHAR(20) NOT NULL CHECK (donor_type IN ('Individual', 'Corporate', 'NGO', 'Government'))
);

-- ---------------------------------------------------------------------
-- 3. VOLUNTEER TABLE
-- ---------------------------------------------------------------------
CREATE TABLE VOLUNTEER (
    volunteer_id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_name VARCHAR(60) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    skill VARCHAR(40) NOT NULL,
    availability_status VARCHAR(20) NOT NULL DEFAULT 'Available' CHECK (availability_status IN ('Available', 'Deployed', 'On Leave'))
);

-- ---------------------------------------------------------------------
-- 4. SHELTER TABLE
-- ---------------------------------------------------------------------
CREATE TABLE SHELTER (
    shelter_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    location VARCHAR(60) NOT NULL UNIQUE,
    capacity INT NOT NULL CHECK (capacity > 0),
    current_occupancy INT NOT NULL DEFAULT 0 CHECK (current_occupancy >= 0),
    CONSTRAINT fk_shelter_event FOREIGN KEY (event_id) 
        REFERENCES DISASTER_EVENT(event_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- 5. RESOURCE TABLE
-- ---------------------------------------------------------------------
CREATE TABLE RESOURCE (
    resource_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    shelter_id INT NOT NULL,
    resource_type VARCHAR(30) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity >= 0),
    unit VARCHAR(15) NOT NULL,
    CONSTRAINT fk_resource_donor FOREIGN KEY (donor_id) 
        REFERENCES DONOR(donor_id) ON DELETE CASCADE,
    CONSTRAINT fk_resource_shelter FOREIGN KEY (shelter_id) 
        REFERENCES SHELTER(shelter_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- 6. REQUEST TABLE (includes NULL handling for fulfilled_date & remarks)
-- ---------------------------------------------------------------------
CREATE TABLE REQUEST (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    shelter_id INT NOT NULL,
    resource_type VARCHAR(30) NOT NULL,
    quantity_requested DECIMAL(10,2) NOT NULL CHECK (quantity_requested > 0),
    request_status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (request_status IN ('Pending', 'In Progress', 'Fulfilled', 'Cancelled')),
    request_date DATE NOT NULL,
    fulfilled_date DATE NULL,
    remarks VARCHAR(255) NULL,
    CONSTRAINT fk_request_shelter FOREIGN KEY (shelter_id) 
        REFERENCES SHELTER(shelter_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- 7. DISTRIBUTION TABLE
-- ---------------------------------------------------------------------
CREATE TABLE DISTRIBUTION (
    distribution_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    resource_id BIGINT NOT NULL,
    volunteer_id INT NOT NULL,
    distributed_qty DECIMAL(10,2) NOT NULL CHECK (distributed_qty > 0),
    distributed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_dist_resource FOREIGN KEY (resource_id) 
        REFERENCES RESOURCE(resource_id) ON DELETE CASCADE,
    CONSTRAINT fk_dist_volunteer FOREIGN KEY (volunteer_id) 
        REFERENCES VOLUNTEER(volunteer_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- INDEXES FOR QUERY OPTIMIZATION (as highlighted in Phase 3)
-- ---------------------------------------------------------------------
CREATE INDEX idx_resource_shelter ON RESOURCE(shelter_id);
CREATE INDEX idx_request_shelter ON REQUEST(shelter_id);
CREATE INDEX idx_distribution_resource ON DISTRIBUTION(resource_id);

-- ---------------------------------------------------------------------
-- SAMPLE DATA POPULATION (Realistic Disaster Relief Scenario)
-- ---------------------------------------------------------------------

-- Disaster Events
INSERT INTO DISASTER_EVENT (event_id, event_type, location, start_date, severity) VALUES
(1, 'Flood', 'Wayanad River Basin', '2026-07-15', 'Critical'),
(2, 'Cyclone', 'Coastal Nagapattinam', '2026-08-02', 'High'),
(3, 'Landslide', 'Idukki Hill Tracts', '2026-08-20', 'Critical'),
(4, 'Earthquake', 'Chamoli Valley', '2026-09-05', 'High'),
(5, 'Flash Flood', 'Rishikesh Foothills', '2026-09-28', 'Medium');

-- Donors
INSERT INTO DONOR (donor_id, donor_name, phone, email, donor_type) VALUES
(1, 'Red Cross International', '9845012340', 'relief@redcross.org', 'NGO'),
(2, 'Tata Relief Trust', '9821034567', 'aid@tatatrusts.org', 'Corporate'),
(3, 'Ananya Sharma', '9819076543', 'ananya.sharma@gmail.com', 'Individual'),
(4, 'State Disaster Response Fund', '9447011223', 'director@sdrf.gov.in', 'Government'),
(5, 'Care Health NGO', '9744098765', 'contact@carehealth.org', 'NGO'),
(6, 'Infosys Foundation', '9880012345', 'csr@infosys.com', 'Corporate');

-- Volunteers
INSERT INTO VOLUNTEER (volunteer_id, volunteer_name, phone, skill, availability_status) VALUES
(1, 'Arjun Menon', '9847111222', 'Rescue & Evacuation', 'Available'),
(2, 'Dr. Priya Nair', '9847222333', 'Medical Aid', 'Deployed'),
(3, 'Rahul Verma', '9847333444', 'Food Distribution', 'Available'),
(4, 'Deepa Das', '9847444555', 'Logistics & Supply', 'Available'),
(5, 'Kiran George', '9847555666', 'First Aid & Triage', 'Deployed'),
(6, 'Sneha Patel', '9847666777', 'Psychological Counseling', 'On Leave');

-- Shelters
INSERT INTO SHELTER (shelter_id, event_id, location, capacity, current_occupancy) VALUES
(1, 1, 'Meppadi High School Relief Center', 350, 290),
(2, 1, 'Chooralmala Community Hall', 200, 185),
(3, 2, 'Velankanni Cyclone Relief Camp', 500, 310),
(4, 3, 'Munnar Town Hall Shelter', 250, 140),
(5, 4, 'Joshimath Government College Camp', 400, 220),
(6, 5, 'Rishikesh Primary Health Shelter', 150, 85);

-- Resources
INSERT INTO RESOURCE (resource_id, donor_id, shelter_id, resource_type, quantity, unit) VALUES
(1, 1, 1, 'Bottled Drinking Water', 4500.00, 'Litres'),
(2, 2, 1, 'Food Grain Kits', 650.00, 'Packets'),
(3, 5, 1, 'First Aid Kits', 120.00, 'Boxes'),
(4, 3, 2, 'Woolen Blankets', 300.00, 'Units'),
(5, 1, 2, 'Bottled Drinking Water', 2000.00, 'Litres'),
(6, 4, 3, 'Tarpaulin Sheets', 400.00, 'Units'),
(7, 2, 3, 'Dry Ration Kits', 800.00, 'Packets'),
(8, 6, 4, 'Solar Emergency Lanterns', 150.00, 'Units'),
(9, 5, 4, 'Essential Medicines', 250.00, 'Kits'),
(10, 4, 5, 'Family Tents', 80.00, 'Tents'),
(11, 1, 5, 'Bottled Drinking Water', 3200.00, 'Litres'),
(12, 3, 6, 'Baby Food & Formula', 180.00, 'Cans');

-- Requests (includes NULL handling test cases: pending requests have fulfilled_date NULL and optional remarks NULL)
INSERT INTO REQUEST (request_id, shelter_id, resource_type, quantity_requested, request_status, request_date, fulfilled_date, remarks) VALUES
(1, 1, 'Bottled Drinking Water', 1500.00, 'Fulfilled', '2026-07-16', '2026-07-17', 'Delivered by Red Cross batch 1'),
(2, 1, 'First Aid Kits', 50.00, 'Fulfilled', '2026-07-17', '2026-07-18', 'Urgent triage requirement'),
(3, 1, 'Woolen Blankets', 200.00, 'Pending', '2026-07-20', NULL, 'Children and elderly priority'),
(4, 2, 'Food Grain Kits', 300.00, 'In Progress', '2026-07-21', NULL, NULL),
(5, 2, 'Bottled Drinking Water', 800.00, 'Pending', '2026-07-22', NULL, 'Water line contaminated'),
(6, 3, 'Tarpaulin Sheets', 250.00, 'Fulfilled', '2026-08-03', '2026-08-04', 'Roof damage relief'),
(7, 3, 'Dry Ration Kits', 500.00, 'Pending', '2026-08-05', NULL, NULL),
(8, 4, 'Essential Medicines', 100.00, 'Fulfilled', '2026-08-21', '2026-08-22', 'Antiseptics and painkillers'),
(9, 4, 'Solar Emergency Lanterns', 60.00, 'Pending', '2026-08-22', NULL, 'Power outage in valley'),
(10, 5, 'Family Tents', 40.00, 'Pending', '2026-09-06', NULL, 'Displaced families awaiting transit');

-- Distributions
INSERT INTO DISTRIBUTION (distribution_id, resource_id, volunteer_id, distributed_qty, distributed_at) VALUES
(1, 1, 3, 1200.00, '2026-07-17 10:30:00'),
(2, 3, 2, 45.00, '2026-07-18 14:15:00'),
(3, 6, 1, 200.00, '2026-08-04 09:00:00'),
(4, 9, 5, 90.00, '2026-08-22 16:45:00'),
(5, 7, 4, 350.00, '2026-08-06 11:20:00'),
(6, 2, 3, 250.00, '2026-07-19 13:00:00');

-- ---------------------------------------------------------------------
-- PHASE 3: VIEW - Shelter_Resource_Summary
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW Shelter_Resource_Summary AS
SELECT 
    s.shelter_id,
    s.location AS shelter_name,
    e.event_type AS disaster_event,
    e.severity,
    r.resource_id,
    r.resource_type,
    r.quantity AS available_quantity,
    r.unit,
    COALESCE(SUM(d.distributed_qty), 0) AS total_distributed_qty
FROM SHELTER s
JOIN DISASTER_EVENT e ON s.event_id = e.event_id
JOIN RESOURCE r ON s.shelter_id = r.shelter_id
LEFT JOIN DISTRIBUTION d ON r.resource_id = d.resource_id
GROUP BY s.shelter_id, s.location, e.event_type, e.severity, r.resource_id, r.resource_type, r.quantity, r.unit;

-- ---------------------------------------------------------------------
-- PHASE 3: FUNCTION - GetShelterRequestCount(shelter_id)
-- ---------------------------------------------------------------------
DELIMITER //
CREATE FUNCTION GetShelterRequestCount(p_shelter_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count
    FROM REQUEST
    WHERE shelter_id = p_shelter_id;
    RETURN v_count;
END //
DELIMITER ;

-- ---------------------------------------------------------------------
-- PHASE 4: STORED PROCEDURE - AddDistribution(resource_id, volunteer_id, distributed_qty)
-- Includes Transaction, Concurrency lock (FOR UPDATE), Savepoint, Commit & Rollback
-- ---------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE AddDistribution(
    IN p_resource_id BIGINT,
    IN p_volunteer_id INT,
    IN p_distributed_qty DECIMAL(10,2)
)
proc_block: BEGIN
    DECLARE v_avail_qty DECIMAL(10,2);
    DECLARE v_res_count INT;
    DECLARE v_vol_count INT;

    -- Exit handler to rollback if unexpected SQL exception occurs
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    -- Validate distributed quantity
    IF p_distributed_qty <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Distribution quantity must be greater than zero.';
    END IF;

    -- Start ACID Transaction
    START TRANSACTION;

    -- Verify volunteer existence
    SELECT COUNT(*) INTO v_vol_count FROM VOLUNTEER WHERE volunteer_id = p_volunteer_id;
    IF v_vol_count = 0 THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Volunteer ID does not exist in the database.';
    END IF;

    -- Lock the specific RESOURCE row FOR UPDATE to prevent race conditions / concurrent overallocation
    SELECT quantity INTO v_avail_qty
    FROM RESOURCE
    WHERE resource_id = p_resource_id
    FOR UPDATE;

    IF v_avail_qty IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Resource ID does not exist.';
    END IF;

    -- Check availability constraint (Atomicity & Business rule)
    IF v_avail_qty < p_distributed_qty THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient resource quantity! Operation aborted and rolled back to maintain Atomicity.';
    END IF;

    -- Savepoint before writing distribution log
    SAVEPOINT sp_before_distribution;

    -- Step 1: Insert into DISTRIBUTION
    INSERT INTO DISTRIBUTION (resource_id, volunteer_id, distributed_qty, distributed_at)
    VALUES (p_resource_id, p_volunteer_id, p_distributed_qty, NOW());

    -- Savepoint before updating resource inventory
    SAVEPOINT sp_before_resource_deduction;

    -- Step 2: Deduct allocated quantity from inventory
    UPDATE RESOURCE
    SET quantity = quantity - p_distributed_qty
    WHERE resource_id = p_resource_id;

    -- Both operations succeeded: Commit the transaction
    COMMIT;
END //
DELIMITER ;
