# Week 8 Progress Report

## Project
**EntryPoint: Personalized Onboarding System for International Students**

---

# Objectives

The primary objective for Week 8 was to complete the EntryPoint prototype by finalizing the AI-powered notification system and integrating personalized notifications into the webpage monitoring workflow. The focus was on transforming generic webpage updates into meaningful, student-specific notifications while maintaining a lightweight architecture using a locally hosted large language model.

---

# Work Completed

## 1. Personalized AI Notification System

Implemented a personalized notification generation system that combines:

- AI-generated webpage change summaries
- Student profile information
- Resource category information
- Personalized recommendations

Instead of delivering identical notifications to every subscribed student, the system now generates notifications that explain:

- What changed
- Why the update is relevant to the student
- Recommended actions based on the resource category

This provides students with more meaningful and actionable information.

---

## 2. Improved Local AI Summarization

Refined the Ollama (Gemma 3:1B) prompt to produce concise and factual webpage summaries.

The updated prompt now:

- Limits summaries to 1–3 short sentences.
- Reports only meaningful changes supported by the webpage content.
- Ignores formatting or wording changes that do not alter meaning.
- Focuses on schedules, deadlines, procedures, locations, fees, requirements, and other important information.
- Prevents speculation or unsupported statements.

The AI is now responsible only for summarizing factual webpage changes, while the application handles personalization.

---

## 3. Monitoring Pipeline Completion

Completed the end-to-end webpage monitoring workflow.

When a monitored webpage changes, the system now performs the following steps:

1. Detects webpage changes using SHA-256 content hashing.
2. Generates a factual AI summary using Ollama.
3. Stores the detected change in the database.
4. Retrieves all students subscribed to the affected resource.
5. Creates personalized notifications for each subscribed student.
6. Stores notifications in the database.
7. Makes notifications immediately available through the frontend.

This completes the automated monitoring pipeline.

---

## 4. AI Demonstration Endpoint

Expanded the local AI demonstration endpoint to showcase the complete personalization process.

The demonstration now returns:

- AI-generated webpage summary
- Personalized notification
- Student profile context
- Local AI model information

This allows the personalization process to be demonstrated without modifying production data.

---

## 5. Frontend Enhancements

Updated the React frontend to display:

- AI-generated webpage summaries
- Personalized notifications
- Student profile context
- Local AI status indicators
- Improved notification presentation

The interface now demonstrates the complete workflow from webpage monitoring to personalized student notifications.

---

# Technologies Used

- React
- FastAPI
- PostgreSQL
- SQLAlchemy
- Ollama
- Gemma 3:1B
- Python
- JavaScript

---

# Current Project Status

The EntryPoint prototype now includes:

- Student profile management
- Personalized onboarding recommendations
- Transportation onboarding pilot
- Accommodation scalability demonstration
- Resource subscriptions
- Automated webpage monitoring
- Local AI webpage summarization
- Personalized notification generation
- React frontend
- FastAPI backend
- PostgreSQL database
- End-to-end monitoring and notification workflow

The prototype is now fully functional and ready for demonstration.

---

# Next Steps

The remaining work focuses on presentation and evaluation rather than additional software development.

The next tasks include:

- Preparing the final presentation slides
- Creating architecture and workflow diagrams
- Demonstrating the completed system
- Conducting user evaluation using the prepared survey
- Presenting the final research prototype

---

# Overall Progress

**Project Completion:** **100%**

The EntryPoint research prototype has been completed successfully and is ready for final presentation and evaluation.