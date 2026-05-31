# Requirements

## Functional Requirements

### Student Features

Students shall be able to:

* Create an account.
* Log in and log out.
* View a personalized onboarding checklist.
* Mark checklist tasks as completed.
* View categorized Texas State resources.
* Search resources by keyword.
* Filter resources by category.
* View important university updates generated from monitored webpages.

### Administrator Features

Administrators shall be able to:

* Create resources.
* Edit resources.
* Delete resources.
* Create resource categories.
* Create onboarding checklist templates.
* Edit onboarding checklist templates.
* Create checklist tasks.
* Edit checklist tasks.
* View webpage monitoring results.
* Review detected webpage changes.

### Resource Management Features

Each resource shall contain:

* Title
* Description
* Category
* URL
* Student type relevance
* Last updated date

### Checklist Features

Each checklist task shall contain:

* Task title
* Task description
* Category
* Priority level
* Related resource link
* Completion status

### Webpage Monitoring Features

The system shall be able to:

* Store monitored Texas State webpage URLs.
* Periodically check selected webpages.
* Detect webpage content changes.
* Store webpage change logs.
* Generate summaries of detected changes.
* Allow administrators to review detected changes.

---

## Non-Functional Requirements

### Usability

* The interface should be easy to learn and navigate.
* The system should provide clear organization of resources and tasks.

### Performance

* Resource pages should load quickly.
* API responses should remain responsive under normal usage.

### Security

* Passwords must be securely stored.
* Authentication must use JWT tokens.
* Protected routes must require authentication.

### Maintainability

* Backend code should be modular.
* Database structure should support future expansion.
* Documentation should be maintained throughout development.

### Scalability

* The architecture should allow future support for additional universities.

---

## Technical Requirements

### Frontend

* React

### Backend

* FastAPI

### Database

* PostgreSQL

### ORM

* SQLAlchemy

### Authentication

* JWT Authentication

### Version Control

* Git and GitHub

---

## Independent Study Requirements

The project must produce:

* A functional software system.
* Documentation of design and implementation decisions.
* A written report.
* A final presentation and demonstration.
* Evaluation of the webpage monitoring component.
