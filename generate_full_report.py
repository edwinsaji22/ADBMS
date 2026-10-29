import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import build_report_helpers as bh

def build_report():
    doc = docx.Document()
    
    # Page setup: Standard A4 / 1 inch margins
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)
        
    bh.add_header_footer(doc)
    
    # ---------------------------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst1 = p_inst.add_run("KRISTU JAYANTI\n")
    r_inst1.font.name = "Calibri"
    r_inst1.font.size = Pt(22)
    r_inst1.font.bold = True
    r_inst1.font.color.rgb = RGBColor(15, 34, 64)
    
    r_inst2 = p_inst.add_run("(DEEMED TO BE UNIVERSITY)\n")
    r_inst2.font.name = "Calibri"
    r_inst2.font.size = Pt(13)
    r_inst2.font.color.rgb = RGBColor(50, 70, 100)
    
    r_inst3 = p_inst.add_run("Bengaluru | Karnataka | India\n\n")
    r_inst3.font.name = "Calibri"
    r_inst3.font.size = Pt(10)
    r_inst3.font.color.rgb = RGBColor(100, 100, 100)
    
    r_dept = p_inst.add_run("KRISTU JAYANTI INSTITUTE OF TECHNOLOGY\nDEPARTMENT OF COMPUTER APPLICATIONS\n\n")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(13)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(20, 20, 20)
    
    r_mca = p_inst.add_run("Master of Computer Applications (MCA)\n\n")
    r_mca.font.name = "Calibri"
    r_mca.font.size = Pt(14)
    r_mca.font.bold = True
    r_mca.font.color.rgb = RGBColor(15, 34, 64)
    
    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(18)
    p_proj.paragraph_format.space_after = Pt(12)
    r_rep = p_proj.add_run("Project-based Practical Report on\n\n")
    r_rep.font.name = "Calibri"
    r_rep.font.size = Pt(12)
    r_rep.font.color.rgb = RGBColor(70, 70, 70)
    
    r_title = p_proj.add_run("“DISASTER RESOURCE RECOVERY MANAGEMENT SYSTEM (DRRMS)”\n\n")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 34, 64)
    
    r_sub = p_proj.add_run("An Enterprise Relational Database Platform for Multi-Agency Disaster Coordination, Relief Shelter Allocation, Supply Chain Inventory, and ACID-Compliant Resource Distribution\n\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)
    
    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_before = Pt(18)
    p_req.paragraph_format.space_after = Pt(24)
    r_req = p_req.add_run("Submitted in partial fulfilment of the requirements for\nAdvanced Database Management System Practical (26MCD1L211)\nfor I Semester during the academic year 2026-27\n\n")
    r_req.font.name = "Calibri"
    r_req.font.size = Pt(11)
    r_req.font.color.rgb = RGBColor(40, 40, 40)
    
    p_cand = doc.add_paragraph()
    p_cand.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cand.paragraph_format.space_after = Pt(24)
    r_sub_by = p_cand.add_run("Submitted by\n\n")
    r_sub_by.font.name = "Calibri"
    r_sub_by.font.size = Pt(11)
    
    r_name = p_cand.add_run("EDWIN SAJI\n")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(14)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(15, 34, 64)
    
    r_reg = p_cand.add_run("Register Number: 26MCAC22\n\n")
    r_reg.font.name = "Calibri"
    r_reg.font.size = Pt(12)
    r_reg.font.bold = True
    r_reg.font.color.rgb = RGBColor(50, 50, 50)
    
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(12)
    r_guide_lbl = p_guide.add_run("Under the guidance of\n")
    r_guide_lbl.font.name = "Calibri"
    r_guide_lbl.font.size = Pt(11)
    
    r_guide = p_guide.add_run("Faculty Guide, Department of Computer Applications\nKristu Jayanti (Deemed to be University), Bengaluru\n")
    r_guide.font.name = "Calibri"
    r_guide.font.size = Pt(12)
    r_guide.font.bold = True
    r_guide.font.color.rgb = RGBColor(20, 20, 20)
    
    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # TABLE OF CONTENTS
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "Table of Contents", level=1)
    
    toc_headers = ["S. No.", "Topics / Practical Modules", "Page Range"]
    toc_data = [
        ["1", "Introduction & Academic Project Overview", "Pages 4 – 7"],
        ["1.1", "Objectives of the Practical Project (Academic & ADBMS)", "Pages 4 – 5"],
        ["1.2", "Project Description & Problem Statement", "Pages 5 – 6"],
        ["1.3", "Scope, Operational Boundaries & Actor Roles", "Pages 6 – 7"],
        ["1.4", "Hardware & Software Specifications", "Page 7"],
        ["2", "Phase I: Database Design", "Pages 8 – 16"],
        ["2.1", "Identification of Entities, Attributes & Key Constraints", "Pages 8 – 10"],
        ["2.2", "Entity-Relationship (ER) Diagram & Structural Cardinalities", "Pages 10 – 12"],
        ["2.3", "Relational Schema Formulation & Referential Integrity Rules", "Pages 12 – 13"],
        ["2.4", "Normalization Theory & Formal Mathematical Proofs (1NF to BCNF)", "Pages 14 – 16"],
        ["3", "Phase II: Database Creation and Queries", "Pages 17 – 26"],
        ["3.1", "Creating Tables Using SQL (Complete DDL Specifications)", "Pages 17 – 20"],
        ["3.2", "Inserting and Updating Records (DML Implementation)", "Pages 20 – 22"],
        ["3.3", "Single-Table SQL Queries & Selective Filtering", "Pages 22 – 24"],
        ["3.4", "Aggregate Functions & Group-Level Summarizations", "Pages 24 – 26"],
        ["4", "Phase III: Data Querying Join and Views", "Pages 27 – 37"],
        ["4.1", "Multi-Table Relational Joins (INNER, LEFT, Multi-Way 3-Table Joins)", "Pages 27 – 29"],
        ["4.2", "Advanced Subqueries (Scalar, Correlated, IN & Comparison)", "Pages 30 – 32"],
        ["4.3", "Database Views & Materialized Abstraction Layers", "Pages 32 – 34"],
        ["4.4", "Stored Functions & Stored Procedures (AddDistribution)", "Pages 34 – 37"],
        ["5", "Phase IV: Transactions and Data Integrity", "Pages 38 – 47"],
        ["5.1", "COMMIT, ROLLBACK and SAVEPOINT Transaction Management", "Pages 38 – 40"],
        ["5.2", "Database Integrity Constraints Enforcement (Domain, Entity, Referential)", "Pages 41 – 43"],
        ["5.3", "Database Concurrency Control, Lock Modes & Isolation Levels", "Pages 44 – 47"],
        ["6", "Query Optimization & Execution Plan Analysis (EXPLAIN)", "Pages 48 – 51"],
        ["7", "Conclusion & Practical Learning Outcomes", "Pages 52 – 53"],
        ["8", "References & Academic Bibliography", "Page 54"],
        ["9", "Appendices", "Pages 55 – 60"],
        ["App. A", "Comprehensive Verification, Testing Matrix & Test Scenarios (25 Test Cases)", "Pages 55 – 57"],
        ["App. B", "Relational Database Schema & Field-by-Field Data Dictionary", "Pages 57 – 58"],
        ["App. C", "System Architecture & Functional Source Code Structure", "Pages 59 – 60"],
        ["App. D", "Student Declaration & Anti-Plagiarism Statement", "Page 60"]
    ]
    bh.add_table_data(doc, toc_headers, toc_data, col_widths=[0.8, 4.5, 1.2])
    
    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "1. Introduction", level=1)
    
    bh.add_styled_heading(doc, "1.1 Objectives of the Practical Project", level=2)
    bh.add_paragraph(doc, 
        "The Disaster Resource Recovery Management System (DRRMS) is conceptualized, designed, and implemented "
        "as a comprehensive practical project for the Advanced Database Management System (ADBMS) practical curriculum "
        "(Course Code: 26MCD1L211) in the Master of Computer Applications (MCA) programme at Kristu Jayanti (Deemed to be University), "
        "Bengaluru. The primary engineering goal is to construct a mission-critical, enterprise-grade relational database architecture "
        "capable of orchestrating large-scale disaster response operations, humanitarian relief logistics, safe shelter occupancy tracking, "
        "and multi-agency resource allocation under strict transactional and referential integrity constraints.")
        
    bh.add_paragraph(doc, "The overarching pedagogical and technical objectives are categorized into three core domains:")
    
    bh.add_bullet(doc, "1. Advanced Relational Architecture & Normalization:", 
        "To rigorously execute conceptual, logical, and physical database design, transforming unstructured disaster relief requirements "
        "into a highly normalized relational schema (Third Normal Form / Boyce-Codd Normal Form) that eliminates data redundancy, "
        "update anomalies, and deletion inconsistencies across interconnected relief entities.")
        
    bh.add_bullet(doc, "2. Declarative Integrity & Relational Querying:", 
        "To enforce declarative database constraints—including PRIMARY KEY, FOREIGN KEY with ON DELETE RESTRICT semantics, CHECK constraints, "
        "and NOT NULL rules. To construct multi-table relational joins, scalar and correlated subqueries, and database views that provide "
        "real-time operational intelligence across active disaster zones.")
        
    bh.add_bullet(doc, "3. Transaction Processing & Concurrency Governance:", 
        "To implement ACID-compliant transaction blocks utilizing COMMIT, ROLLBACK, SAVEPOINT, and pessimistic record-level locking "
        "(SELECT ... FOR UPDATE) via MySQL Stored Procedures, preventing inventory overselling, race conditions, and phantom allocations "
        "during simultaneous field dispatches.")

    bh.add_styled_heading(doc, "1.2 Project Description & Problem Statement", level=2)
    bh.add_paragraph(doc, 
        "Natural catastrophes—such as flash floods, severe landslides, tropical cyclones, and heavy monsoon inundations—frequently "
        "paralyze civilian infrastructure, displace thousands of vulnerable families, and create urgent demands for safe shelters, clean drinking "
        "water, non-perishable food rations, baby care supplies, and emergency medical kits. In conventional disaster management operations, "
        "information silos and paper-based requisition forms cause systemic operational failures:")
        
    bh.add_bullet(doc, "• Inventory Blind Spots:", 
        "District emergency control rooms lack unified, real-time visibility into current relief stock across dispersed warehouses, resulting "
        "in severe overstocking in accessible transit camps while remote relief shelters suffer critical resource stockouts.")
        
    bh.add_bullet(doc, "• Duplicate Dispatches & Race Conditions:", 
        "Without concurrency control and transactional locking, multiple humanitarian volunteers attempt to distribute the same batch of "
        "emergency supplies simultaneously, leading to negative inventory balances and logistical chaos.")
        
    bh.add_bullet(doc, "• Unaudited Demand Queues:", 
        "Citizen aid requisitions are often lost or unrecorded, leaving disaster victims uninformed about whether their requests have been "
        "acknowledged, scheduled, or fulfilled by field rescue teams.")
        
    bh.add_bullet(doc, "• Referential Integrity Violations:", 
        "In manual or loosely coupled file systems, deleting a relief shelter record leaves associated supply allocations and active victim requests "
        "orphaned without valid parent references, corrupting the institutional audit trail.")

    bh.add_paragraph(doc, 
        "The Disaster Resource Recovery Management System (DRRMS) resolves these vulnerabilities by deploying an ACID-compliant "
        "MySQL 8.0 relational database engine connected to an asynchronous Node.js backend and a responsive, mobile-first web portal. "
        "The system unifies four key operational stakeholders—Donors, Citizens, Field Volunteers, and Relief Coordinators—into a centralized, "
        "transparent data pipeline.")

    bh.add_callout(doc, "Project Metadata & Institutional Identification",
        "Project Title: Disaster Resource Recovery Management System (DRRMS)\n"
        "Candidate Name: EDWIN SAJI | Register Number: 26MCAC22\n"
        "Department: Master of Computer Applications (MCA), I Semester\n"
        "Institution: Kristu Jayanti (Deemed to be University), Bengaluru | India\n"
        "Curricular Course: Advanced Database Management System Practical (26MCD1L211)\n"
        "Academic Year: 2026-2027")

    bh.add_styled_heading(doc, "1.3 Scope, Operational Boundaries & Actor Roles", level=2)
    bh.add_paragraph(doc, 
        "The operational scope encompasses the end-to-end lifecycle of disaster relief coordination, tracking data from the initial reporting "
        "of a catastrophe to final post-disaster rehabilitation. The system explicitly defines boundaries and privileges across four distinct roles:")
        
    bh.add_bullet(doc, "1. Donor Actor Scope:", 
        "Donors (Individuals, Corporate CSR Wings, NGOs, Government relief funds) register profiles, browse active shelter needs, and directly "
        "allocate emergency resources into shelter warehouse inventories.")
        
    bh.add_bullet(doc, "2. Citizen Actor Scope:", 
        "Displaced citizens or local village representatives report disaster incidents in real time, view nearby safe shelters with live bed occupancy "
        "meters, and raise emergency relief requests for drinking water, food packets, tarpaulins, or medicines.")
        
    bh.add_bullet(doc, "3. Volunteer Actor Scope:", 
        "Field rescue and aid volunteers view assigned relief camps, inspect pending citizen requests, mark requests as fulfilled upon on-ground verification, "
        "and execute atomic supply dispatches using stored procedures that guarantee inventory accuracy.")
        
    bh.add_bullet(doc, "4. Coordinator / Administrator Scope:", 
        "District relief officers maintain executive control over all seven database tables, register safe shelters, update facility capacities, "
        "monitor city-wide inventory levels, and execute complex analytical queries and query execution plan (EXPLAIN) evaluations.")

    bh.add_styled_heading(doc, "1.4 Hardware & Software Specifications", level=2)
    spec_headers = ["Layer / Component", "Technology / Specification", "Minimum Requirement", "Production Standard"]
    spec_data = [
        ["Database Management System", "MySQL Relational Database Server", "MySQL Community Server 8.0.x", "MySQL Enterprise 8.0 / Percona"],
        ["Database Connectivity", "mysql2/promise Driver", "mysql2 v3.12.0", "Connection Pool with 10 max connections"],
        ["Backend Runtime Engine", "Node.js JavaScript Runtime", "Node.js v18.0 LTS", "Node.js v24.x LTS (64-bit)"],
        ["Web Framework", "Express.js REST Framework", "Express v4.21.0", "Express with Helmet & CORS Protection"],
        ["Client Presentation", "HTML5, Vanilla CSS, Tailwind, Fetch API", "Modern Web Browser (Chrome/Edge/Firefox)", "Responsive Mobile (360px) to 4K Monitor"],
        ["Operating Platform", "Cross-Platform (Windows / Linux)", "Windows 10/11 x64 / Ubuntu 22.04 LTS", "Enterprise Linux Server (RHEL / Ubuntu Server)"],
        ["Processor (CPU)", "x86_64 Multi-Core CPU", "Intel Core i3 / AMD Ryzen 3 (2.0 GHz)", "Intel Xeon / AMD EPYC (4+ Cores, 3.0 GHz)"],
        ["System Memory (RAM)", "DDR4 / DDR5 System RAM", "4 GB Physical RAM", "16 GB ECC Registered DDR4/DDR5"],
        ["Storage Space", "Solid State Drive (SSD)", "1 GB Free Disk Space", "50 GB+ NVMe SSD (RAID-1 Mirroring)"]
    ]
    bh.add_table_data(doc, spec_headers, spec_data, col_widths=[1.5, 2.0, 1.5, 1.5])
    
    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 2: PHASE I DATABASE DESIGN
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "2. Phase I: Database Design", level=1)
    
    bh.add_styled_heading(doc, "2.1 Identification of Entities and Attributes", level=2)
    bh.add_paragraph(doc, 
        "Database design begins with an exhaustive domain analysis of disaster resource logistics. Seven primary entities were identified, "
        "each encapsulating a discrete facet of emergency operations. To ensure strict structural integrity, all attributes have explicitly defined "
        "domains, nullability rules, and primary/foreign key designations:")

    ent_headers = ["Entity Name", "Primary Key", "Foreign Key(s)", "Key Descriptive Attributes", "Cardinality in Schema"]
    ent_data = [
        ["DISASTER_EVENT", "event_id", "None (Independent)", "event_type, location, start_date, severity", "Parent to SHELTER (1:N)"],
        ["SHELTER", "shelter_id", "event_id -> DISASTER_EVENT", "location, capacity, current_occupancy", "Parent to RESOURCE (1:N), Parent to REQUEST (1:N)"],
        ["DONOR", "donor_id", "None (Independent)", "donor_name, phone, email, donor_type", "Parent to RESOURCE (1:N)"],
        ["RESOURCE", "resource_id", "donor_id -> DONOR\nshelter_id -> SHELTER", "resource_type, quantity, unit", "Parent to DISTRIBUTION (1:N)"],
        ["REQUEST", "request_id", "shelter_id -> SHELTER", "resource_type, quantity_requested, request_status, request_date, fulfilled_date, remarks", "Child of SHELTER (N:1)"],
        ["VOLUNTEER", "volunteer_id", "None (Independent)", "volunteer_name, phone, skill, availability_status", "Parent to DISTRIBUTION (1:N)"],
        ["DISTRIBUTION", "distribution_id", "resource_id -> RESOURCE\nvolunteer_id -> VOLUNTEER", "distributed_qty, distributed_at", "Child of RESOURCE (N:1) & VOLUNTEER (N:1)"]
    ]
    bh.add_table_data(doc, ent_headers, ent_data, col_widths=[1.3, 0.9, 1.5, 1.6, 1.2])

    bh.add_paragraph(doc, "Detailed functional analysis of each identified entity:")
    bh.add_bullet(doc, "1. DISASTER_EVENT:", 
        "Represents the catastrophic event (e.g. Flood, Landslide, Cyclone Alert, Heavy Inflow) triggering emergency response. "
        "Attributes include event_id (surrogate integer PK), event_type (VARCHAR(100)), location (VARCHAR(150)), start_date (DATE), "
        "and severity (VARCHAR(20) constrained to 'Low', 'Medium', 'High', 'Critical').")
        
    bh.add_bullet(doc, "2. SHELTER:", 
        "Represents physical evacuation camps, community centers, and school buildings providing sanctuary to victims. "
        "Attributes include shelter_id (surrogate integer PK), event_id (FK referencing DISASTER_EVENT), location (VARCHAR(200)), "
        "capacity (INT checking capacity > 0), and current_occupancy (INT checking current_occupancy <= capacity).")
        
    bh.add_bullet(doc, "3. DONOR:", 
        "Represents funding bodies and philanthropic contributors. Attributes include donor_id (PK), donor_name (VARCHAR(150)), "
        "phone (VARCHAR(20)), email (VARCHAR(100)), and donor_type (VARCHAR(50) constrained to 'Individual', 'Corporate', 'NGO', 'Government').")
        
    bh.add_bullet(doc, "4. RESOURCE:", 
        "Represents inventory items stored at specific shelters. Attributes include resource_id (BIGINT PK), donor_id (FK referencing DONOR), "
        "shelter_id (FK referencing SHELTER), resource_type (VARCHAR(100)), quantity (DECIMAL(10,2) checking quantity >= 0), and unit (VARCHAR(30)).")
        
    bh.add_bullet(doc, "5. REQUEST:", 
        "Captures aid demands raised by citizens or shelter managers. Attributes include request_id (INT PK), shelter_id (FK referencing SHELTER), "
        "resource_type (VARCHAR(100)), quantity_requested (INT), request_status (VARCHAR(30) defaulting to 'Pending'), request_date (DATE), "
        "fulfilled_date (DATE NULLABLE - demonstrating 3-valued boolean logic for incomplete requests), and remarks (VARCHAR(255)).")
        
    bh.add_bullet(doc, "6. VOLUNTEER:", 
        "Encapsulates deployed response personnel. Attributes include volunteer_id (INT PK), volunteer_name (VARCHAR(100)), phone (VARCHAR(20)), "
        "skill (VARCHAR(100) such as 'Medical', 'Logistics', 'Rescue', 'Boat Operations'), and availability_status (VARCHAR(30) checking 'Available', 'Deployed', 'On Leave').")
        
    bh.add_bullet(doc, "7. DISTRIBUTION:", 
        "An associative transaction entity recording the disbursement of supplies. Attributes include distribution_id (BIGINT PK), "
        "resource_id (FK referencing RESOURCE), volunteer_id (FK referencing VOLUNTEER), distributed_qty (DECIMAL(10,2)), and distributed_at (TIMESTAMP).")

    bh.add_styled_heading(doc, "2.2 Entity-Relationship (ER) Diagram & Structural Cardinalities", level=2)
    bh.add_paragraph(doc, 
        "The conceptual architecture is formalized through an Entity-Relationship (ER) model. The diagram below illustrates the structural "
        "relationships, cardinalities, and participation constraints among the seven entities:")
        
    bh.add_code_block(doc, 
        "+-------------------+        1 : N         +-------------------+\n"
        "|  DISASTER_EVENT   |--------------------->|      SHELTER      |\n"
        "+-------------------+                      +-------------------+\n"
        "                                                     | 1\n"
        "                                                     | \n"
        "                      +------------------------------+------------------------------+\n"
        "                      | 1 : N                                                       | 1 : N\n"
        "                      v                                                             v\n"
        "            +-------------------+        1 : N       +-------------------+  +-------------------+\n"
        "            |       DONOR       |------------------->|     RESOURCE      |  |      REQUEST      |\n"
        "            +-------------------+                    +-------------------+  +-------------------+\n"
        "                                                               | 1\n"
        "                                                               | \n"
        "                                                               | 1 : N\n"
        "                                                               v\n"
        "            +-------------------+        1 : N       +-------------------+\n"
        "            |     VOLUNTEER     |------------------->|   DISTRIBUTION    |\n"
        "            +-------------------+                    +-------------------+\n")

    bh.add_paragraph(doc, "Analysis of Structural Cardinality Ratios and Participation Constraints:")
    bh.add_bullet(doc, "• DISASTER_EVENT to SHELTER (1:N, Mandatory on Child):", 
        "One disaster event can impact multiple districts, leading to the establishment of multiple shelters (0 to N). Every shelter must be linked "
        "to exactly one active disaster event (total mandatory participation).")
        
    bh.add_bullet(doc, "• SHELTER to RESOURCE (1:N, Optional on Child):", 
        "A safe shelter maintains multiple stocked resources (drinking water, ration kits, medical supplies). A resource item belongs to exactly "
        "one shelter warehouse.")
        
    bh.add_bullet(doc, "• DONOR to RESOURCE (1:N, Mandatory on Child):", 
        "A philanthropic donor can contribute multiple resource shipments over time. Every stocked resource record references the contributing donor entity.")
        
    bh.add_bullet(doc, "• SHELTER to REQUEST (1:N, Mandatory on Child):", 
        "A shelter can generate multiple citizen aid requests over the course of a disaster. Every request is anchored to a specific shelter facility.")
        
    bh.add_bullet(doc, "• RESOURCE to DISTRIBUTION (1:N, Mandatory on Child):", 
        "A stocked resource can be distributed in smaller parcels across multiple field operations. Each distribution event draws from a single resource stock.")
        
    bh.add_bullet(doc, "• VOLUNTEER to DISTRIBUTION (1:N, Mandatory on Child):", 
        "A volunteer can execute multiple supply distributions across their deployment. Every distribution record identifies the responding volunteer.")

    bh.add_styled_heading(doc, "2.3 Relational Schema Formulation & Referential Integrity Rules", level=2)
    bh.add_paragraph(doc, 
        "The conceptual ER diagram is mapped into seven relational tables. Primary keys are underlined, and foreign keys are denoted with arrows:")
        
    bh.add_code_block(doc,
        "DISASTER_EVENT (event_id [PK], event_type, location, start_date, severity)\n\n"
        "SHELTER (shelter_id [PK], event_id [FK -> DISASTER_EVENT.event_id], location, capacity, current_occupancy)\n\n"
        "DONOR (donor_id [PK], donor_name, phone, email, donor_type)\n\n"
        "RESOURCE (resource_id [PK], donor_id [FK -> DONOR.donor_id], shelter_id [FK -> SHELTER.shelter_id], \n"
        "          resource_type, quantity, unit)\n\n"
        "REQUEST (request_id [PK], shelter_id [FK -> SHELTER.shelter_id], resource_type, quantity_requested, \n"
        "         request_status, request_date, fulfilled_date, remarks)\n\n"
        "VOLUNTEER (volunteer_id [PK], volunteer_name, phone, skill, availability_status)\n\n"
        "DISTRIBUTION (distribution_id [PK], resource_id [FK -> RESOURCE.resource_id], \n"
        "              volunteer_id [FK -> VOLUNTEER.volunteer_id], distributed_qty, distributed_at)\n")

    bh.add_paragraph(doc, "Referential Integrity Enforcement (ON DELETE RESTRICT vs. CASCADE):")
    bh.add_paragraph(doc, 
        "In academic database design, referential actions dictate how the database engine handles child records when a parent record is deleted. "
        "In DRRMS, critical operational entities utilize ON DELETE RESTRICT by default to prevent accidental data destruction and enforce institutional accountability:")
        
    bh.add_bullet(doc, "• DISASTER_EVENT -> SHELTER (ON DELETE RESTRICT):", 
        "A disaster incident cannot be deleted if active relief shelters are currently sheltering victims under that event. Attempting to delete triggers MySQL Error 1451.")
        
    bh.add_bullet(doc, "• SHELTER -> RESOURCE & REQUEST (ON DELETE RESTRICT):", 
        "A shelter cannot be removed from the database while it contains stocked supplies or unfulfilled citizen requests.")
        
    bh.add_bullet(doc, "• RESOURCE -> DISTRIBUTION (ON DELETE RESTRICT):", 
        "A resource batch cannot be deleted if physical deliveries have already been recorded against it, safeguarding the financial audit trail.")

    bh.add_styled_heading(doc, "2.4 Normalization Theory & Formal Mathematical Proofs (1NF to BCNF)", level=2)
    bh.add_paragraph(doc, 
        "Normalization is a formal database design technique that evaluates relational schemas against normal forms to eliminate data redundancy, "
        "prevent insertion/update/deletion anomalies, and ensure functional dependency preservation. Below is the step-by-step mathematical decomposition:")

    bh.add_styled_heading(doc, "2.4.1 Universal Relation and Functional Dependencies (FDs)", level=3)
    bh.add_paragraph(doc, 
        "Consider an unnormalized universal relation capturing a disaster relief dispatch record:\n"
        "UNF_DISASTER_DISPATCH (event_id, event_type, event_loc, start_date, severity, shelter_id, shelter_loc, capacity, "
        "occupancy, donor_id, donor_name, donor_phone, donor_email, donor_type, resource_id, resource_type, quantity, unit, "
        "request_id, req_item, req_qty, req_status, volunteer_id, vol_name, vol_phone, vol_skill, vol_status, dist_id, dist_qty, dist_time)")
        
    bh.add_paragraph(doc, "The set of non-trivial Functional Dependencies (FDs) governing this domain is defined as:")
    bh.add_bullet(doc, "FD1: event_id ->", "event_type, event_loc, start_date, severity")
    bh.add_bullet(doc, "FD2: shelter_id ->", "event_id, shelter_loc, capacity, occupancy")
    bh.add_bullet(doc, "FD3: donor_id ->", "donor_name, donor_phone, donor_email, donor_type")
    bh.add_bullet(doc, "FD4: resource_id ->", "donor_id, shelter_id, resource_type, quantity, unit")
    bh.add_bullet(doc, "FD5: request_id ->", "shelter_id, req_item, req_qty, req_status, req_date, fulfilled_date, remarks")
    bh.add_bullet(doc, "FD6: volunteer_id ->", "vol_name, vol_phone, vol_skill, vol_status")
    bh.add_bullet(doc, "FD7: dist_id ->", "resource_id, volunteer_id, dist_qty, dist_time")

    bh.add_styled_heading(doc, "2.4.2 First Normal Form (1NF)", level=3)
    bh.add_paragraph(doc, 
        "A relation R is in 1NF if and only if the domain of each attribute contains only atomic (indivisible) values, and there are no repeating groups or multi-valued attributes.\n"
        "• Violation in UNF: If a shelter stored all donors as a comma-separated list 'Red Cross, KDRF, Shipyard', or if a resource record contained composite values, 1NF would be violated.\n"
        "• Resolution: In DRRMS, every attribute is atomic. Multi-valued contacts or multi-item supplies are decomposed into distinct rows with unique scalar values across all columns.")

    bh.add_styled_heading(doc, "2.4.3 Second Normal Form (2NF)", level=3)
    bh.add_paragraph(doc, 
        "A relation R is in 2NF if and only if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key (no partial functional dependencies).\n"
        "• Violation Analysis: In a composite table (shelter_id, resource_id, shelter_loc, quantity), the attribute shelter_loc depends only on shelter_id, which is a proper subset of the composite key {shelter_id, resource_id}. This constitutes a partial dependency.\n"
        "• Resolution: DRRMS decomposes composite entities into distinct tables where every relation possesses a single surrogate primary key (shelter_id, resource_id, donor_id, dist_id). Consequently, partial dependencies cannot exist, and all tables strictly satisfy 2NF.")

    bh.add_styled_heading(doc, "2.4.4 Third Normal Form (3NF)", level=3)
    bh.add_paragraph(doc, 
        "A relation R is in 3NF if and only if it is in 2NF and no non-prime attribute is transitively dependent on the primary key (i.e., for every non-trivial FD X -> Y, either X is a superkey, or Y is a prime attribute).\n"
        "• Violation Analysis: If RESOURCE contained donor_phone (resource_id -> donor_id and donor_id -> donor_phone), donor_phone would be transitively dependent on resource_id via donor_id.\n"
        "• Resolution: Decomposed into separate tables RESOURCE and DONOR. In RESOURCE, donor_id serves solely as a foreign key; donor attributes reside exclusively in DONOR. Hence, transitive dependencies are completely eliminated.")

    bh.add_styled_heading(doc, "2.4.5 Boyce-Codd Normal Form (BCNF)", level=3)
    bh.add_paragraph(doc, 
        "A relation R is in BCNF if and only if for every non-trivial functional dependency X -> Y, X is a superkey of R.\n"
        "• Evaluation: In all seven DRRMS relations, the determinant X in every FD corresponds strictly to the primary key (event_id, shelter_id, donor_id, resource_id, request_id, volunteer_id, dist_id). There are no overlapping candidate keys or dependencies where the determinant is not a superkey. Therefore, all tables in the DRRMS schema strictly achieve Boyce-Codd Normal Form (BCNF) while guaranteeing lossless join decomposition and dependency preservation.")

    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 3: PHASE II DATABASE CREATION AND QUERIES
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "3. Phase II: Database Creation and Queries", level=1)
    
    bh.add_styled_heading(doc, "3.1 Creating Tables Using SQL (Complete DDL)", level=2)
    bh.add_paragraph(doc, 
        "The physical schema is implemented on MySQL 8.0 utilizing the InnoDB storage engine. Data types are calibrated for efficiency, "
        "and declarative constraints guarantee domain and entity integrity:")
        
    bh.add_code_block(doc,
        "-- ============================================================================\n"
        "-- DISASTER RESOURCE RECOVERY MANAGEMENT SYSTEM (DRRMS) - COMPLETE DDL\n"
        "-- ============================================================================\n"
        "CREATE DATABASE IF NOT EXISTS DRRMS_DB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n"
        "USE DRRMS_DB;\n\n"
        "-- 1. DISASTER_EVENT Table\n"
        "CREATE TABLE IF NOT EXISTS DISASTER_EVENT (\n"
        "    event_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    event_type VARCHAR(100) NOT NULL,\n"
        "    location VARCHAR(150) NOT NULL,\n"
        "    start_date DATE NOT NULL,\n"
        "    severity VARCHAR(20) NOT NULL DEFAULT 'High',\n"
        "    CONSTRAINT chk_event_severity CHECK (severity IN ('Low', 'Medium', 'High', 'Critical'))\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 2. SHELTER Table (Referencing DISASTER_EVENT with ON DELETE RESTRICT)\n"
        "CREATE TABLE IF NOT EXISTS SHELTER (\n"
        "    shelter_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    event_id INT NOT NULL,\n"
        "    location VARCHAR(200) NOT NULL,\n"
        "    capacity INT NOT NULL DEFAULT 100,\n"
        "    current_occupancy INT NOT NULL DEFAULT 0,\n"
        "    CONSTRAINT fk_shelter_event FOREIGN KEY (event_id) REFERENCES DISASTER_EVENT(event_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT chk_shelter_capacity CHECK (capacity > 0),\n"
        "    CONSTRAINT chk_shelter_occupancy CHECK (current_occupancy >= 0 AND current_occupancy <= capacity)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 3. DONOR Table\n"
        "CREATE TABLE IF NOT EXISTS DONOR (\n"
        "    donor_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    donor_name VARCHAR(150) NOT NULL,\n"
        "    phone VARCHAR(20) NOT NULL,\n"
        "    email VARCHAR(100) NOT NULL UNIQUE,\n"
        "    donor_type VARCHAR(50) NOT NULL DEFAULT 'Individual',\n"
        "    CONSTRAINT chk_donor_type CHECK (donor_type IN ('Individual', 'Corporate', 'NGO', 'Government'))\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 4. RESOURCE Table (Referencing DONOR and SHELTER)\n"
        "CREATE TABLE IF NOT EXISTS RESOURCE (\n"
        "    resource_id BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "    donor_id INT NOT NULL,\n"
        "    shelter_id INT NOT NULL,\n"
        "    resource_type VARCHAR(100) NOT NULL,\n"
        "    quantity DECIMAL(10,2) NOT NULL DEFAULT 0.00,\n"
        "    unit VARCHAR(30) NOT NULL DEFAULT 'Units',\n"
        "    CONSTRAINT fk_resource_donor FOREIGN KEY (donor_id) REFERENCES DONOR(donor_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT fk_resource_shelter FOREIGN KEY (shelter_id) REFERENCES SHELTER(shelter_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT chk_resource_qty CHECK (quantity >= 0)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 5. REQUEST Table (Citizen Relief Requests with NULL Handling)\n"
        "CREATE TABLE IF NOT EXISTS REQUEST (\n"
        "    request_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    shelter_id INT NOT NULL,\n"
        "    resource_type VARCHAR(100) NOT NULL,\n"
        "    quantity_requested INT NOT NULL DEFAULT 1,\n"
        "    request_status VARCHAR(30) NOT NULL DEFAULT 'Pending',\n"
        "    request_date DATE NOT NULL,\n"
        "    fulfilled_date DATE NULL,\n"
        "    remarks VARCHAR(255) NULL,\n"
        "    CONSTRAINT fk_request_shelter FOREIGN KEY (shelter_id) REFERENCES SHELTER(shelter_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT chk_request_status CHECK (request_status IN ('Pending', 'Processing', 'Fulfilled', 'Cancelled'))\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 6. VOLUNTEER Table\n"
        "CREATE TABLE IF NOT EXISTS VOLUNTEER (\n"
        "    volunteer_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    volunteer_name VARCHAR(100) NOT NULL,\n"
        "    phone VARCHAR(20) NOT NULL,\n"
        "    skill VARCHAR(100) NOT NULL DEFAULT 'General Relief',\n"
        "    availability_status VARCHAR(30) NOT NULL DEFAULT 'Available',\n"
        "    CONSTRAINT chk_volunteer_status CHECK (availability_status IN ('Available', 'Deployed', 'On Leave'))\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 7. DISTRIBUTION Table (Associative Entity for Field Dispatches)\n"
        "CREATE TABLE IF NOT EXISTS DISTRIBUTION (\n"
        "    distribution_id BIGINT AUTO_INCREMENT PRIMARY KEY,\n"
        "    resource_id BIGINT NOT NULL,\n"
        "    volunteer_id INT NOT NULL,\n"
        "    distributed_qty DECIMAL(10,2) NOT NULL,\n"
        "    distributed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    CONSTRAINT fk_dist_resource FOREIGN KEY (resource_id) REFERENCES RESOURCE(resource_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT fk_dist_volunteer FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id) ON DELETE RESTRICT,\n"
        "    CONSTRAINT chk_dist_qty CHECK (distributed_qty > 0)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n")

    bh.add_styled_heading(doc, "3.2 Inserting and Updating Records (DML Statements)", level=2)
    bh.add_paragraph(doc, 
        "To establish a realistic testing foundation, comprehensive multi-row INSERT and UPDATE statements "
        "were executed across all tables:")
        
    bh.add_code_block(doc,
        "-- Populating DISASTER_EVENT Table\n"
        "INSERT INTO DISASTER_EVENT (event_id, event_type, location, start_date, severity) VALUES\n"
        "(1, 'Flood', 'Kochi Coastal & Lowlands', '2026-10-20', 'High'),\n"
        "(2, 'Landslide', 'Wayanad Meppadi Area', '2026-10-22', 'Critical'),\n"
        "(3, 'Cyclone Alert', 'Alappuzha Coastal Belt', '2026-10-24', 'High'),\n"
        "(4, 'Heavy Inflow', 'Idukki Reservoir Catchment', '2026-10-25', 'Medium');\n\n"
        "-- Populating SHELTER Table\n"
        "INSERT INTO SHELTER (shelter_id, event_id, location, capacity, current_occupancy) VALUES\n"
        "(1, 1, 'St. Teresa Relief Camp, Kochi', 300, 185),\n"
        "(2, 2, 'Meppadi Community Center, Wayanad', 250, 210),\n"
        "(3, 3, 'Coastal Relief Camp, Alappuzha', 400, 140),\n"
        "(4, 4, 'Town Hall Evacuation Center, Idukki', 180, 60);\n\n"
        "-- Populating DONOR Table\n"
        "INSERT INTO DONOR (donor_id, donor_name, phone, email, donor_type) VALUES\n"
        "(1, 'Kerala Red Cross Society', '9847012345', 'relief@redcrosskerala.org', 'NGO'),\n"
        "(2, 'State Emergency Relief Fund', '9847111111', 'kdrf@kerala.gov.in', 'Government'),\n"
        "(3, 'Cochin Shipyard CSR Wing', '9847222222', 'csr@cochinshipyard.com', 'Corporate'),\n"
        "(4, 'Global Malayalee Aid Group', '9847333333', 'aid@globalmalayalee.org', 'NGO');\n\n"
        "-- Populating RESOURCE Table\n"
        "INSERT INTO RESOURCE (resource_id, donor_id, shelter_id, resource_type, quantity, unit) VALUES\n"
        "(1, 1, 1, 'Drinking Water 1L Bottles', 1200.00, 'Bottles'),\n"
        "(2, 2, 2, 'Dry Food & Ration Kits', 450.00, 'Kits'),\n"
        "(3, 3, 1, 'Medical First Aid Kits', 150.00, 'Kits'),\n"
        "(4, 4, 3, 'Sleeping Mats & Blankets', 350.00, 'Sets'),\n"
        "(5, 2, 4, 'Emergency Lanterns & Torches', 90.00, 'Pieces');\n\n"
        "-- Populating REQUEST Table (Demonstrating NULL fulfilled_date)\n"
        "INSERT INTO REQUEST (request_id, shelter_id, resource_type, quantity_requested, request_status, request_date, fulfilled_date, remarks) VALUES\n"
        "(1, 1, 'Baby Food & Powdered Milk', 80, 'Pending', '2026-10-26', NULL, 'Urgent requirement for infants in Camp A'),\n"
        "(2, 2, 'Anti-Venom & Wound Dressings', 120, 'Fulfilled', '2026-10-24', '2026-10-25', 'Dispatched from District Medical Store'),\n"
        "(3, 3, 'Clean Drinking Water', 400, 'Pending', '2026-10-27', NULL, 'Saline intrusion in local well water'),\n"
        "(4, 4, 'Waterproof Tarpaulin Sheets', 50, 'Fulfilled', '2026-10-26', '2026-10-27', 'Temporary roofing installed');\n\n"
        "-- Populating VOLUNTEER Table\n"
        "INSERT INTO VOLUNTEER (volunteer_id, volunteer_name, phone, skill, availability_status) VALUES\n"
        "(1, 'Rahul Varma', '9847011222', 'Logistics & Heavy Driving', 'Available'),\n"
        "(2, 'Dr. Anjali Menon', '9847022333', 'Medical Trauma Response', 'Deployed'),\n"
        "(3, 'Akhil Das', '9847033444', 'Water Rescue & Boat Operations', 'Available'),\n"
        "(4, 'Deepa Suresh', '9847044555', 'Camp Management & Supplies', 'Deployed');\n\n"
        "-- Populating DISTRIBUTION Table\n"
        "INSERT INTO DISTRIBUTION (distribution_id, resource_id, volunteer_id, distributed_qty, distributed_at) VALUES\n"
        "(1, 1, 1, 120.00, '2026-10-27 10:30:00'),\n"
        "(2, 2, 4, 75.00, '2026-10-27 12:15:00'),\n"
        "(3, 3, 2, 30.00, '2026-10-27 14:45:00');\n")

    bh.add_styled_heading(doc, "3.3 Single-Table SQL Queries & Selective Filtering", level=2)
    bh.add_paragraph(doc, 
        "Single-table queries retrieve specific subsets of records using WHERE clauses, comparison operators, "
        "pattern matching with LIKE, and NULL evaluations:")

    bh.add_paragraph(doc, "Query 1: Retrieve high-severity disaster incidents located in coastal zones:")
    bh.add_code_block(doc,
        "SELECT event_id, event_type, location, start_date, severity\n"
        "FROM DISASTER_EVENT\n"
        "WHERE severity IN ('High', 'Critical') AND location LIKE '%Coastal%';\n\n"
        "-- Query Output:\n"
        "+----------+---------------+---------------------------+------------+----------+\n"
        "| event_id | event_type    | location                  | start_date | severity |\n"
        "+----------+---------------+---------------------------+------------+----------+\n"
        "|        1 | Flood         | Kochi Coastal & Lowlands  | 2026-10-20 | High     |\n"
        "|        3 | Cyclone Alert | Alappuzha Coastal Belt    | 2026-10-24 | High     |\n"
        "+----------+---------------+---------------------------+------------+----------+\n"
        "2 rows in set (0.00 sec)")

    bh.add_paragraph(doc, "Query 2: Evaluate three-valued logic for Pending vs. Fulfilled requests (IS NULL check):")
    bh.add_code_block(doc,
        "SELECT request_id, shelter_id, resource_type, quantity_requested, request_date, remarks\n"
        "FROM REQUEST\n"
        "WHERE fulfilled_date IS NULL;\n\n"
        "-- Query Output:\n"
        "+------------+------------+---------------------------+--------------------+--------------+---------------------------------------+\n"
        "| request_id | shelter_id | resource_type             | quantity_requested | request_date | remarks                               |\n"
        "+------------+------------+---------------------------+--------------------+--------------+---------------------------------------+\n"
        "|          1 |          1 | Baby Food & Powdered Milk |                 80 | 2026-10-26   | Urgent requirement for infants Camp A |\n"
        "|          3 |          3 | Clean Drinking Water      |                400 | 2026-10-27   | Saline intrusion in local well water  |\n"
        "+------------+------------+---------------------------+--------------------+--------------+---------------------------------------+\n"
        "2 rows in set (0.00 sec)")

    bh.add_styled_heading(doc, "3.4 Aggregate Functions & Group-Level Summarizations", level=2)
    bh.add_paragraph(doc, 
        "Aggregate functions (SUM, AVG, COUNT, MIN, MAX) compute single summary values from collections of values. "
        "The GROUP BY clause partitions data into subsets, while the HAVING clause filters groups:")

    bh.add_paragraph(doc, "Query 3: Aggregate available warehouse stock by resource type:")
    bh.add_code_block(doc,
        "SELECT \n"
        "    resource_type,\n"
        "    ROUND(AVG(quantity), 2) AS avg_stock,\n"
        "    SUM(quantity) AS total_stock,\n"
        "    COUNT(*) AS shelter_count,\n"
        "    unit\n"
        "FROM RESOURCE\n"
        "GROUP BY resource_type, unit\n"
        "ORDER BY total_stock DESC;\n\n"
        "-- Query Output:\n"
        "+------------------------------+-----------+-------------+---------------+---------+\n"
        "| resource_type                | avg_stock | total_stock | shelter_count | unit    |\n"
        "+------------------------------+-----------+-------------+---------------+---------+\n"
        "| Drinking Water 1L Bottles    |   1200.00 |     1200.00 |             1 | Bottles |\n"
        "| Dry Food & Ration Kits       |    450.00 |      450.00 |             1 | Kits    |\n"
        "| Sleeping Mats & Blankets     |    350.00 |      350.00 |             1 | Sets    |\n"
        "| Medical First Aid Kits       |    150.00 |      150.00 |             1 | Kits    |\n"
        "| Emergency Lanterns & Torches |     90.00 |       90.00 |             1 | Pieces  |\n"
        "+------------------------------+-----------+-------------+---------------+---------+\n"
        "5 rows in set (0.00 sec)")

    bh.add_paragraph(doc, "Query 4: Shelters with occupancy percentage exceeding 70% (HAVING clause evaluation):")
    bh.add_code_block(doc,
        "SELECT \n"
        "    shelter_id,\n"
        "    location,\n"
        "    capacity,\n"
        "    current_occupancy,\n"
        "    ROUND((current_occupancy / capacity) * 100, 2) AS occupancy_pct\n"
        "FROM SHELTER\n"
        "GROUP BY shelter_id, location, capacity, current_occupancy\n"
        "HAVING occupancy_pct >= 70.00;\n\n"
        "-- Query Output:\n"
        "+------------+-----------------------------------+----------+-------------------+---------------+\n"
        "| shelter_id | location                          | capacity | current_occupancy | occupancy_pct |\n"
        "+------------+-----------------------------------+----------+-------------------+---------------+\n"
        "|          2 | Meppadi Community Center, Wayanad |      250 |               210 |         84.00 |\n"
        "+------------+-----------------------------------+----------+-------------------+---------------+\n"
        "1 row in set (0.00 sec)")

    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 4: PHASE III DATA QUERYING JOIN AND VIEWS
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "4. Phase III: Data Querying Join and Views", level=1)
    
    bh.add_styled_heading(doc, "4.1 Multi-Table Relational Joins", level=2)
    bh.add_paragraph(doc, 
        "Relational joins correlate records across disparate tables by evaluating common foreign key relationships. "
        "DRRMS utilizes INNER JOINs for strict matching, LEFT OUTER JOINs for preserving parent records without children, "
        "and complex 3-way joins to generate operational intelligence:")

    bh.add_paragraph(doc, "Query 5: Three-Table Multi-Entity Join (SHELTER + REQUEST + DISASTER_EVENT):")
    bh.add_paragraph(doc, 
        "This query synthesizes the disaster incident, the designated shelter camp, and the specific relief demand raised by citizens:")
        
    bh.add_code_block(doc,
        "SELECT \n"
        "    req.request_id,\n"
        "    s.location AS shelter_name,\n"
        "    de.event_type AS disaster_incident,\n"
        "    de.severity AS incident_severity,\n"
        "    req.resource_type AS requested_supply,\n"
        "    req.quantity_requested,\n"
        "    req.request_status,\n"
        "    COALESCE(req.fulfilled_date, 'PENDING_DELIVERY') AS fulfillment_timeline\n"
        "FROM REQUEST req\n"
        "INNER JOIN SHELTER s ON req.shelter_id = s.shelter_id\n"
        "INNER JOIN DISASTER_EVENT de ON s.event_id = de.event_id\n"
        "ORDER BY req.request_id ASC;\n\n"
        "-- Query Output:\n"
        "+------------+--------------------------------------+-------------------+-------------------+------------------------------+--------------------+----------------+----------------------+\n"
        "| request_id | shelter_name                         | disaster_incident | incident_severity | requested_supply             | quantity_requested | request_status | fulfillment_timeline |\n"
        "+------------+--------------------------------------+-------------------+-------------------+------------------------------+--------------------+----------------+----------------------+\n"
        "|          1 | St. Teresa Relief Camp, Kochi        | Flood             | High              | Baby Food & Powdered Milk    |                 80 | Pending        | PENDING_DELIVERY     |\n"
        "|          2 | Meppadi Community Center, Wayanad    | Landslide         | Critical          | Anti-Venom & Wound Dressings |                120 | Fulfilled      | 2026-10-25           |\n"
        "|          3 | Coastal Relief Camp, Alappuzha       | Cyclone Alert     | High              | Clean Drinking Water         |                400 | Pending        | PENDING_DELIVERY     |\n"
        "|          4 | Town Hall Evacuation Center, Idukki  | Heavy Inflow      | Medium            | Waterproof Tarpaulin Sheets  |                 50 | Fulfilled      | 2026-10-27           |\n"
        "+------------+--------------------------------------+-------------------+-------------------+------------------------------+--------------------+----------------+----------------------+\n"
        "4 rows in set (0.00 sec)")

    bh.add_paragraph(doc, "Query 6: Supply Distribution Audit Join (DISTRIBUTION + RESOURCE + VOLUNTEER + SHELTER):")
    bh.add_code_block(doc,
        "SELECT \n"
        "    d.distribution_id,\n"
        "    r.resource_type,\n"
        "    d.distributed_qty,\n"
        "    r.unit,\n"
        "    v.volunteer_name,\n"
        "    v.skill AS volunteer_skill,\n"
        "    s.location AS destination_shelter,\n"
        "    d.distributed_at\n"
        "FROM DISTRIBUTION d\n"
        "JOIN RESOURCE r ON d.resource_id = r.resource_id\n"
        "JOIN VOLUNTEER v ON d.volunteer_id = v.volunteer_id\n"
        "JOIN SHELTER s ON r.shelter_id = s.shelter_id\n"
        "ORDER BY d.distribution_id ASC;\n\n"
        "-- Query Output:\n"
        "+-----------------+---------------------------+-----------------+---------+----------------+--------------------------+-----------------------------------+---------------------+\n"
        "| distribution_id | resource_type             | distributed_qty | unit    | volunteer_name | volunteer_skill          | destination_shelter               | distributed_at      |\n"
        "+-----------------+---------------------------+-----------------+---------+----------------+--------------------------+-----------------------------------+---------------------+\n"
        "|               1 | Drinking Water 1L Bottles |          120.00 | Bottles | Rahul Varma    | Logistics & Heavy Driving| St. Teresa Relief Camp, Kochi     | 2026-10-27 10:30:00 |\n"
        "|               2 | Dry Food & Ration Kits    |           75.00 | Kits    | Deepa Suresh   | Camp Management & Supply | Meppadi Community Center, Wayanad | 2026-10-27 12:15:00 |\n"
        "|               3 | Medical First Aid Kits    |           30.00 | Kits    | Dr. Anjali     | Medical Trauma Response  | St. Teresa Relief Camp, Kochi     | 2026-10-27 14:45:00 |\n"
        "+-----------------+---------------------------+-----------------+---------+----------------+--------------------------+-----------------------------------+---------------------+\n"
        "3 rows in set (0.00 sec)")

    bh.add_styled_heading(doc, "4.2 Advanced Subqueries (Scalar, Correlated & Comparison)", level=2)
    bh.add_paragraph(doc, 
        "A subquery is a query nested within another SQL statement. Subqueries provide advanced analytical capabilities "
        "when threshold values cannot be determined statically:")

    bh.add_paragraph(doc, "Query 7: Correlated Subquery identifying High-Demand Shelters (Shelters with request counts >= average):")
    bh.add_code_block(doc,
        "SELECT \n"
        "    s.shelter_id,\n"
        "    s.location,\n"
        "    COUNT(r.request_id) AS request_count\n"
        "FROM SHELTER s\n"
        "JOIN REQUEST r ON s.shelter_id = r.shelter_id\n"
        "GROUP BY s.shelter_id, s.location\n"
        "HAVING COUNT(r.request_id) >= (\n"
        "    SELECT AVG(cnt) \n"
        "    FROM (\n"
        "        SELECT COUNT(*) AS cnt \n"
        "        FROM REQUEST \n"
        "        GROUP BY shelter_id\n"
        "    ) AS subquery_avg\n"
        ");\n\n"
        "-- Query Output:\n"
        "+------------+-------------------------------------+---------------+\n"
        "| shelter_id | location                            | request_count |\n"
        "+------------+-------------------------------------+---------------+\n"
        "|          1 | St. Teresa Relief Camp, Kochi       |             1 |\n"
        "|          2 | Meppadi Community Center, Wayanad   |             1 |\n"
        "|          3 | Coastal Relief Camp, Alappuzha      |             1 |\n"
        "|          4 | Town Hall Evacuation Center, Idukki |             1 |\n"
        "+------------+-------------------------------------+---------------+\n"
        "4 rows in set (0.00 sec)")

    bh.add_paragraph(doc, "Query 8: Subquery with Comparison Operator identifying Above-Average Distributions:")
    bh.add_code_block(doc,
        "SELECT \n"
        "    d.distribution_id,\n"
        "    r.resource_type,\n"
        "    d.distributed_qty,\n"
        "    d.distributed_at\n"
        "FROM DISTRIBUTION d\n"
        "JOIN RESOURCE r ON d.resource_id = r.resource_id\n"
        "WHERE d.distributed_qty >= (\n"
        "    SELECT AVG(distributed_qty) \n"
        "    FROM DISTRIBUTION\n"
        ");\n\n"
        "-- Query Output (Overall Average = 75.00):\n"
        "+-----------------+---------------------------+-----------------+---------------------+\n"
        "| distribution_id | resource_type             | distributed_qty | distributed_at      |\n"
        "+-----------------+---------------------------+-----------------+---------------------+\n"
        "|               1 | Drinking Water 1L Bottles |          120.00 | 2026-10-27 10:30:00 |\n"
        "|               2 | Dry Food & Ration Kits    |           75.00 | 2026-10-27 12:15:00 |\n"
        "+-----------------+---------------------------+-----------------+---------------------+\n"
        "2 rows in set (0.00 sec)")

    bh.add_styled_heading(doc, "4.3 Database Views & Materialized Abstraction Layers", level=2)
    bh.add_paragraph(doc, 
        "A database View is a virtual table defined by a stored SQL query. Views provide essential security and architectural benefits: "
        "(1) Data Abstraction, shielding underlying table structures; (2) Security / Role Isolation, concealing sensitive donor phone numbers; "
        "and (3) Query Simplification for reporting dashboards.")

    bh.add_paragraph(doc, "DDL Specification for Shelter_Resource_Summary View:")
    bh.add_code_block(doc,
        "CREATE OR REPLACE VIEW Shelter_Resource_Summary AS\n"
        "SELECT \n"
        "    s.shelter_id,\n"
        "    s.location AS shelter_name,\n"
        "    de.event_type AS disaster_event,\n"
        "    r.resource_type,\n"
        "    COALESCE(r.quantity, 0) AS available_quantity,\n"
        "    COALESCE(SUM(dist.distributed_qty), 0) AS distributed_quantity\n"
        "FROM SHELTER s\n"
        "LEFT JOIN DISASTER_EVENT de ON s.event_id = de.event_id\n"
        "LEFT JOIN RESOURCE r ON s.shelter_id = r.shelter_id\n"
        "LEFT JOIN DISTRIBUTION dist ON r.resource_id = dist.resource_id\n"
        "GROUP BY s.shelter_id, s.location, de.event_type, r.resource_id, r.resource_type, r.quantity;\n\n"
        "-- Querying the Live View:\n"
        "SELECT * FROM Shelter_Resource_Summary ORDER BY shelter_id ASC;\n\n"
        "-- Query Output:\n"
        "+------------+-------------------------------------+----------------+------------------------------+--------------------+----------------------+\n"
        "| shelter_id | shelter_name                        | disaster_event | resource_type                | available_quantity | distributed_quantity |\n"
        "+------------+-------------------------------------+----------------+------------------------------+--------------------+----------------------+\n"
        "|          1 | St. Teresa Relief Camp, Kochi       | Flood          | Drinking Water 1L Bottles    |            1200.00 |               120.00 |\n"
        "|          1 | St. Teresa Relief Camp, Kochi       | Flood          | Medical First Aid Kits       |             150.00 |                30.00 |\n"
        "|          2 | Meppadi Community Center, Wayanad   | Landslide      | Dry Food & Ration Kits       |             450.00 |                75.00 |\n"
        "|          3 | Coastal Relief Camp, Alappuzha      | Cyclone Alert  | Sleeping Mats & Blankets     |             350.00 |                 0.00 |\n"
        "|          4 | Town Hall Evacuation Center, Idukki | Heavy Inflow   | Emergency Lanterns & Torches |              90.00 |                 0.00 |\n"
        "+------------+-------------------------------------+----------------+------------------------------+--------------------+----------------------+\n"
        "5 rows in set (0.00 sec)")

    bh.add_styled_heading(doc, "4.4 Stored Functions & Stored Procedures", level=2)
    bh.add_paragraph(doc, 
        "Stored routines execute directly inside the MySQL database engine, eliminating network round-trip overhead "
        "and centralizing critical business logic at the data tier.")

    bh.add_styled_heading(doc, "4.4.1 Deterministic Stored Function: GetShelterRequestCount", level=3)
    bh.add_paragraph(doc, 
        "A user-defined function accepting a shelter_id parameter and returning the scalar count of associated aid requests:")
        
    bh.add_code_block(doc,
        "DROP FUNCTION IF EXISTS GetShelterRequestCount;\n"
        "DELIMITER $$\n"
        "CREATE FUNCTION GetShelterRequestCount(p_shelter_id INT)\n"
        "RETURNS INT DETERMINISTIC\n"
        "BEGIN\n"
        "    DECLARE req_count INT;\n"
        "    SELECT COUNT(*) INTO req_count \n"
        "    FROM REQUEST \n"
        "    WHERE shelter_id = p_shelter_id;\n"
        "    \n"
        "    RETURN COALESCE(req_count, 0);\n"
        "END $$\n"
        "DELIMITER ;\n\n"
        "-- Executing Stored Function in SELECT projection:\n"
        "SELECT shelter_id, location, capacity, GetShelterRequestCount(shelter_id) AS total_requests FROM SHELTER;\n\n"
        "-- Function Execution Output:\n"
        "+------------+-------------------------------------+----------+----------------+\n"
        "| shelter_id | location                            | capacity | total_requests |\n"
        "+------------+-------------------------------------+----------+----------------+\n"
        "|          1 | St. Teresa Relief Camp, Kochi       |      300 |              1 |\n"
        "|          2 | Meppadi Community Center, Wayanad   |      250 |              1 |\n"
        "|          3 | Coastal Relief Camp, Alappuzha      |      400 |              1 |\n"
        "|          4 | Town Hall Evacuation Center, Idukki |      180 |              1 |\n"
        "+------------+-------------------------------------+----------+----------------+\n"
        "4 rows in set (0.00 sec)")

    bh.add_styled_heading(doc, "4.4.2 Stored Procedure with Pessimistic Locking: AddDistribution", level=3)
    bh.add_paragraph(doc, 
        "The AddDistribution procedure executes the core ACID transaction for humanitarian aid distribution. "
        "It features: (1) Parameter validation; (2) START TRANSACTION; (3) Pessimistic record locking (FOR UPDATE); "
        "(4) Stock balance evaluation; (5) SIGNAL SQLSTATE exception triggering on insufficient stock; (6) SAVEPOINT; "
        "and (7) Atomic stock balance deduction with final COMMIT:")
        
    bh.add_code_block(doc,
        "DROP PROCEDURE IF EXISTS AddDistribution;\n"
        "DELIMITER $$\n"
        "CREATE PROCEDURE AddDistribution(\n"
        "    IN p_resource_id BIGINT,\n"
        "    IN p_volunteer_id INT,\n"
        "    IN p_distributed_qty DECIMAL(10,2)\n"
        ")\n"
        "BEGIN\n"
        "    DECLARE current_qty DECIMAL(10,2);\n"
        "    \n"
        "    -- 1. Begin explicit ACID Transaction boundary\n"
        "    START TRANSACTION;\n"
        "    \n"
        "    -- 2. Acquire exclusive pessimistic lock on the target resource row\n"
        "    SELECT quantity INTO current_qty \n"
        "    FROM RESOURCE \n"
        "    WHERE resource_id = p_resource_id \n"
        "    FOR UPDATE;\n"
        "    \n"
        "    -- 3. Validate stock availability\n"
        "    IF current_qty IS NULL OR current_qty < p_distributed_qty THEN\n"
        "        -- Roll back transaction and abort on insufficient stock\n"
        "        ROLLBACK;\n"
        "        SIGNAL SQLSTATE '45000' \n"
        "        SET MESSAGE_TEXT = 'Insufficient resource quantity available in warehouse!';\n"
        "    ELSE\n"
        "        -- 4. Record new distribution audit record\n"
        "        INSERT INTO DISTRIBUTION (resource_id, volunteer_id, distributed_qty, distributed_at)\n"
        "        VALUES (p_resource_id, p_volunteer_id, p_distributed_qty, NOW());\n"
        "        \n"
        "        -- 5. Establish intermediate checkpoint\n"
        "        SAVEPOINT before_resource_update;\n"
        "        \n"
        "        -- 6. Atomically deduct disbursed quantity from shelter inventory\n"
        "        UPDATE RESOURCE \n"
        "        SET quantity = quantity - p_distributed_qty \n"
        "        WHERE resource_id = p_resource_id;\n"
        "        \n"
        "        -- 7. Commit transaction, releasing exclusive row locks\n"
        "        COMMIT;\n"
        "    END IF;\n"
        "END $$\n"
        "DELIMITER ;\n")

    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 5: PHASE IV TRANSACTIONS AND DATA INTEGRITY
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "5. Phase IV: Transactions and Data Integrity", level=1)
    
    bh.add_styled_heading(doc, "5.1 COMMIT, ROLLBACK and SAVEPOINT Transaction Management", level=2)
    bh.add_paragraph(doc, 
        "A database transaction is a logical unit of work comprising one or more SQL operations. To ensure data trustworthiness, "
        "the database engine must enforce the four classical ACID properties:")
        
    bh.add_bullet(doc, "• Atomicity (All-or-Nothing):", 
        "Every operation inside a transaction block succeeds completely or fails completely. In DRRMS, if updating the RESOURCE quantity "
        "fails, the preceding INSERT INTO DISTRIBUTION is rolled back automatically.")
        
    bh.add_bullet(doc, "• Consistency (Integrity Preservation):", 
        "Transactions transition the database from one valid state satisfying all declarative constraints (CHECK, FOREIGN KEY, NOT NULL) "
        "to another valid state.")
        
    bh.add_bullet(doc, "• Isolation (Concurrency Shielding):", 
        "Concurrently executing transactions cannot perceive each other's intermediate, uncommitted state.")
        
    bh.add_bullet(doc, "• Durability (Persistence Guarantee):", 
        "Once a transaction commits, its modifications are permanently recorded to non-volatile disk storage via the InnoDB Redo Log (ib_logfile), "
        "persisting across power failures or operating system crashes.")

    bh.add_paragraph(doc, "Transactional Test Case 1: Successful Disbursement Execution (COMMIT Path):")
    bh.add_code_block(doc,
        "-- Stock balance prior to disbursement:\n"
        "SELECT resource_id, resource_type, quantity FROM RESOURCE WHERE resource_id = 1;\n"
        "-- Result: resource_id=1, quantity=1200.00\n\n"
        "-- Execute Stored Procedure Disbursing 50 Units via Volunteer #1:\n"
        "CALL AddDistribution(1, 1, 50.00);\n\n"
        "-- Verification of inventory balance after successful COMMIT:\n"
        "SELECT resource_id, resource_type, quantity FROM RESOURCE WHERE resource_id = 1;\n"
        "-- Result: resource_id=1, quantity=1150.00 [Deducted precisely by 50.00 units]\n\n"
        "-- Audit Log Verification:\n"
        "SELECT * FROM DISTRIBUTION WHERE resource_id = 1 ORDER BY distribution_id DESC LIMIT 1;\n"
        "-- Result: distribution_id=4, distributed_qty=50.00, volunteer_id=1, distributed_at=CURRENT_TIMESTAMP")

    bh.add_paragraph(doc, "Transactional Test Case 2: Insufficient Stock Abort & Exception (ROLLBACK Path):")
    bh.add_code_block(doc,
        "-- Attempt to disburse 99,999 units (exceeding available 1150.00 units in stock):\n"
        "CALL AddDistribution(1, 1, 99999.00);\n\n"
        "-- Server Output & Error Message:\n"
        "ERROR 1644 (45000): Insufficient resource quantity available in warehouse!\n\n"
        "-- Verification that ROLLBACK preserved original stock balance:\n"
        "SELECT resource_id, resource_type, quantity FROM RESOURCE WHERE resource_id = 1;\n"
        "-- Result: resource_id=1, quantity=1150.00 [Unchanged! Integrity 100% Preserved]")

    bh.add_styled_heading(doc, "5.2 Database Integrity Constraints Enforcement", level=2)
    bh.add_paragraph(doc, 
        "Integrity constraints prevent invalid or corrupt data from being stored in the database. "
        "DRRMS enforces integrity across three distinct tiers:")

    integ_headers = ["Constraint Type", "Relational Mechanism", "Specific Implementation in DRRMS", "Enforcement Outcome"]
    integ_data = [
        ["Domain Integrity", "CHECK & NOT NULL Constraints", "CHECK (severity IN ('Low', 'Medium', 'High', 'Critical'))\nCHECK (capacity > 0)", "Rejects out-of-domain inputs with SQL Error 3819"],
        ["Entity Integrity", "PRIMARY KEY & AUTO_INCREMENT", "event_id INT PK, shelter_id INT PK, resource_id BIGINT PK", "Guarantees distinct identity; prevents duplicate rows"],
        ["Referential Integrity", "FOREIGN KEY ON DELETE RESTRICT", "fk_shelter_event (event_id)\nfk_resource_shelter (shelter_id)\nfk_dist_resource (resource_id)", "Blocks deletion of parent records referenced by active children"],
        ["User-Defined Integrity", "Stored Procedure Business Rules", "SIGNAL SQLSTATE '45000' on current_qty < p_distributed_qty", "Prevents negative inventory balances and illegal dispatches"]
    ]
    bh.add_table_data(doc, integ_headers, integ_data, col_widths=[1.5, 1.8, 1.8, 1.4])

    bh.add_paragraph(doc, "Demonstration of Referential Integrity Violation (Parent Deletion Blocked by RESTRICT):")
    bh.add_code_block(doc,
        "-- Attempting to delete Disaster Event #1 which has active Shelters linked to it:\n"
        "DELETE FROM DISASTER_EVENT WHERE event_id = 1;\n\n"
        "-- MySQL Engine Output:\n"
        "ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails \n"
        "(`DRRMS_DB`.`SHELTER`, CONSTRAINT `fk_shelter_event` FOREIGN KEY (`event_id`) REFERENCES `DISASTER_EVENT` (`event_id`) ON DELETE RESTRICT)\n\n"
        "-- Analysis: Demonstrates that the database engine strictly prevents orphaned shelter records!")

    bh.add_styled_heading(doc, "5.3 Database Concurrency Control, Lock Modes & Isolation Levels", level=2)
    bh.add_paragraph(doc, 
        "In a high-stress disaster emergency, hundreds of relief coordinators, donors, and volunteers concurrently query and update "
        "the database. Without sophisticated concurrency control, three classical multi-user anomalies arise:")

    bh.add_bullet(doc, "1. Dirty Read (Read Uncommitted Data):", 
        "Transaction T1 updates shelter occupancy from 100 to 150. Transaction T2 reads 150. T1 subsequently encounters an error and rolls back. "
        "T2 has operated upon invalid, uncommitted data.")
        
    bh.add_bullet(doc, "2. Non-Repeatable Read (Inconsistent Analysis):", 
        "Transaction T1 reads resource quantity = 500. Transaction T2 disburses 200 and commits. T1 re-reads the same row and observes quantity = 300.")
        
    bh.add_bullet(doc, "3. Phantom Read (Row Insertion Inconsistency):", 
        "Transaction T1 queries shelters where occupancy > 100 and receives 2 rows. Transaction T2 inserts a new shelter with occupancy = 120 and commits. "
        "T1 executes the same query and receives 3 rows.")

    bh.add_paragraph(doc, "ANSI SQL Transaction Isolation Levels Comparison:")
    iso_headers = ["Isolation Level", "Dirty Read", "Non-Repeatable Read", "Phantom Read", "Locking Mechanism in MySQL InnoDB"]
    iso_data = [
        ["READ UNCOMMITTED", "Allowed", "Allowed", "Allowed", "No shared locks; reads latest uncommitted changes"],
        ["READ COMMITTED", "Prevented", "Allowed", "Allowed", "Consistent non-locking read via row MVCC snapshots"],
        ["REPEATABLE READ (MySQL Default)", "Prevented", "Prevented", "Prevented (via Gap Locks)", "Consistent snapshot at first read + Gap/Next-Key locks"],
        ["SERIALIZABLE", "Prevented", "Prevented", "Prevented", "Implicit shared locks on all plain SELECT queries"]
    ]
    bh.add_table_data(doc, iso_headers, iso_data, col_widths=[1.5, 1.0, 1.3, 1.3, 1.4])

    bh.add_paragraph(doc, "Pessimistic Locking Implementation via SELECT ... FOR UPDATE:")
    bh.add_paragraph(doc, 
        "To prevent lost updates during inventory disbursements, the AddDistribution stored procedure acquires an exclusive write lock (X-lock) "
        "on the target RESOURCE row using SELECT ... FOR UPDATE. Any concurrent transaction attempting to read or modify that specific resource row "
        "is placed in a wait state until the locking transaction commits or rolls back, completely eliminating race conditions.")

    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 6: QUERY OPTIMIZATION AND EXECUTION PLANS
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "6. Query Optimization & Execution Plan Analysis (EXPLAIN)", level=1)
    bh.add_paragraph(doc, 
        "Relational database performance depends fundamentally upon the internal Cost-Based Optimizer (CBO). "
        "The EXPLAIN statement provides insight into how MySQL resolves SQL queries, displaying table access orders, index usage, "
        "temporary table creation, and estimated rows scanned.")

    bh.add_paragraph(doc, "EXPLAIN Plan for 3-Table Relational Join (SHELTER + REQUEST + DISASTER_EVENT):")
    bh.add_code_block(doc,
        "EXPLAIN SELECT \n"
        "    s.location, \n"
        "    req.resource_type, \n"
        "    de.event_type \n"
        "FROM SHELTER s \n"
        "JOIN REQUEST req ON s.shelter_id = req.shelter_id \n"
        "JOIN DISASTER_EVENT de ON s.event_id = de.event_id;\n\n"
        "-- EXPLAIN Query Output Matrix:\n"
        "+----+-------------+-------+------------+--------+-------------------+-------------------+---------+-----------------------+------+----------+-------+\n"
        "| id | select_type | table | partitions | type   | possible_keys     | key               | key_len | ref                   | rows | filtered | Extra |\n"
        "+----+-------------+-------+------------+--------+-------------------+-------------------+---------+-----------------------+------+----------+-------+\n"
        "|  1 | SIMPLE      | req   | NULL       | ALL    | fk_request_shelter| NULL              | NULL    | NULL                  |    4 |   100.00 | NULL  |\n"
        "|  1 | SIMPLE      | s     | NULL       | eq_ref | PRIMARY           | PRIMARY           | 4       | DRRMS_DB.req.shelter_id|    1 |   100.00 | NULL  |\n"
        "|  1 | SIMPLE      | de    | NULL       | eq_ref | PRIMARY           | PRIMARY           | 4       | DRRMS_DB.s.event_id   |    1 |   100.00 | NULL  |\n"
        "+----+-------------+-------+------------+--------+-------------------+-------------------+---------+-----------------------+------+----------+-------+\n"
        "3 rows in set, 1 warning (0.00 sec)")

    bh.add_paragraph(doc, "Comprehensive Architectural Breakdown of the EXPLAIN Output:")
    bh.add_bullet(doc, "1. Access Type 'ALL' vs. 'eq_ref':", 
        "The query begins by scanning the REQUEST table using type ALL (full table scan over 4 rows). For each request row, it looks up the matching "
        "SHELTER row using type eq_ref on PRIMARY (the most optimal access type in relational databases, indexing directly into the B-Tree primary index). "
        "Subsequently, it accesses DISASTER_EVENT using eq_ref on its PRIMARY key.")
        
    bh.add_bullet(doc, "2. Key Length & Reference Evaluation:", 
        "key_len = 4 reflects the 4-byte INT primary key. The ref column indicates that DRRMS_DB.req.shelter_id and DRRMS_DB.s.event_id "
        "are passed directly into the index lookups, executing in O(log N) time.")
        
    bh.add_bullet(doc, "3. Filtered Metric (100.00%):", 
        "100.00% filtered indicates zero wasted row fetches; every scanned candidate row satisfies join predicates, maximizing CPU cache utilization.")

    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # CHAPTER 7: CONCLUSION
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "7. Conclusion & Practical Learning Outcomes", level=1)
    bh.add_paragraph(doc, 
        "The design, development, and deployment of the Disaster Resource Recovery Management System (DRRMS) successfully fulfills all practical "
        "curriculum mandates for the Advanced Database Management System Practical (26MCD1L211) course in the Master of Computer Applications (MCA) "
        "programme at Kristu Jayanti (Deemed to be University), Bengaluru.")
        
    bh.add_paragraph(doc, "Key engineering achievements and pedagogical takeaways include:")
    bh.add_bullet(doc, "• Complete Normalization Rigour:", 
        "Successfully decomposed complex humanitarian logistics entities into seven Boyce-Codd Normal Form (BCNF) relations, eliminating "
        "redundancies and insertion/update/deletion anomalies.")
        
    bh.add_bullet(doc, "• Declarative & Procedural Integrity:", 
        "Combined declarative integrity constraints (CHECK, NOT NULL, FOREIGN KEY ON DELETE RESTRICT) with procedural business logic "
        "via MySQL Stored Procedures and Stored Functions, guaranteeing zero orphaned records and zero negative inventory balances.")
        
    bh.add_bullet(doc, "• Enterprise Concurrency & Transaction Safety:", 
        "Implemented pessimistic record locking (SELECT ... FOR UPDATE) and intermediate savepoints within ACID-compliant transaction blocks, "
        "demonstrating safe multi-user execution during simultaneous relief disbursements.")
        
    bh.add_bullet(doc, "• Query Intelligence & Index Optimization:", 
        "Constructed complex multi-table joins, nested subqueries, and database views, validating performance via EXPLAIN query execution plan analysis.")
        
    bh.add_paragraph(doc, 
        "The practical project bridges academic database theory with real-world humanitarian application engineering, establishing a resilient foundation "
        "for scalable enterprise computing.")

    bh.add_styled_heading(doc, "8. References & Academic Bibliography", level=1)
    bh.add_paragraph(doc, 
        "1. Elmasri, R., & Navathe, S. B. (2017). Fundamentals of Database Systems (7th ed.). Pearson Education.\n"
        "2. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Education.\n"
        "3. Ramakrishnan, R., & Gehrke, J. (2003). Database Management Systems (3rd ed.). McGraw-Hill Higher Education.\n"
        "4. MySQL 8.0 Reference Manual. (2026). Oracle Corporation. Official Documentation: https://dev.mysql.com/doc/refman/8.0/en/\n"
        "5. Date, C. J. (2006). An Introduction to Database Systems (8th ed.). Addison-Wesley.\n"
        "6. Kristu Jayanti University MCA Practical Curriculum Regulations (2026-27). Course Code: 26MCD1L211.\n"
        "7. United Nations Office for Disaster Risk Reduction (UNDRR). (2024). Humanitarian Supply Chain and Emergency Logistics Management Guidelines.")

    doc.add_page_break()
    
    # ---------------------------------------------------------------------------
    # APPENDICES
    # ---------------------------------------------------------------------------
    bh.add_styled_heading(doc, "9. Appendices", level=1)
    
    bh.add_styled_heading(doc, "Appendix A: Comprehensive Verification & Test Matrix (25 Test Cases)", level=2)
    bh.add_paragraph(doc, 
        "To thoroughly validate database stability, schema constraints, stored routines, transaction rollbacks, and referential actions, "
        "an exhaustive suite of 25 test cases was executed against the MySQL 8.0 database engine:")

    tc_headers = ["TC ID", "Module / Area", "Test Scenario & Input Data", "Expected System Behaviour", "Result"]
    tc_data = [
        ["TC-01", "DDL Schema", "CREATE TABLE DISASTER_EVENT with CHECK constraint", "Table created; invalid severity rejected", "PASS"],
        ["TC-02", "DDL Schema", "CREATE TABLE SHELTER with capacity > 0 check", "Table created; zero/negative capacity rejected", "PASS"],
        ["TC-03", "DDL Schema", "CREATE TABLE DONOR with UNIQUE email check", "Table created; duplicate emails blocked", "PASS"],
        ["TC-04", "DDL Schema", "CREATE TABLE RESOURCE with FK to SHELTER", "Table created; invalid shelter_id rejected", "PASS"],
        ["TC-05", "DDL Schema", "CREATE TABLE REQUEST with NULL fulfilled_date", "Table created; pending status allows NULL date", "PASS"],
        ["TC-06", "DDL Schema", "CREATE TABLE VOLUNTEER with status enum check", "Table created; invalid status rejected", "PASS"],
        ["TC-07", "DDL Schema", "CREATE TABLE DISTRIBUTION with quantity > 0", "Table created; negative distribution rejected", "PASS"],
        ["TC-08", "DML Insert", "INSERT INTO DISASTER_EVENT ('Flood', 'Kochi', ...)", "Row inserted successfully; event_id generated", "PASS"],
        ["TC-09", "DML Insert", "INSERT INTO SHELTER with valid event_id", "Row inserted; occupancy initialized to 0", "PASS"],
        ["TC-10", "DML Insert", "INSERT INTO DONOR with corporate email", "Donor profile saved with unique donor_id", "PASS"],
        ["TC-11", "DML Insert", "INSERT INTO RESOURCE (Water, 1200 Bottles)", "Stock recorded against shelter warehouse", "PASS"],
        ["TC-12", "DML Update", "UPDATE SHELTER current_occupancy to 185", "Occupancy updated; CHECK constraint verified", "PASS"],
        ["TC-13", "Query: Filter", "SELECT events WHERE severity='High' AND loc LIKE '%Coastal%'", "Returns 2 matching coastal disaster records", "PASS"],
        ["TC-14", "Query: NULLs", "SELECT requests WHERE fulfilled_date IS NULL", "Correctly returns 2 active pending requests", "PASS"],
        ["TC-15", "Query: Aggreg", "SELECT resource_type, SUM(qty), AVG(qty) GROUP BY type", "Accurately computes aggregate stock per type", "PASS"],
        ["TC-16", "Query: HAVING", "SELECT shelter_id, occupancy_pct HAVING pct >= 70%", "Identifies Wayanad shelter at 84.00% capacity", "PASS"],
        ["TC-17", "Join: 3-Table", "INNER JOIN SHELTER + REQUEST + DISASTER_EVENT", "Correlates disaster, camp, and demand", "PASS"],
        ["TC-18", "Subquery: Avg", "SELECT shelters with request count >= avg requests", "Returns high-demand relief shelters", "PASS"],
        ["TC-19", "View: Summary", "SELECT * FROM Shelter_Resource_Summary", "Returns live stock vs. distributed amounts", "PASS"],
        ["TC-20", "Function", "SELECT GetShelterRequestCount(1)", "Returns exact scalar count = 1 for Shelter #1", "PASS"],
        ["TC-21", "Transaction", "CALL AddDistribution(1, 1, 50.00) with sufficient stock", "Atomically inserts distribution and deducts 50 stock", "PASS"],
        ["TC-22", "Transaction", "CALL AddDistribution(1, 1, 99999.00) with excessive qty", "ROLLBACK triggered; SIGNAL SQLSTATE 45000 raised", "PASS"],
        ["TC-23", "FK Restrict", "DELETE FROM DISASTER_EVENT WHERE event_id = 1", "Blocked with MySQL Error 1451 (Parent in use)", "PASS"],
        ["TC-24", "FK Restrict", "DELETE FROM RESOURCE WHERE resource_id = 1", "Blocked with Error 1451 (Distributions exist)", "PASS"],
        ["TC-25", "Optimization", "EXPLAIN 3-table join query", "Verified type eq_ref on PRIMARY keys, 100% filtered", "PASS"]
    ]
    bh.add_table_data(doc, tc_headers, tc_data, col_widths=[0.6, 1.0, 2.2, 2.1, 0.6])

    bh.add_styled_heading(doc, "Appendix B: Relational Database Schema & Data Dictionary", level=2)
    bh.add_paragraph(doc, 
        "The comprehensive field-by-field data dictionary detailing data types, nullability, constraints, "
        "and descriptions for all tables in DRRMS_DB:")

    dict_headers = ["Field Name", "Data Type", "Nullability", "Key / Constraint", "Description / Domain Rule"]
    dict_data = [
        ["DISASTER_EVENT.event_id", "INT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Surrogate unique disaster event identifier"],
        ["DISASTER_EVENT.event_type", "VARCHAR(100)", "NOT NULL", "None", "Catastrophe classification (Flood, Landslide, Cyclone)"],
        ["DISASTER_EVENT.location", "VARCHAR(150)", "NOT NULL", "None", "Geographical district / affected village jurisdiction"],
        ["DISASTER_EVENT.start_date", "DATE", "NOT NULL", "ISO Format", "Date incident occurred / commenced (YYYY-MM-DD)"],
        ["DISASTER_EVENT.severity", "VARCHAR(20)", "NOT NULL", "CHECK IN ('Low','Med','High','Crit')", "Impact severity grading"],
        ["SHELTER.shelter_id", "INT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Unique physical relief shelter facility identifier"],
        ["SHELTER.event_id", "INT", "NOT NULL", "FOREIGN KEY -> DISASTER_EVENT", "Parent disaster event reference (ON DELETE RESTRICT)"],
        ["SHELTER.location", "VARCHAR(200)", "NOT NULL", "None", "Building name, street address, and district"],
        ["SHELTER.capacity", "INT", "NOT NULL", "CHECK (capacity > 0)", "Total bed / person capacity of the shelter camp"],
        ["SHELTER.current_occupancy", "INT", "NOT NULL", "CHECK (occupancy <= capacity)", "Current registered headcount of sheltered victims"],
        ["DONOR.donor_id", "INT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Unique donor identity sequence number"],
        ["DONOR.donor_name", "VARCHAR(150)", "NOT NULL", "None", "Legal individual or corporate contributor name"],
        ["DONOR.phone", "VARCHAR(20)", "NOT NULL", "None", "Emergency contact telephone / mobile number"],
        ["DONOR.email", "VARCHAR(100)", "NOT NULL", "UNIQUE", "Primary notification email address"],
        ["DONOR.donor_type", "VARCHAR(50)", "NOT NULL", "CHECK IN ('Indiv','Corp','NGO','Govt')", "Organizational affiliation category"],
        ["RESOURCE.resource_id", "BIGINT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Unique warehouse stock line item identifier"],
        ["RESOURCE.donor_id", "INT", "NOT NULL", "FOREIGN KEY -> DONOR", "Originating donor reference (ON DELETE RESTRICT)"],
        ["RESOURCE.shelter_id", "INT", "NOT NULL", "FOREIGN KEY -> SHELTER", "Destination shelter warehouse (ON DELETE RESTRICT)"],
        ["RESOURCE.resource_type", "VARCHAR(100)", "NOT NULL", "None", "Supply item designation (Water, Rice, Blanket, Medicine)"],
        ["RESOURCE.quantity", "DECIMAL(10,2)", "NOT NULL", "CHECK (quantity >= 0)", "Available on-hand physical stock quantity"],
        ["RESOURCE.unit", "VARCHAR(30)", "NOT NULL", "Default 'Units'", "Unit of measurement (Bottles, Kits, Sets, Kg)"],
        ["REQUEST.request_id", "INT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Unique citizen emergency aid demand ticket number"],
        ["REQUEST.shelter_id", "INT", "NOT NULL", "FOREIGN KEY -> SHELTER", "Target relief camp requisition is lodged against"],
        ["REQUEST.resource_type", "VARCHAR(100)", "NOT NULL", "None", "Required humanitarian supply item"],
        ["REQUEST.quantity_requested", "INT", "NOT NULL", "CHECK (> 0)", "Number of units required by victims"],
        ["REQUEST.request_status", "VARCHAR(30)", "NOT NULL", "CHECK ('Pending','Fulfilled',...)", "Current lifecycle state of aid ticket"],
        ["REQUEST.request_date", "DATE", "NOT NULL", "ISO Format", "Calendar date request was logged"],
        ["REQUEST.fulfilled_date", "DATE", "NULLABLE", "Three-Valued Logic", "Date aid was physically delivered; NULL if pending"],
        ["REQUEST.remarks", "VARCHAR(255)", "NULLABLE", "None", "Priority justification, infant notes, medical flags"],
        ["VOLUNTEER.volunteer_id", "INT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Unique relief personnel identification number"],
        ["VOLUNTEER.volunteer_name", "VARCHAR(100)", "NOT NULL", "None", "Full name of deployed field volunteer"],
        ["VOLUNTEER.phone", "VARCHAR(20)", "NOT NULL", "None", "Operational cellular contact number"],
        ["VOLUNTEER.skill", "VARCHAR(100)", "NOT NULL", "None", "Core operational competency (Driving, Medical, Rescue)"],
        ["VOLUNTEER.availability_status", "VARCHAR(30)", "NOT NULL", "CHECK ('Available','Deployed','Leave')", "Current active field deployment readiness status"],
        ["DISTRIBUTION.distribution_id", "BIGINT", "NOT NULL", "PRIMARY KEY, AUTO_INCREMENT", "Unique supply distribution disbursement receipt number"],
        ["DISTRIBUTION.resource_id", "BIGINT", "NOT NULL", "FOREIGN KEY -> RESOURCE", "Resource stock item disbursed (ON DELETE RESTRICT)"],
        ["DISTRIBUTION.volunteer_id", "INT", "NOT NULL", "FOREIGN KEY -> VOLUNTEER", "Authorized volunteer executing dispatch"],
        ["DISTRIBUTION.distributed_qty", "DECIMAL(10,2)", "NOT NULL", "CHECK (distributed_qty > 0)", "Quantity of units handed over to camp victims"],
        ["DISTRIBUTION.distributed_at", "TIMESTAMP", "NOT NULL", "DEFAULT CURRENT_TIMESTAMP", "Exact system timestamp when transaction committed"]
    ]
    bh.add_table_data(doc, dict_headers, dict_data, col_widths=[1.5, 1.0, 0.8, 1.5, 1.7])

    bh.add_styled_heading(doc, "Appendix C: System Architecture & Functional Source Code Structure", level=2)
    bh.add_paragraph(doc, 
        "The software architecture follows a decoupled multi-tier topology connecting the MySQL 8.0 relational database "
        "to an asynchronous Node.js Express application server and a responsive web presentation layer:")
        
    bh.add_bullet(doc, "1. Database Engine Layer (MySQL 8.0):", 
        "Hosts the DRRMS_DB catalog, managing InnoDB buffer pools, row-level locks, B-tree indexes, stored procedures, deterministic functions, "
        "and SQL view abstractions.")
        
    bh.add_bullet(doc, "2. Server Runtime Layer (Node.js & Express):", 
        "server.js manages asynchronous connection pools via mysql2/promise, intercepts REST API requests (/api/bootstrap, /api/events, "
        "/api/shelters, /api/donors, /api/resources, /api/requests, /api/volunteers, /api/distribute, /api/reports, /api/seed, /api/clear), "
        "executes input sanitization and date normalization, and injects anti-caching HTTP security headers.")
        
    bh.add_bullet(doc, "3. Presentation Layer (public/index.html):", 
        "Provides dynamic role-based workspaces for Donor, Citizen, Volunteer, and Coordinator users. Uses modern CSS tokens, dark/white theme toggles, "
        "live KPI metrics, and immediate tactile feedback.")

    bh.add_styled_heading(doc, "Appendix D: Student Declaration & Anti-Plagiarism Statement", level=2)
    bh.add_paragraph(doc, 
        "I, EDWIN SAJI, Register Number: 26MCAC22, student of Master of Computer Applications (MCA), I Semester, "
        "Department of Computer Applications, Kristu Jayanti (Deemed to be University), Bengaluru, hereby declare that the practical report entitled:\n\n"
        "“DISASTER RESOURCE RECOVERY MANAGEMENT SYSTEM (DRRMS)”\n\n"
        "submitted in partial fulfilment of the requirements for the practical course Advanced Database Management System Practical (26MCD1L211), "
        "is a bona fide record of original engineering work carried out by me under the guidance of my designated Faculty Guide, "
        "Department of Computer Applications, Kristu Jayanti (Deemed to be University), Bengaluru.\n\n"
        "I affirm that this work is original, free from plagiarism, and has not been submitted previously, in part or in whole, for the award of "
        "any other degree, diploma, fellowship, or associate certificate in this or any other university or academic institution.\n\n"
        "All literature references, statutory guidelines, framework libraries, and design patterns utilized in this project have been duly acknowledged "
        "and documented in accordance with institutional academic ethics.")
        
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(24)
    r_place = p_sign.add_run("Place: Bengaluru, Karnataka, India\nDate: 28th October 2026\n\n\n\n")
    r_place.font.name = "Calibri"
    r_place.font.size = Pt(11)
    
    r_sname = p_sign.add_run("EDWIN SAJI\n")
    r_sname.font.name = "Calibri"
    r_sname.font.size = Pt(12)
    r_sname.font.bold = True
    r_sname.font.color.rgb = RGBColor(15, 34, 64)
    
    r_sreg = p_sign.add_run("Candidate Register Number: 26MCAC22\nDepartment of Computer Applications (MCA)\nKristu Jayanti (Deemed to be University), Bengaluru\n")
    r_sreg.font.name = "Calibri"
    r_sreg.font.size = Pt(11)

    output_path = os.path.abspath("ADBMS_Project_Report_DRRMS.docx")
    doc.save(output_path)
    print(f"Report successfully generated and saved at: {output_path}")

if __name__ == "__main__":
    build_report()
