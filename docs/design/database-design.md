# EntryPoint Database Design

## Overview

EntryPoint will use PostgreSQL as the backend relational database. The schema is designed to be minimal, normalized, and avoid unnecessary redundancy. The initial version focuses on Texas State University, but the structure can later support expansion to additional universities.

## Tables

### users

Stores login and account information.

| Column        | Type         | Key         | Description           |
| ------------- | ------------ | ----------- | --------------------- |
| user_id       | SERIAL       | Primary Key | Unique user ID        |
| first_name    | VARCHAR(100) |             | User first name       |
| last_name     | VARCHAR(100) |             | User last name        |
| email         | VARCHAR(255) | Unique      | User email            |
| password_hash | VARCHAR(255) |             | Hashed password       |
| role          | VARCHAR(20)  |             | student or admin      |
| created_at    | TIMESTAMP    |             | Account creation date |

---

### student_profiles

Stores student-specific information. This table separates student profile data from login data to avoid mixing authentication information with student details.

| Column           | Type         | Key                                   | Description                        |
| ---------------- | ------------ | ------------------------------------- | ---------------------------------- |
| profile_id       | SERIAL       | Primary Key                           | Unique profile ID                  |
| user_id          | INTEGER      | Foreign Key references users(user_id) | Connected user                     |
| student_type     | VARCHAR(50)  |                                       | freshman, transfer, graduate, etc. |
| major            | VARCHAR(100) |                                       | Student major                      |
| is_international | BOOLEAN      |                                       | Whether student is international   |
| created_at       | TIMESTAMP    |                                       | Profile creation date              |

Relationship:

* One user can have one student profile.

---

### resource_categories

Stores resource categories.

| Column      | Type         | Key         | Description          |
| ----------- | ------------ | ----------- | -------------------- |
| category_id | SERIAL       | Primary Key | Unique category ID   |
| name        | VARCHAR(100) | Unique      | Category name        |
| description | TEXT         |             | Category description |

Example categories:

* Admissions
* Orientation
* Housing
* Financial Aid
* Academic Advising
* Registration
* International Student Services
* Technology Resources
* Career Services

---

### resources

Stores official Texas State resources.

| Column           | Type         | Key                                                     | Description             |
| ---------------- | ------------ | ------------------------------------------------------- | ----------------------- |
| resource_id      | SERIAL       | Primary Key                                             | Unique resource ID      |
| category_id      | INTEGER      | Foreign Key references resource_categories(category_id) | Resource category       |
| title            | VARCHAR(255) |                                                         | Resource title          |
| description      | TEXT         |                                                         | Resource description    |
| url              | TEXT         |                                                         | Official resource URL   |
| last_reviewed_at | TIMESTAMP    |                                                         | Last manual review date |
| created_at       | TIMESTAMP    |                                                         | Resource creation date  |

Relationship:

* One category can have many resources.

---

### checklist_templates

Stores reusable checklist templates.

| Column           | Type         | Key         | Description                                    |
| ---------------- | ------------ | ----------- | ---------------------------------------------- |
| template_id      | SERIAL       | Primary Key | Unique template ID                             |
| name             | VARCHAR(255) |             | Template name                                  |
| description      | TEXT         |             | Template description                           |
| student_type     | VARCHAR(50)  |             | freshman, transfer, graduate, etc.             |
| is_international | BOOLEAN      |             | Whether template is for international students |
| created_at       | TIMESTAMP    |             | Template creation date                         |

Example templates:

* New Freshman Checklist
* Transfer Student Checklist
* International Student Checklist

---

### checklist_tasks

Stores tasks that belong to checklist templates.

