# Week 6 Progress Report

## Project Update

This week focused on strengthening EntryPoint as a research prototype by improving the frontend demo, expanding the evaluation component, and continuing work on personalized monitoring.

## Work Completed

- Completed a cleaner React frontend demo for EntryPoint.
- Added a student-facing dashboard for the personalized onboarding workflow.
- Included transportation onboarding as the main pilot domain.
- Included accommodation as a scalability example to show that the framework can expand beyond transportation.
- Connected the frontend to backend API endpoints for resources, subscriptions, monitoring, and notifications.
- Improved the monitoring workflow so monitored pages can store baseline hashes and compare future checks against stored values.
- Continued refining the personalized notification workflow for students subscribed to specific transportation resources.
- Created and used a survey to collect student feedback on EntryPoint.
- Generated an initial evaluation PDF summarizing survey results.

## Evaluation Work

A small preliminary user evaluation was conducted with international students. Participants compared existing Texas State transportation resources with the EntryPoint prototype.

The evaluation measured:

- Ease of finding transportation information
- Ease of understanding transportation information
- Confidence after completing the task
- Preference between existing resources and EntryPoint
- Qualitative feedback on what EntryPoint made easier

Initial survey results suggested that participants found EntryPoint easier to use and more organized than navigating existing transportation webpages directly.

## Monitoring Work

The monitoring component retrieves transportation webpages, extracts meaningful page text, removes unnecessary HTML elements such as scripts, styles, navigation, and footers, and generates a SHA-256 content hash. This hash is used as a content fingerprint.

The improved monitoring design allows the system to store an initial baseline hash and compare future checks against it. If the hash changes, the system can identify that the webpage content changed and use that change to notify students who subscribed to the affected resource.

## Scalability

Transportation remains the primary pilot domain, but accommodation is now included as a second domain example. This demonstrates that the framework can scale by replacing transportation-specific resources and templates with accommodation-related resources such as housing, leases, utilities, move-in information, and roommate guidance.

## Current Status

EntryPoint now has a working backend, database, monitoring prototype, notification workflow, React frontend demo, accommodation scalability example, and preliminary student evaluation results.

## Next Steps

- Continue collecting more student survey responses if possible.
- Refine the automatic monitoring and notification workflow.
- Improve the frontend presentation for the final demo.
- Create final diagrams for system architecture and database design.
- Begin preparing the final report and presentation.