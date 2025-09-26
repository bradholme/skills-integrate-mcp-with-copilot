"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from typing import Literal

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities and managing users/roles")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory user database
users = {
    "emma@mergington.edu": {"role": "student"},
    "sophia@mergington.edu": {"role": "student"},
    "michael@mergington.edu": {"role": "student"},
    "daniel@mergington.edu": {"role": "student"},
    "john@mergington.edu": {"role": "student"},
    "olivia@mergington.edu": {"role": "student"},
    "liam@mergington.edu": {"role": "student"},
    "noah@mergington.edu": {"role": "student"},
    "ava@mergington.edu": {"role": "student"},
    "mia@mergington.edu": {"role": "student"},
    "amelia@mergington.edu": {"role": "student"},
    "harper@mergington.edu": {"role": "student"},
    "ella@mergington.edu": {"role": "student"},
    "scarlett@mergington.edu": {"role": "student"},
    "james@mergington.edu": {"role": "student"},
    "benjamin@mergington.edu": {"role": "student"},
    "charlotte@mergington.edu": {"role": "student"},
    "henry@mergington.edu": {"role": "student"},
    # Example teachers
    "teacher1@mergington.edu": {"role": "teacher"},
    "teacher2@mergington.edu": {"role": "teacher"},
    # Example staff
    "admin@mergington.edu": {"role": "staff"}
}

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/users")
def list_users():
    """List all users and their roles"""
    return users

@app.post("/users/create")
def create_user(email: str = Query(...), role: Literal["student", "teacher", "staff"] = Query(...)):
    """Create a new user with a role"""
    if email in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[email] = {"role": role}
    return {"message": f"Created user {email} with role {role}"}

@app.get("/activities")
def get_activities():
    return activities

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate user exists and is a student
    if email not in users or users[email]["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can sign up for activities (user not found or not a student)")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, acting_user: str = Query(...)):
    """Unregister a student from an activity. Only teachers can perform this action."""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate acting user exists and is a teacher
    if acting_user not in users or users[acting_user]["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can unregister students from activities")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name} by {acting_user}"}