| Column      | Type         | Key                                                     | Description                             |
| ----------- | ------------ | ------------------------------------------------------- | --------------------------------------- |
| task_id     | SERIAL       | Primary Key                                             | Unique task ID                          |
| template_id | INTEGER      | Foreign Key references checklist_templates(template_id) | Parent checklist template               |
| resource_id | INTEGER      | Foreign Key references resources(resource_id), nullable | Related resource                        |
| title       | VARCHAR(255) |                                                         | Task title                              |
| description | TEXT         |                                                         | Task details                            |
| priority    | VARCHAR(20)  |                                                         | low, medium, or high                    |
| due_stage   | VARCHAR(50)  |                                                         | before_arrival, first_week, first_month |
| created_at  | TIMESTAMP    |                                                         | Task creation date                      |

Relationship:

* One checklist template can have many checklist tasks.
* One checklist task may link to one resource.

---

### student_task_completion

Tracks which tasks a student has completed.

| Column        | Type      | Key                                                 | Description                 |
| ------------- | --------- | --------------------------------------------------- | --------------------------- |
| completion_id | SERIAL    | Primary Key                                         | Unique completion record ID |
| profile_id    | INTEGER   | Foreign Key references student_profiles(profile_id) | Student profile             |
| task_id       | INTEGER   | Foreign Key references checklist_tasks(task_id)     | Completed task              |
| is_completed  | BOOLEAN   |                                                     | Completion status           |
| completed_at  | TIMESTAMP |                                                     | Date completed              |

Constraint:

* Unique(profile_id, task_id)

Relationship:

* One student profile can have many task completion records.
* One checklist task can appear in many student completion records.

---

### monitored_pages

Stores Texas State webpages selected for change monitoring.

| Column          | Type         | Key                                                     | Description                  |
| --------------- | ------------ | ------------------------------------------------------- | ---------------------------- |
| page_id         | SERIAL       | Primary Key                                             | Unique page ID               |
| category_id     | INTEGER      | Foreign Key references resource_categories(category_id) | Related category             |
| title           | VARCHAR(255) |                                                         | Page title                   |
| url             | TEXT         | Unique                                                  | Page URL                     |
| last_checked_at | TIMESTAMP    |                                                         | Last monitoring check        |
| active          | BOOLEAN      |                                                         | Whether monitoring is active |

Relationship:

* One category can have many monitored pages.

---

### page_change_logs

Stores detected webpage changes.

| Column                | Type         | Key                                             | Description                       |
| --------------------- | ------------ | ----------------------------------------------- | --------------------------------- |
| change_id             | SERIAL       | Primary Key                                     | Unique change record ID           |
| page_id               | INTEGER      | Foreign Key references monitored_pages(page_id) | Monitored page                    |
| previous_content_hash | VARCHAR(255) |                                                 | Hash of previous content          |
| new_content_hash      | VARCHAR(255) |                                                 | Hash of new content               |
| change_summary        | TEXT         |                                                 | Summary of detected change        |
| importance_level      | VARCHAR(20)  |                                                 | low, medium, or high              |
| detected_at           | TIMESTAMP    |                                                 | Date change was detected          |
| reviewed_by_admin     | BOOLEAN      |                                                 | Whether admin reviewed the change |

Relationship:

* One monitored page can have many change logs.

## Normalization Notes

The schema avoids redundancy by separating repeated information into separate tables.

Examples:

* Resource category names are stored only in `resource_categories`, not repeated directly in each resource.
* User login information is stored in `users`, while student-specific information is stored in `student_profiles`.
* Checklist templates are separated from checklist tasks.
* Student task completion is stored separately so checklist tasks are not duplicated for every student.
* Monitored pages are separated from page change logs so each page can have multiple historical change records.

## Future Expansion

For future multi-university support, a `universities` table can be added:

| Column        | Type         | Key         | Description          |
| ------------- | ------------ | ----------- | -------------------- |
| university_id | SERIAL       | Primary Key | Unique university ID |
| name          | VARCHAR(255) | Unique      | University name      |
| website_url   | TEXT         |             | University website   |

Then `resources`, `checklist_templates`, and `monitored_pages` can reference `universities(university_id)`.
