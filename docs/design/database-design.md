# Database Design

## Overview

EntryPoint will use PostgreSQL as the relational database. The database is designed to support student accounts, administrator accounts, onboarding checklists, campus resources, and webpage monitoring logs.

The design focuses on Texas State University for the initial version but keeps future multi-university expansion possible.

---

## Main Tables

### users

Stores account information for students and administrators.

Fields:

- id
- first_name
- last_name
- email
- password_hash
- role
- created_at

Role values:

- student
- admin

---

### student_profiles

Stores student-specific information used to personalize onboarding checklists.

Fields:

- id
- user_id
- student_type
- major
- is_international
- created_at

Example student types:

- freshman
- transfer
- graduate
- international

---

### resource_categories

Stores categories used to organize Texas State resources.

Fields:

- id
- name
- description

Example categories:

- Admissions
- Orientation
- Housing
- Financial Aid
- Academic Advising
- Registration
- International Student Services
- Technology Resources
- Career Services
- Student Organizations

---

### resources

Stores Texas State resources shown to students.

Fields:

- id
- category_id
- title
- description
- url
- student_type_relevance
- last_reviewed_at
- created_at

---

### checklist_templates

Stores reusable onboarding checklist templates.

Fields:

- id
- name
- description
- student_type
- is_international
- created_at

Example templates:

- New Freshman Checklist
- Transfer Student Checklist
- International Student Checklist

---

### checklist_tasks

Stores tasks that belong to checklist templates.

Fields:

- id
- template_id
- resource_id
- title
- description
- priority
- due_stage
- created_at

Example priority values:

- low
- medium
- high

Example due stages:

- before_arrival
- first_week
- first_month

---

### student_task_completion

Tracks which checklist tasks each student has completed.

Fields:

- id
- student_profile_id
- task_id
- is_completed
- completed_at

---

### monitored_pages

Stores Texas State webpages that the system monitors for changes.

Fields:

- id
- title
- url
- category_id
- last_checked_at
- active

---

### page_change_logs

Stores detected webpage changes.

Fields:

- id
- monitored_page_id
- previous_content_hash
- new_content_hash
- change_summary
- importance_level
- detected_at
- reviewed_by_admin

Example importance levels:

- low
- medium
- high

---

## Relationships

- One user can have one student profile.
- One resource category can have many resources.
- One resource category can have many monitored pages.
- One checklist template can have many checklist tasks.
- One checklist task can be connected to one resource.
- One student profile can have many task completion records.
- One monitored page can have many page change logs.

---

## Future Expansion Consideration

Although the first version focuses on Texas State University, the database can later be expanded by adding a `universities` table and connecting resources, checklist templates, and monitored pages to a university ID.