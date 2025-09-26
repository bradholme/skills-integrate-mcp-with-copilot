# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities with role-based access controls.

## Features

- View all available extracurricular activities
- Sign up for activities (students only)
- Unregister students from activities (teachers only)
- Create new users with roles (student, teacher, staff)
- Role-based access controls for activity management

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
   - Web interface: http://localhost:8000
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/users`                                                          | List all users and their roles                                      |
| POST   | `/users/create?email=user@mergington.edu&role=student`           | Create a new user with a specific role                             |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity (students only)                            |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu&acting_user=teacher@mergington.edu` | Unregister a student from an activity (teachers only) |

## Role-Based Access Controls

- **Students**: Can sign up for activities
- **Teachers**: Can unregister students from activities  
- **Staff**: Currently has same permissions as students

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Users** - Uses email as identifier:
   - Role (student, teacher, or staff)

2. **Activities** - Uses activity name as identifier:
   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

All data is stored in memory, which means data will be reset when the server restarts.
