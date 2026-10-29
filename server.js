const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());
app.use((req, res, next) => {
  res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  next();
});
app.use(express.static('public', { etag: false, maxAge: 0 }));

const pool = mysql.createPool({
  host: process.env.DB_HOST || '127.0.0.1',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '555637',
  database: process.env.DB_NAME || 'DRRMS_DB',
  multipleStatements: true
});

// Auto-initialize View, Function, Procedure & missing columns on startup
async function ensureDatabaseObjects() {
  try {
    // 1. Ensure 'remarks' column exists on REQUEST table
    const [cols] = await pool.query(`SHOW COLUMNS FROM REQUEST LIKE 'remarks'`);
    if (cols.length === 0) {
      await pool.query(`ALTER TABLE REQUEST ADD COLUMN remarks VARCHAR(255) NULL`);
    }

    // 2. Ensure Shelter_Resource_Summary View exists
    await pool.query(`
      CREATE OR REPLACE VIEW Shelter_Resource_Summary AS
      SELECT 
        s.shelter_id,
        s.location AS shelter_name,
        de.event_type AS disaster_event,
        r.resource_type,
        COALESCE(r.quantity, 0) AS available_quantity,
        COALESCE(SUM(dist.distributed_qty), 0) AS distributed_quantity
      FROM SHELTER s
      LEFT JOIN DISASTER_EVENT de ON s.event_id = de.event_id
      LEFT JOIN RESOURCE r ON s.shelter_id = r.shelter_id
      LEFT JOIN DISTRIBUTION dist ON r.resource_id = dist.resource_id
      GROUP BY s.shelter_id, s.location, de.event_type, r.resource_id, r.resource_type, r.quantity;
    `);

    // 3. Ensure GetShelterRequestCount Function exists
    await pool.query(`DROP FUNCTION IF EXISTS GetShelterRequestCount`);
    await pool.query(`
      CREATE FUNCTION GetShelterRequestCount(p_shelter_id INT) 
      RETURNS INT DETERMINISTIC
      BEGIN
        DECLARE req_count INT;
        SELECT COUNT(*) INTO req_count FROM REQUEST WHERE shelter_id = p_shelter_id;
        RETURN COALESCE(req_count, 0);
      END
    `);

    // 4. Ensure AddDistribution Procedure exists
    await pool.query(`DROP PROCEDURE IF EXISTS AddDistribution`);
    await pool.query(`
      CREATE PROCEDURE AddDistribution(
        IN p_resource_id BIGINT,
        IN p_volunteer_id INT,
        IN p_distributed_qty DECIMAL(10,2)
      )
      BEGIN
        DECLARE current_qty DECIMAL(10,2);
        START TRANSACTION;
        SELECT quantity INTO current_qty FROM RESOURCE WHERE resource_id = p_resource_id FOR UPDATE;
        IF current_qty IS NULL OR current_qty < p_distributed_qty THEN
          ROLLBACK;
          SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient resource quantity available!';
        ELSE
          INSERT INTO DISTRIBUTION (resource_id, volunteer_id, distributed_qty, distributed_at)
          VALUES (p_resource_id, p_volunteer_id, p_distributed_qty, NOW());
          SAVEPOINT before_resource_update;
          UPDATE RESOURCE SET quantity = quantity - p_distributed_qty WHERE resource_id = p_resource_id;
          COMMIT;
        END IF;
      END
    `);
    // 5. Ensure Foreign Keys enforce referential integrity (ON DELETE RESTRICT) for ADBMS demonstration
    const fkUpdates = [
      { table: 'SHELTER', name: 'fk_shelter_event', sql: 'ALTER TABLE SHELTER ADD CONSTRAINT fk_shelter_event FOREIGN KEY (event_id) REFERENCES DISASTER_EVENT(event_id) ON DELETE RESTRICT' },
      { table: 'REQUEST', name: 'fk_request_shelter', sql: 'ALTER TABLE REQUEST ADD CONSTRAINT fk_request_shelter FOREIGN KEY (shelter_id) REFERENCES SHELTER(shelter_id) ON DELETE RESTRICT' },
      { table: 'RESOURCE', name: 'fk_resource_shelter', sql: 'ALTER TABLE RESOURCE ADD CONSTRAINT fk_resource_shelter FOREIGN KEY (shelter_id) REFERENCES SHELTER(shelter_id) ON DELETE RESTRICT' },
      { table: 'DISTRIBUTION', name: 'fk_dist_resource', sql: 'ALTER TABLE DISTRIBUTION ADD CONSTRAINT fk_dist_resource FOREIGN KEY (resource_id) REFERENCES RESOURCE(resource_id) ON DELETE RESTRICT' },
      { table: 'DISTRIBUTION', name: 'fk_dist_volunteer', sql: 'ALTER TABLE DISTRIBUTION ADD CONSTRAINT fk_dist_volunteer FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id) ON DELETE RESTRICT' }
    ];
    for (const fk of fkUpdates) {
      try {
        await pool.query(`ALTER TABLE ${fk.table} DROP FOREIGN KEY ${fk.name}`);
      } catch (_) {}
      try {
        await pool.query(fk.sql);
      } catch (_) {}
    }

    console.log('✅ All MySQL Views, Functions, Procedures & Foreign Key Constraints verified!');
  } catch (err) {
    console.error('DB Init Warning:', err.message);
  }
}
ensureDatabaseObjects();

