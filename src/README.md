# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities with role-based user management.

## Features

- View all available extracurricular activities
- Student-only activity signup (role-based access control)
- Teacher-only student unregistration (role-based access control)  
- User management with roles (student, teacher, staff)
- In-memory user and activity data storage

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - Web interface: http://localhost:8000/
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                                               | Description                                                         | Access Control           |
| ------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------ |
| GET    | `/activities`                                                                          | Get all activities with their details and current participant count | Public                   |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu`                     | Sign up for an activity                                             | Students only            |
| DELETE | `/activities/{activity_name}/unregister?email=student@edu&acting_user=teacher@edu`    | Unregister a student from an activity                               | Teachers only            |
| GET    | `/users`                                                                               | List all users and their roles                                      | Public                   |
| POST   | `/users/create?email=user@mergington.edu&role=student`                                | Create a new user with a role (student, teacher, or staff)         | Public                   |

## Role-Based Access Control

The system implements three user roles with specific permissions:

- **Students**: Can sign up for activities
- **Teachers**: Can unregister students from activities (requires teacher authentication)
- **Staff**: No specific activity permissions currently defined

### Web Interface Role Controls

- **Activity Signup**: Students can use the signup form to join activities
- **Student Unregistration**: Clicking the ❌ button next to a participant prompts for teacher email authentication

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Users** - Uses email as identifier:
   - Role (student, teacher, staff)

2. **Activities** - Uses activity name as identifier:
   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

All data is stored in memory, which means data will be reset when the server restarts.
