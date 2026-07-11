# Week 7 Progress Report

## Project Update

This week focused on extending EntryPoint with a limited AI-assisted feature to improve the monitoring component and provide more meaningful notifications to students.

## Work Completed

### AI-Assisted Change Summarization

A local language model was integrated into the monitoring workflow using Ollama. Instead of only detecting that a webpage has changed, the system can now generate a concise, student-friendly summary describing the meaningful changes.

The AI component is used only after a webpage change has been detected. The monitoring process remains deterministic through webpage content hashing, while the AI assists with organizing and explaining the detected changes.

### Monitoring Workflow Improvements

The monitoring workflow now performs the following steps:

1. Retrieve webpage content.
2. Remove unnecessary HTML elements.
3. Generate a SHA-256 content hash.
4. Compare the new hash with the previously stored baseline.
5. If a change is detected, compare the previous and current page content.
6. Generate an AI-assisted summary of the detected changes.
7. Store the summary in the database.
8. Generate personalized notifications for students subscribed to the affected resource.

This provides students with a clear explanation of what changed instead of only informing them that a webpage was updated.

### Local AI Integration

The AI-assisted summarization feature was implemented using Ollama with a locally hosted language model. This approach allows the project to demonstrate AI-assisted information handling without relying on external paid APIs.

The local model receives the previous and updated webpage content and produces a short summary focused on student-relevant changes such as schedules, procedures, deadlines, routes, and requirements.

### Notification Improvements

Notifications now contain meaningful summaries instead of generic update messages. This allows students to quickly understand whether a webpage update is relevant before visiting the official university website.

### Overall Progress

The EntryPoint prototype now includes:

- Personalized onboarding framework
- Transportation onboarding
- Accommodation scalability example
- Resource subscriptions
- Automated webpage monitoring
- Webpage content hashing
- AI-assisted change summarization
- Personalized notifications
- React frontend demonstration
- Preliminary user evaluation

## Current Status

The project now demonstrates a complete end-to-end workflow:

Student → Personalized Resources → Subscription → Webpage Monitoring → Change Detection → AI Summary → Personalized Notification

## Next Steps

- Continue polishing the frontend for the final presentation.
- Improve the visual presentation of monitoring and notifications.
- Collect any additional user feedback if possible.
- Complete the final report.
- Prepare the final presentation and demonstration.