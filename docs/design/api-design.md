# API Design

## Overview

The EntryPoint backend will expose REST API endpoints through FastAPI.

The API will handle:

- Authentication
- Student profiles
- Resources
- Checklists
- Task completion
- Webpage monitoring

---

# Authentication Endpoints

## Register User

POST /api/auth/register

Purpose:

Create a new student account.

---

## Login User

POST /api/auth/login

Purpose:

Authenticate user and return JWT token.

---

## Get Current User

GET /api/auth/me

Purpose:

Return current authenticated user information.

---

# Student Profile Endpoints

## Get Student Profile

GET /api/profile

Purpose:

Retrieve student profile information.

---

## Update Student Profile

PUT /api/profile

Purpose:

Update profile information.

---

# Resource Endpoints

## Get All Resources

GET /api/resources

Purpose:

Return all available resources.

---

## Get Single Resource

GET /api/resources/{id}

Purpose:

Return resource details.

---

## Search Resources

GET /api/resources/search

Purpose:

Search resources by keyword.

---

## Filter Resources

GET /api/resources/category/{category_id}

Purpose:

Filter resources by category.

---

# Checklist Endpoints

## Get Student Checklist

GET /api/checklists

Purpose:

Return student's assigned checklist.

---

## Get Checklist Tasks

GET /api/checklists/tasks

Purpose:

Return checklist tasks.

---

## Complete Task

PUT /api/checklists/tasks/{task_id}

Purpose:

Mark task as completed.

---

# Admin Endpoints

## Create Resource

POST /api/admin/resources

Purpose:

Create a resource.

---

## Update Resource

PUT /api/admin/resources/{id}

Purpose:

Update resource.

---

## Delete Resource

DELETE /api/admin/resources/{id}

Purpose:

Delete resource.

---

## Create Checklist Template

POST /api/admin/checklists

Purpose:

Create onboarding checklist template.

---

## Update Checklist Template

PUT /api/admin/checklists/{id}

Purpose:

Update checklist template.

---

# Monitoring Endpoints

## Get Monitored Pages

GET /api/monitoring/pages

Purpose:

Return monitored webpages.

---

## Add Monitored Page

POST /api/monitoring/pages

Purpose:

Add webpage to monitoring list.

---

## Get Change Logs

GET /api/monitoring/logs

Purpose:

Return webpage change history.

---

## Get Change Summary

GET /api/monitoring/summary

Purpose:

Return summarized webpage updates.

---

# Future Expansion

Future versions may include:

- Multi-university support
- Notification endpoints
- AI recommendation endpoints
- Mobile application support