# Week 5 Progress Report

## Project Update

This week focused on expanding EntryPoint into a fully personalized onboarding framework by connecting transportation monitoring directly to individual students. Rather than simply monitoring transportation webpages, the system now supports student-specific transportation preferences and personalized notifications.

## Work Completed

* Implemented student transportation subscriptions to allow students to follow transportation resources relevant to them.
* Added a notification system for storing personalized transportation updates.
* Connected transportation resources to student-specific subscriptions.
* Expanded the monitoring workflow to support personalized notifications.
* Updated the database design with new subscription and notification tables.
* Implemented API endpoints for managing subscriptions and retrieving notifications.
* Created a demonstration workflow showing the complete personalized monitoring process.
* Continued refining project documentation to emphasize scalability beyond transportation.

## Monitoring Implementation

The monitoring service retrieves transportation webpages using Python Requests and parses the HTML using BeautifulSoup. Before comparing content, scripts, navigation menus, styles, and footer elements are removed so that only meaningful transportation information remains. The cleaned content is then converted into a SHA-256 hash that serves as a fingerprint of the webpage.

This monitoring approach is intended to identify meaningful transportation information changes while reducing false positives caused by webpage formatting or layout updates. The generated fingerprints provide the foundation for comparing future versions of monitored webpages.

## Personalization Workflow

The personalized workflow now follows these steps:

1. A student subscribes to one or more transportation resources.
2. The subscription is stored in the database.
3. The monitoring service checks transportation webpages.
4. When a transportation resource changes, the system identifies students subscribed to that resource.
5. Personalized notifications are generated and stored for those affected students.
6. Students can retrieve their notifications through the API.

## Scalability

Transportation continues to serve as the pilot implementation. The framework is designed so that the same architecture can later support additional onboarding domains, including accommodation, healthcare, academic services, and employment. Only the domain-specific resources, templates, and monitored webpages would need to change, while the personalization, monitoring, and notification framework remains reusable.

## Current Status

The backend now supports transportation resources, student-specific subscriptions, personalized notification generation, and a working monitoring prototype. The project has evolved from a general onboarding concept into a personalized onboarding framework with transportation serving as the initial research domain.

## Next Steps

* Persist webpage hashes and automatically compare newly generated hashes with previously stored versions.
* Implement automatic change logging for monitored transportation resources.
* Connect monitoring directly to notification generation without manual simulation.
* Begin integrating the React frontend with the backend APIs.
* Develop the user interface for transportation subscriptions and personalized notifications.
* Continue preparing the framework for expansion into additional onboarding domains.
