# Disaster Relief Resource Management System (DRRMS)
**Advanced Database Management System (ADBMS) Project**

DRRMS is an end-to-end full-stack web application designed for emergency disaster response and relief resource management. It provides complete operational workflows across all ADBMS development phases, backed by a normalized MySQL relational database (`DRRMS_DB`) and a Node.js/Express REST API engine.

---

## 🏗️ System Architecture & ADBMS Phases

### **1. Schema & Relational Modeling (Phase 1)**
All tables adhere strictly to **Boyce-Codd Normal Form (BCNF)** and **3NF**:
* `DISASTER_EVENT` (`event_id` [PK], `event_type`, `location`, `start_date`, `severity`)
* `DONOR` (`donor_id` [PK], `donor_name`, `phone`, `email` [UNIQUE], `donor_type`)
* `VOLUNTEER` (`volunteer_id` [PK], `volunteer_name`, `phone`, `skill`, `availability_status`)
* `SHELTER` (`shelter_id` [PK], `event_id` [FK &rarr; DISASTER_EVENT], `location` [UNIQUE], `capacity`, `current_occupancy`)
* `RESOURCE` (`resource_id` [PK], `donor_id` [FK &rarr; DONOR], `shelter_id` [FK &rarr; SHELTER], `resource_type`, `quantity`, `unit`)
* `REQUEST` (`request_id` [PK], `shelter_id` [FK &rarr; SHELTER], `resource_type`, `quantity_requested`, `request_status`, `request_date`, `fulfilled_date` [NULLable], `remarks`)
* `DISTRIBUTION` (`distribution_id` [PK], `resource_id` [FK &rarr; RESOURCE], `volunteer_id` [FK &rarr; VOLUNTEER], `distributed_qty`, `distributed_at`)

### **2. DML, NULL Value Handling & Aggregation (Phase 2)**
* **NULL Handling:** Pending relief requests maintain `fulfilled_date IS NULL`. Once satisfied, `fulfilled_date` is stamped using `CURDATE()`.
* **Aggregates:**
  - `COUNT()`: Requests raised per shelter.
  - `AVG()`: Average stock quantity per resource category.
  - `SUM()`: Total aid quantity distributed to disaster victims.

### **3. Analytical Reports, Joins, Views & Optimization (Phase 3)**
* **Multi-Table Joins:**
  1. *Donor + Resource Join* (Donation provenance & shelter allocation).
  2. *Shelter + Request + Disaster Event Join* (Relief incident requirements).
  3. *Resource + Distribution + Volunteer Join* (End-to-end dispatch audit trail).
* **Nested Subqueries:**
  - Shelters with request counts exceeding the global average.
  - Distributions whose volume is greater than the overall distribution average.
* **Database View:** `Shelter_Resource_Summary` aggregating shelter status, incident severity, and remaining stock.
* **Deterministic Function:** `GetShelterRequestCount(shelter_id)` returning real-time request counts.
* **Query Optimization:** Real-time `EXPLAIN` query plan inspector highlighting index utilization (`idx_resource_shelter`, `idx_request_shelter`, `idx_distribution_resource`).

### **4. ACID Transactions & Concurrency Control (Phase 4)**
* **Stored Procedure:** `AddDistribution(resource_id, volunteer_id, distributed_qty)`
  - Explicit `START TRANSACTION`.
  - Row-level locking using `SELECT ... FOR UPDATE` on `RESOURCE` to eliminate race conditions and prevent concurrent overallocation.
  - Granular `SAVEPOINT` checkpoints.
  - Atomicity enforcement: If requested volume exceeds available stock, a MySQL exception (`SIGNAL SQLSTATE '45000'`) triggers an immediate `ROLLBACK`, guaranteeing zero partial database writes.
  - Interactive UI demonstrator showing both **Commit** and live **Rollback & Atomicity** proofs.

