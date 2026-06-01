# AI Change Monitoring Plan

## Overview

The AI-assisted component of EntryPoint focuses on monitoring selected Texas State University webpages and identifying meaningful content changes.

## Initial Pages to Monitor

Examples include:

- Orientation
- Academic Advising
- Registration
- Housing
- Financial Aid
- International Student Services
- Technology Resources

## Monitoring Process

### Step 1

Retrieve webpage content.

### Step 2

Store a snapshot of the webpage content.

### Step 3

Compare current content against previously stored content.

### Step 4

Identify meaningful differences.

### Step 5

Generate a short change summary.

### Step 6

Store the results in the database.

### Step 7

Display updates to administrators and students.

## Stored Information

For each monitored page:

- Page title
- URL
- Last checked date
- Previous content hash
- Current content hash
- Change summary
- Importance level

## Importance Levels

### Low

Minor wording changes.

### Medium

Updates to information or procedures.

### High

Important deadlines, requirements, or policy changes.

## Potential AI Usage

Future versions may use LLMs to:

- Summarize webpage changes.
- Classify change importance.
- Improve update descriptions.

## Expected Benefits

- More current resource information.
- Reduced manual monitoring effort.
- Better student awareness of important updates.