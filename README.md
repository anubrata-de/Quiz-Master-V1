<!-- portfolio
title: Quiz Master V1
tagline: Multi-User Exam Preparation Platform
category: Full-stack apps
summary: Admins manage subjects, chapters and quizzes; students take timed quizzes with a live countdown and auto-submit, then track their results.
tags: Flask, Jinja2, SQLite, Bootstrap
slug: quiz-master-v1
featured: yes
-->

# Quiz Master - V1

A multi-user exam preparation platform built with Flask that allows administrators to create and manage quizzes while enabling users to take tests and track their performance.

## Project Overview
This is a mandatory project that implements an exam preparation site for multiple courses. The application is built using:
- Flask for application back-end
- Jinja2 templating, HTML, CSS and Bootstrap for front-end
- SQLite for database

## Core Features

### User Management
- Two distinct roles: Admin (Quiz Master) and User
- Admin account pre-exists in database (no registration required)
- User registration with:
  - Email (username)
  - Password
  - Full Name
  - Qualification
  - Date of Birth
- Secure password hashing
- Role-based access control

### Subject and Chapter Management
- Admin can create and manage subjects
- Each subject can have multiple chapters
- Hierarchical organization of content
- Edit and delete functionality for both subjects and chapters

### Quiz Management
- Create quizzes with:
  - Title and description
  - Date and time settings
  - Duration limit (HH:MM format)
  - Remarks/instructions
- Add multiple-choice questions (MCQ)
- Edit and delete quizzes
- View quiz statistics (attempts, questions)

### Quiz Taking Experience
- Dynamic subject and chapter filtering
- Real-time countdown timer
- Auto-submit when time expires
- Multiple choice questions
- Immediate score calculation
- View detailed results

### Admin Dashboard
- Overview of recent quizzes
- Manage users, subjects, and chapters
- View quiz records and statistics
- Create and edit quizzes
- Monitor user attempts

### User Dashboard
- View available quizzes
- Filter quizzes by subject and chapter
- See quiz details (duration, date, description)
- Track personal performance
- View attempt history

## Technical Implementation

### Database Structure
- User: Stores user information and authentication
- Subject: Manages quiz subjects
- Chapter: Organizes content within subjects
- Quiz: Contains quiz details and settings
- Question: Stores quiz questions
- Option: Manages answer choices
- Result: Tracks user performance

### Security Features
- Password hashing
- Role-based access control
- Session management
- Input validation
- SQL injection prevention

## Usage

### Admin (Quiz Master)
1. Login with pre-existing admin account
2. Create subjects and chapters
3. Create quizzes with questions
4. Manage users and view statistics

### User
1. Register with required details
2. Login to access dashboard
3. Browse available quizzes
4. Take quizzes within time limit
5. View results and performance history