### **5. Real-Time Emergency Command Center Features**
* **Live Emergency Broadcast Ticker:** High-visibility animated marquee bar scrolling active Critical/High incidents and unfulfilled relief requests in real time.
* **Interactive Disaster Zone Radar / Map View:** Command-center radar grid plotting incidents by severity (`Critical`, `High`, `Medium`) with interactive inspection cards showing shelter bed occupancy gauges, available batches, and pending aid.
* **🚨 "Report New Disaster" Atomic Incident Flow:** Single modal workflow that registers a `DISASTER_EVENT`, establishes a linked `SHELTER`, and creates starter `REQUEST` records in one database transaction, complete with full-screen red emergency flash and synthesized dual-tone siren.
* **⚡ One-Click "Quick Dispatch":** Auto-matches available `RESOURCE` batches and `VOLUNTEER`s for any pending request, pre-fills allocation quantities, executes the ACID stored procedure, and stamps `fulfilled_date = CURDATE()`.
* **Live MySQL Query Logger Dock:** Collapsible bottom drawer displaying syntax-highlighted SQL queries, execution latency (ms), affected rows, and a one-click copy button for presentation and viva demonstrations.
* **Interactive Charts (Chart.js):** Live Bar Chart for Resource Inventory vs. Distributed Aid and Doughnut Chart for Requests Breakdown.

---

## 🚀 Getting Started

### 1. Database Configuration
Open the `.env` file in the project root:
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_root_password_here
DB_NAME=DRRMS_DB
PORT=3000
```
*(Alternatively, you can launch the app and enter your password directly in the **"⚙️ DB Settings"** modal in your browser!)*

### 2. Initializing the Database
You can initialize the schema and populate the test dataset in either of two ways:

#### Option A: One-Click via Web App (Recommended)
1. Launch the server (`npm start` or `node server.js`).
2. Open `http://localhost:3000` in your browser.
3. Click the **"⚡ Initialize Schema"** button in the top navigation bar.

#### Option B: Via MySQL Command Line
```powershell
mysql -u root -p < database_setup.sql
```

### 3. Running the Server
```powershell
npm start
```
The server will be available at: **`http://localhost:3000`**

---

## 📁 Project Structure

```
c:\Users\ivins\Desktop\MCA\ADBMS\
├── database_setup.sql          # Complete DDL, DML, View, Function & Stored Procedure
├── server.js                   # Express REST API backend with MySQL connection pool
├── package.json                # Project dependencies
├── .env                        # Local database credentials
├── .env.example                # Environment variables template
├── public/                     # Frontend Single-Page Application (SPA)
│   ├── index.html              # Modern semantic UI with phase tabs & modals
│   ├── css/style.css           # Glassmorphism dark emergency relief theme
│   └── js/app.js               # Frontend controller & live ACID testing logic
└── README.md                   # Documentation & ADBMS presentation guide
```

---

## 🧪 Demonstration & Viva Guide for ADBMS

1. **Dashboard:** Point out the live KPI indicators and relational architecture.
2. **Phase 1 Tab:** Register a donor, allocate a resource, and raise a relief request.
3. **Phase 2 Tab:** Switch between `IS NULL` and `IS NOT NULL` to show how SQL handles pending vs completed requests. Show the `COUNT()`, `AVG()`, and `SUM()` cards.
4. **Phase 3 Tab:**
   - Toggle through the 3 Join reports.
   - Run the subqueries comparing local metrics against global averages.
   - Select a shelter and execute the stored function `GetShelterRequestCount(shelter_id)`.
   - Inspect the `EXPLAIN` query execution plan and explain the index lookups.
5. **Phase 4 Tab:**
   - Select a resource and volunteer, then click **"Execute Valid Allocation (Commit)"** to prove inventory is atomically updated and logged.
   - Click **"Test Rollback & Atomicity"** to simulate an attempt to allocate more units than available in stock. Show the professor the intercepted `SIGNAL SQLSTATE '45000'` exception and the proof that inventory was not modified!