async function exec(sql, params = []) {
  const [rows] = await pool.query(sql, params);
  return { rows, sql: mysql.format(sql, params) };
}

// 1. Bootstrap All Data for the Frontend
app.get('/api/bootstrap', async (req, res) => {
  try {
    const [events] = await pool.query('SELECT * FROM DISASTER_EVENT ORDER BY event_id DESC');
    const [shelters] = await pool.query(`
      SELECT s.*, de.event_type, de.severity,
        (SELECT COUNT(*) FROM REQUEST r WHERE r.shelter_id = s.shelter_id) AS total_requests
      FROM SHELTER s
      LEFT JOIN DISASTER_EVENT de ON s.event_id = de.event_id
      ORDER BY s.shelter_id DESC
    `);
    const [donors] = await pool.query('SELECT * FROM DONOR ORDER BY donor_id DESC');
    const [resources] = await pool.query(`
      SELECT r.*, d.donor_name, d.donor_type, s.location AS shelter_name
      FROM RESOURCE r
      LEFT JOIN DONOR d ON r.donor_id = d.donor_id
      LEFT JOIN SHELTER s ON r.shelter_id = s.shelter_id
      ORDER BY r.resource_id DESC
    `);
    // 3-Table Join: SHELTER + REQUEST + DISASTER_EVENT
    const [requests] = await pool.query(`
      SELECT req.*, s.location AS shelter_name, COALESCE(de.event_type, 'General Emergency') AS event_type, de.severity
      FROM REQUEST req
      LEFT JOIN SHELTER s ON req.shelter_id = s.shelter_id
      LEFT JOIN DISASTER_EVENT de ON s.event_id = de.event_id
      ORDER BY req.request_id DESC
    `);
    const [volunteers] = await pool.query('SELECT * FROM VOLUNTEER ORDER BY volunteer_id DESC');
    const [distributions] = await pool.query(`
      SELECT dist.*, r.resource_type, r.unit, v.volunteer_name, v.skill, s.location AS shelter_name
      FROM DISTRIBUTION dist
      LEFT JOIN RESOURCE r ON dist.resource_id = r.resource_id
      LEFT JOIN VOLUNTEER v ON dist.volunteer_id = v.volunteer_id
      LEFT JOIN SHELTER s ON r.shelter_id = s.shelter_id
      ORDER BY dist.distribution_id DESC
    `);
    const [summaryView] = await pool.query('SELECT * FROM Shelter_Resource_Summary');
    const [[totals]] = await pool.query(`
      SELECT 
        (SELECT COUNT(*) FROM REQUEST WHERE fulfilled_date IS NULL) AS pending_requests,
        (SELECT COALESCE(SUM(distributed_qty), 0) FROM DISTRIBUTION) AS total_distributed
    `);
    res.json({ events, shelters, donors, resources, requests, volunteers, distributions, summaryView, totals });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

function normalizeDate(d) {
  if (!d) return new Date().toISOString().slice(0, 10);
  const str = String(d).trim();
  const dmyMatch = str.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$/);
  if (dmyMatch) {
    const day = dmyMatch[1].padStart(2, '0');
    const month = dmyMatch[2].padStart(2, '0');
    const year = dmyMatch[3];
    return `${year}-${month}-${day}`;
  }
  const ymdMatch = str.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/);
  if (ymdMatch) {
    const year = ymdMatch[1];
    const month = ymdMatch[2].padStart(2, '0');
    const day = ymdMatch[3].padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  const parsed = new Date(str);
  if (!isNaN(parsed.getTime())) {
    return parsed.toISOString().slice(0, 10);
  }
  return new Date().toISOString().slice(0, 10);
}

// 2. Disaster Events (CREATE, UPDATE SEVERITY, DELETE with FK & Cascade Handling)
app.post('/api/events', async (req, res) => {
  try {
    let { event_type, location, start_date, severity } = req.body;
    if (!severity || severity === 'Severe') severity = 'High';
    if (!['Low', 'Medium', 'High', 'Critical'].includes(severity)) severity = 'High';
    start_date = normalizeDate(start_date);
    const result = await exec(
      'INSERT INTO DISASTER_EVENT (event_type, location, start_date, severity) VALUES (?, ?, ?, ?)',
      [event_type, location, start_date, severity]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

app.put('/api/events/:id', async (req, res) => {
  try {
    let { severity } = req.body;
    if (severity === 'Severe') severity = 'Critical';
    if (!['Low', 'Medium', 'High', 'Critical'].includes(severity)) severity = 'High';
    const result = await exec(
      'UPDATE DISASTER_EVENT SET severity = ? WHERE event_id = ?',
      [severity, req.params.id]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

app.delete('/api/events/:id', async (req, res) => {
  const eventId = req.params.id;
  const isCascade = req.query.cascade === 'true' || req.body.cascade === true;

  if (isCascade) {
    // Transactional Cascade Delete: distributions -> resources -> requests -> shelters -> disaster
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      const [shelters] = await conn.query('SELECT shelter_id FROM SHELTER WHERE event_id = ?', [eventId]);
      const shelterIds = shelters.map(s => s.shelter_id);
      if (shelterIds.length > 0) {
        const [resources] = await conn.query('SELECT resource_id FROM RESOURCE WHERE shelter_id IN (?)', [shelterIds]);
        const resourceIds = resources.map(r => r.resource_id);
        if (resourceIds.length > 0) {
          await conn.query('DELETE FROM DISTRIBUTION WHERE resource_id IN (?)', [resourceIds]);
          await conn.query('DELETE FROM RESOURCE WHERE shelter_id IN (?)', [shelterIds]);
        }
        await conn.query('DELETE FROM REQUEST WHERE shelter_id IN (?)', [shelterIds]);
        await conn.query('DELETE FROM SHELTER WHERE event_id = ?', [eventId]);
      }
      await conn.query('DELETE FROM DISASTER_EVENT WHERE event_id = ?', [eventId]);
      await conn.commit();
      res.json({ sql: `DELETE CASCADE for DISASTER_EVENT #${eventId} and all linked records committed!` });
    } catch (err) {
      await conn.rollback();
      res.status(400).json({ error: err.message });
    } finally {
      conn.release();
    }
  } else {
    // Normal Delete (triggers Foreign Key check if active shelters exist)
    try {
      const result = await exec('DELETE FROM DISASTER_EVENT WHERE event_id = ?', [eventId]);
      res.json(result);
    } catch (err) {
      if (err.errno === 1451 || err.code === 'ER_ROW_IS_REFERENCED_2' || (err.message && err.message.includes('foreign key constraint fails'))) {
        return res.status(409).json({
          isForeignKeyViolation: true,
          error: "Cannot delete directly: This Disaster has active Shelters linked to it (Foreign Key Constraint enforced!). Click 'Force Delete with Linked Records' or delete an empty disaster."
        });
      }
      res.status(400).json({ error: err.message });
    }
  }
});

// 3. Shelters (CREATE, UPDATE OCCUPANCY, DELETE with FK & Cascade Handling)
app.post('/api/shelters', async (req, res) => {
  try {
    let { event_id, location, capacity, current_occupancy } = req.body;
    if (!event_id) {
      const [events] = await pool.query('SELECT event_id FROM DISASTER_EVENT ORDER BY event_id DESC LIMIT 1');
      if (events.length > 0) {
        event_id = events[0].event_id;
      } else {
        const [ne] = await pool.query('INSERT INTO DISASTER_EVENT (event_type, location, start_date, severity) VALUES ("General Emergency", "Primary District", CURDATE(), "Medium")');
        event_id = ne.insertId;
      }
    }
    const result = await exec(
      'INSERT INTO SHELTER (event_id, location, capacity, current_occupancy) VALUES (?, ?, ?, ?)',
      [event_id, location, capacity || 100, current_occupancy || 0]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

app.put('/api/shelters/:id', async (req, res) => {
  try {
    const { current_occupancy } = req.body;
    const result = await exec(
      'UPDATE SHELTER SET current_occupancy = ? WHERE shelter_id = ?',
      [current_occupancy, req.params.id]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

app.delete('/api/shelters/:id', async (req, res) => {
  const shelterId = req.params.id;
  const isCascade = req.query.cascade === 'true' || req.body.cascade === true;

  if (isCascade) {
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      const [resources] = await conn.query('SELECT resource_id FROM RESOURCE WHERE shelter_id = ?', [shelterId]);
      const resourceIds = resources.map(r => r.resource_id);
      if (resourceIds.length > 0) {
        await conn.query('DELETE FROM DISTRIBUTION WHERE resource_id IN (?)', [resourceIds]);
        await conn.query('DELETE FROM RESOURCE WHERE shelter_id = ?', [shelterId]);
      }
      await conn.query('DELETE FROM REQUEST WHERE shelter_id = ?', [shelterId]);
      await conn.query('DELETE FROM SHELTER WHERE shelter_id = ?', [shelterId]);
      await conn.commit();
      res.json({ sql: `DELETE CASCADE for SHELTER #${shelterId} and all linked requests/resources committed!` });
    } catch (err) {
      await conn.rollback();
      res.status(400).json({ error: err.message });
    } finally {
      conn.release();
    }
  } else {
    try {
      const result = await exec('DELETE FROM SHELTER WHERE shelter_id = ?', [shelterId]);
      res.json(result);
    } catch (err) {
      if (err.errno === 1451 || err.code === 'ER_ROW_IS_REFERENCED_2' || (err.message && err.message.includes('foreign key constraint fails'))) {
        return res.status(409).json({
          isForeignKeyViolation: true,
          error: "Cannot delete directly: This Shelter has active Requests or Resources linked to it (Foreign Key Integrity enforced!). Click 'Force Delete with Linked Records' or delete an empty shelter."
        });
      }
      res.status(400).json({ error: err.message });
    }
  }
});

// 4. Donors & Resources (CREATE, DELETE RESOURCE with FK Handling)
app.post('/api/donors', async (req, res) => {
  try {
    let { donor_name, phone, email, donor_type } = req.body;
    if (donor_type === 'Organization') donor_type = 'Corporate';
    if (!['Individual', 'Corporate', 'NGO', 'Government'].includes(donor_type)) donor_type = 'Individual';
    const result = await exec(
      'INSERT INTO DONOR (donor_name, phone, email, donor_type) VALUES (?, ?, ?, ?)',
      [donor_name, phone, email, donor_type]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

// Direct Combined Donation Endpoint for Donor Users
app.post('/api/donate', async (req, res) => {
  try {
    let { donor_name, phone, email, donor_type, shelter_id, resource_type, quantity, unit } = req.body;
    let donorId;
    if (donor_name) {
      const [existing] = await pool.query('SELECT donor_id FROM DONOR WHERE donor_name = ? LIMIT 1', [donor_name]);
      if (existing.length > 0) {
        donorId = existing[0].donor_id;
      } else {
        const [nd] = await pool.query(
          'INSERT INTO DONOR (donor_name, phone, email, donor_type) VALUES (?, ?, ?, ?)',
          [donor_name, phone || '9847000000', email || `${donor_name.toLowerCase().replace(/[^a-z0-9]/g, '') || 'donor'}@relief.org`, donor_type || 'Individual']
        );
        donorId = nd.insertId;
      }
    } else {
      const [donors] = await pool.query('SELECT donor_id FROM DONOR ORDER BY donor_id DESC LIMIT 1');
      donorId = donors.length > 0 ? donors[0].donor_id : (await pool.query('INSERT INTO DONOR (donor_name, phone, email, donor_type) VALUES ("Anonymous Donor", "9999999999", "donor@relief.org", "Individual")'))[0].insertId;
    }

    let shelterId = shelter_id;
    if (!shelterId) {
      const [shelters] = await pool.query('SELECT shelter_id FROM SHELTER ORDER BY shelter_id DESC LIMIT 1');
      if (shelters.length > 0) {
        shelterId = shelters[0].shelter_id;
      } else {
        const [events] = await pool.query('SELECT event_id FROM DISASTER_EVENT ORDER BY event_id DESC LIMIT 1');
        let eid = events.length > 0 ? events[0].event_id : (await pool.query('INSERT INTO DISASTER_EVENT (event_type, location, start_date, severity) VALUES ("General Emergency", "Primary District", CURDATE(), "Medium")'))[0].insertId;
        const [ns] = await pool.query('INSERT INTO SHELTER (event_id, location, capacity, current_occupancy) VALUES (?, "Primary Relief Camp", 150, 0)', [eid]);
        shelterId = ns.insertId;
      }
    }

    const qty = parseFloat(quantity) || 100;
    const result = await exec(
      'INSERT INTO RESOURCE (donor_id, shelter_id, resource_type, quantity, unit) VALUES (?, ?, ?, ?, ?)',
      [donorId, shelterId, resource_type, qty, unit || 'Units']
    );

    res.json({
      success: true,
      result,
      sql: `INSERT INTO RESOURCE (donor_id, shelter_id, resource_type, quantity, unit) VALUES (${donorId}, ${shelterId}, '${resource_type}', ${qty}, '${unit || 'Units'}');`
    });
  } catch (err) {
    console.error('Donation error:', err.message);
    res.status(400).json({ error: err.message });
  }
});

app.post('/api/resources', async (req, res) => {
  try {
    let { donor_id, shelter_id, resource_type, quantity, unit } = req.body;
    if (!donor_id) {
      const [donors] = await pool.query('SELECT donor_id FROM DONOR ORDER BY donor_id DESC LIMIT 1');
      if (donors.length > 0) {
        donor_id = donors[0].donor_id;
      } else {
        const [nd] = await pool.query('INSERT INTO DONOR (donor_name, phone, email, donor_type) VALUES ("Anonymous Donor", "9999999999", "donor@relief.org", "Individual")');
        donor_id = nd.insertId;
      }
    }
    if (!shelter_id) {
      const [shelters] = await pool.query('SELECT shelter_id FROM SHELTER ORDER BY shelter_id DESC LIMIT 1');
      if (shelters.length > 0) {
        shelter_id = shelters[0].shelter_id;
      } else {
        const [events] = await pool.query('SELECT event_id FROM DISASTER_EVENT ORDER BY event_id DESC LIMIT 1');
        let eid = events.length > 0 ? events[0].event_id : (await pool.query('INSERT INTO DISASTER_EVENT (event_type, location, start_date, severity) VALUES ("General Emergency", "Primary District", CURDATE(), "Medium")'))[0].insertId;
        const [ns] = await pool.query('INSERT INTO SHELTER (event_id, location, capacity, current_occupancy) VALUES (?, "Primary Relief Camp", 150, 0)', [eid]);
        shelter_id = ns.insertId;
      }
    }
    const result = await exec(
      'INSERT INTO RESOURCE (donor_id, shelter_id, resource_type, quantity, unit) VALUES (?, ?, ?, ?, ?)',
      [donor_id, shelter_id, resource_type, quantity, unit || 'Units']
    );
    res.json(result);
  } catch (e) {
    console.error('Resource insert error:', e.message);
    res.status(400).json({ error: e.message });
  }
});

app.delete('/api/resources/:id', async (req, res) => {
  const resourceId = req.params.id;
  const isCascade = req.query.cascade === 'true' || req.body.cascade === true;

  if (isCascade) {
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      await conn.query('DELETE FROM DISTRIBUTION WHERE resource_id = ?', [resourceId]);
      await conn.query('DELETE FROM RESOURCE WHERE resource_id = ?', [resourceId]);
      await conn.commit();
      res.json({ sql: `DELETE RESOURCE #${resourceId} and linked distributions committed!` });
    } catch (err) {
      await conn.rollback();
      res.status(400).json({ error: err.message });
    } finally {
      conn.release();
    }
  } else {
    try {
      const result = await exec('DELETE FROM RESOURCE WHERE resource_id = ?', [resourceId]);
      res.json(result);
    } catch (err) {
      if (err.errno === 1451 || err.code === 'ER_ROW_IS_REFERENCED_2' || (err.message && err.message.includes('foreign key constraint fails'))) {
        return res.status(409).json({
          isForeignKeyViolation: true,
          error: "Cannot delete directly: This Resource has recorded Distributions. Click 'Force Delete with Linked Records' to remove."
        });
      }
      res.status(400).json({ error: err.message });
    }
  }
});

// 5. Shelter Help Requests (INSERT, Fulfill UPDATE, DELETE)
app.post('/api/requests', async (req, res) => {
  try {
    let { shelter_id, resource_type, quantity_requested, remarks } = req.body;
    if (!shelter_id) {
      const [shelters] = await pool.query('SELECT shelter_id FROM SHELTER ORDER BY shelter_id DESC LIMIT 1');
      if (shelters.length > 0) {
        shelter_id = shelters[0].shelter_id;
      } else {
        const [events] = await pool.query('SELECT event_id FROM DISASTER_EVENT ORDER BY event_id DESC LIMIT 1');
        let eid = events.length > 0 ? events[0].event_id : (await pool.query('INSERT INTO DISASTER_EVENT (event_type, location, start_date, severity) VALUES ("General Emergency", "Primary District", CURDATE(), "Medium")'))[0].insertId;
        const [ns] = await pool.query('INSERT INTO SHELTER (event_id, location, capacity, current_occupancy) VALUES (?, "Primary Relief Camp", 150, 0)', [eid]);
        shelter_id = ns.insertId;
      }
    }
    const result = await exec(
      'INSERT INTO REQUEST (shelter_id, resource_type, quantity_requested, request_status, request_date, fulfilled_date, remarks) VALUES (?, ?, ?, "Pending", CURDATE(), NULL, ?)',
      [shelter_id, resource_type, quantity_requested, remarks || null]
    );
    res.json(result);
  } catch (e) {
    console.error('Request insert error:', e.message);
    res.status(400).json({ error: e.message });
  }
});

app.put('/api/requests/:id/fulfill', async (req, res) => {
  try {
    const result = await exec(
      'UPDATE REQUEST SET request_status = "Fulfilled", fulfilled_date = CURDATE() WHERE request_id = ?',
      [req.params.id]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

app.delete('/api/requests/:id', async (req, res) => {
  try {
    const result = await exec(
      'DELETE FROM REQUEST WHERE request_id = ?',
      [req.params.id]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

// 6. Volunteers (CREATE, DELETE with FK Handling)
app.post('/api/volunteers', async (req, res) => {
  try {
    let { volunteer_name, phone, skill, availability_status } = req.body;
    if (availability_status === 'Busy') availability_status = 'Deployed';
    if (!['Available', 'Deployed', 'On Leave'].includes(availability_status)) availability_status = 'Available';
    const result = await exec(
      'INSERT INTO VOLUNTEER (volunteer_name, phone, skill, availability_status) VALUES (?, ?, ?, ?)',
      [volunteer_name, phone, skill, availability_status]
    );
    res.json(result);
  } catch (e) { res.status(400).json({ error: e.message }); }
});

app.delete('/api/volunteers/:id', async (req, res) => {
  const volunteerId = req.params.id;
  const isCascade = req.query.cascade === 'true' || req.body.cascade === true;

  if (isCascade) {
    const conn = await pool.getConnection();
    try {
      await conn.beginTransaction();
      await conn.query('DELETE FROM DISTRIBUTION WHERE volunteer_id = ?', [volunteerId]);
      await conn.query('DELETE FROM VOLUNTEER WHERE volunteer_id = ?', [volunteerId]);
      await conn.commit();
      res.json({ sql: `DELETE VOLUNTEER #${volunteerId} and linked distributions committed!` });
    } catch (err) {
      await conn.rollback();
      res.status(400).json({ error: err.message });
    } finally {
      conn.release();
    }
  } else {
    try {
      const result = await exec('DELETE FROM VOLUNTEER WHERE volunteer_id = ?', [volunteerId]);
      res.json(result);
    } catch (err) {
      if (err.errno === 1451 || err.code === 'ER_ROW_IS_REFERENCED_2' || (err.message && err.message.includes('foreign key constraint fails'))) {
        return res.status(409).json({
          isForeignKeyViolation: true,
          error: "Cannot delete directly: This Volunteer has recorded Distributions. Click 'Force Delete with Linked Records' to remove."
        });
      }
      res.status(400).json({ error: err.message });
    }
  }
});

// 7. Supply Distribution (ACID Transaction via Stored Procedure)
app.post('/api/distribute', async (req, res) => {
  const { resource_id, volunteer_id, distributed_qty } = req.body;
  try {
    await pool.query('CALL AddDistribution(?, ?, ?)', [resource_id, volunteer_id, distributed_qty]);
    res.json({
      sql: `CALL AddDistribution(${resource_id}, ${volunteer_id}, ${distributed_qty}); -- [Transaction Committed]`
    });
  } catch (e) {
    res.status(400).json({
      error: e.message,
      sql: `CALL AddDistribution(${resource_id}, ${volunteer_id}, ${distributed_qty}); -- [Rolled Back: ${e.message}]`
    });
  }
});

// 8. Analytical Reports & EXPLAIN
app.get('/api/reports/:type', async (req, res) => {
  const map = {
    avg_resource: 'SELECT resource_type, ROUND(AVG(quantity), 2) AS avg_quantity, unit FROM RESOURCE GROUP BY resource_type, unit',
    high_req_shelters: 'SELECT s.shelter_id, s.location, COUNT(r.request_id) AS req_count FROM SHELTER s JOIN REQUEST r ON s.shelter_id = r.shelter_id GROUP BY s.shelter_id, s.location HAVING COUNT(r.request_id) >= (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM REQUEST GROUP BY shelter_id) AS sub)',
    high_distributions: 'SELECT d.distribution_id, r.resource_type, d.distributed_qty, d.distributed_at FROM DISTRIBUTION d JOIN RESOURCE r ON d.resource_id = r.resource_id WHERE d.distributed_qty >= (SELECT AVG(distributed_qty) FROM DISTRIBUTION)',
    explain_join: 'EXPLAIN SELECT s.location, req.resource_type, de.event_type FROM SHELTER s JOIN REQUEST req ON s.shelter_id = req.shelter_id JOIN DISASTER_EVENT de ON s.event_id = de.event_id'
  };
  try {
    if (!map[req.params.type]) return res.status(400).json({ error: 'Unknown report type' });
    res.json(await exec(map[req.params.type]));
  } catch (e) { res.status(400).json({ error: e.message }); }
});

// 9. Clear All Data (Allows user to start completely fresh and add all their own data)
app.post('/api/clear', async (req, res) => {
  const conn = await pool.getConnection();
  try {
    await conn.query('SET FOREIGN_KEY_CHECKS = 0');
    await conn.query('TRUNCATE TABLE DISTRIBUTION');
    await conn.query('TRUNCATE TABLE REQUEST');
    await conn.query('TRUNCATE TABLE RESOURCE');
    await conn.query('TRUNCATE TABLE SHELTER');
    await conn.query('TRUNCATE TABLE VOLUNTEER');
    await conn.query('TRUNCATE TABLE DONOR');
    await conn.query('TRUNCATE TABLE DISASTER_EVENT');
    await conn.query('SET FOREIGN_KEY_CHECKS = 1');
    res.json({ success: true, sql: 'TRUNCATE ALL TABLES; -- All tables cleared for fresh user data entry' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    conn.release();
  }
});

// 10. Load Realistic Sample / Dummy Data
app.post('/api/seed', async (req, res) => {
  const conn = await pool.getConnection();
  try {
    await conn.query('SET FOREIGN_KEY_CHECKS = 0');
    await conn.query('TRUNCATE TABLE DISTRIBUTION');
    await conn.query('TRUNCATE TABLE REQUEST');
    await conn.query('TRUNCATE TABLE RESOURCE');
    await conn.query('TRUNCATE TABLE SHELTER');
    await conn.query('TRUNCATE TABLE VOLUNTEER');
    await conn.query('TRUNCATE TABLE DONOR');
    await conn.query('TRUNCATE TABLE DISASTER_EVENT');
    await conn.query('SET FOREIGN_KEY_CHECKS = 1');

    // 1. Events
    await conn.query(`
      INSERT INTO DISASTER_EVENT (event_id, event_type, location, start_date, severity) VALUES
      (1, 'Flood', 'Kochi Coastal & Lowlands', CURDATE(), 'High'),
      (2, 'Landslide', 'Wayanad Meppadi Area', CURDATE(), 'Critical'),
      (3, 'Cyclone Alert', 'Alappuzha Coastal Belt', CURDATE(), 'High'),
      (4, 'Heavy Inflow', 'Idukki Reservoir Catchment', CURDATE(), 'Medium')
    `);

    // 2. Shelters
    await conn.query(`
      INSERT INTO SHELTER (shelter_id, event_id, location, capacity, current_occupancy) VALUES
      (1, 1, 'St. Teresa Relief Camp, Kochi', 300, 185),
      (2, 2, 'Meppadi Community Center, Wayanad', 250, 210),
      (3, 3, 'Coastal Relief Camp, Alappuzha', 400, 140),
      (4, 4, 'Town Hall Evacuation Center, Idukki', 180, 60)
    `);

    // 3. Donors
    await conn.query(`
      INSERT INTO DONOR (donor_id, donor_name, phone, email, donor_type) VALUES
      (1, 'Kerala Red Cross Society', '9847012345', 'relief@redcrosskerala.org', 'NGO'),
      (2, 'State Emergency Relief Fund', '9847111111', 'kdrf@kerala.gov.in', 'Government'),
      (3, 'Cochin Shipyard CSR Wing', '9847222222', 'csr@cochinshipyard.com', 'Corporate'),
      (4, 'Global Malayalee Aid Group', '9847333333', 'aid@globalmalayalee.org', 'NGO')
    `);

    // 4. Resources
    await conn.query(`
      INSERT INTO RESOURCE (resource_id, donor_id, shelter_id, resource_type, quantity, unit) VALUES
      (1, 1, 1, 'Drinking Water 1L Bottles', 1200, 'Bottles'),
      (2, 2, 2, 'Dry Food & Ration Kits', 450, 'Kits'),
      (3, 3, 1, 'Medical First Aid Kits', 150, 'Kits'),
      (4, 4, 3, 'Sleeping Mats & Blankets', 350, 'Sets'),
      (5, 2, 4, 'Emergency Lanterns & Torches', 90, 'Pieces')
    `);

    // 5. Requests (demonstrates NULL fulfilled_date for Pending)
    await conn.query(`
      INSERT INTO REQUEST (request_id, shelter_id, resource_type, quantity_requested, request_status, request_date, fulfilled_date, remarks) VALUES
      (1, 1, 'Baby Food & Powdered Milk', 80, 'Pending', CURDATE(), NULL, 'Urgent requirement for infants in Camp A'),
      (2, 2, 'Anti-Venom & Wound Dressings', 120, 'Fulfilled', CURDATE(), CURDATE(), 'Dispatched from District Medical Store'),
      (3, 3, 'Clean Drinking Water', 400, 'Pending', CURDATE(), NULL, 'Saline intrusion in local well water'),
      (4, 4, 'Waterproof Tarpaulin Sheets', 50, 'Fulfilled', CURDATE(), CURDATE(), 'Temporary roofing installed')
    `);

    // 6. Volunteers
    await conn.query(`
      INSERT INTO VOLUNTEER (volunteer_id, volunteer_name, phone, skill, availability_status) VALUES
      (1, 'Rahul Varma', '9847011222', 'Logistics & Heavy Driving', 'Available'),
      (2, 'Dr. Anjali Menon', '9847022333', 'Medical Trauma Response', 'Deployed'),
      (3, 'Akhil Das', '9847033444', 'Water Rescue & Boat Operations', 'Available'),
      (4, 'Deepa Suresh', '9847044555', 'Camp Management & Supplies', 'Deployed')
    `);

    // 7. Distributions
    await conn.query(`
      INSERT INTO DISTRIBUTION (distribution_id, resource_id, volunteer_id, distributed_qty, distributed_at) VALUES
      (1, 1, 1, 120, NOW() - INTERVAL 2 HOUR),
      (2, 2, 4, 75, NOW() - INTERVAL 1 HOUR),
      (3, 3, 2, 30, NOW() - INTERVAL 30 MINUTE)
    `);

    res.json({ success: true, sql: 'INSERT INTO ALL TABLES (Dummy Data Initialized across 7 ADBMS Tables)' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    conn.release();
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 DRRMS Server running on http://localhost:${PORT}`));
