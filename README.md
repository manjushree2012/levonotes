# LevoNotes
Levonotes is a simple and clean note taking application. Built as a assignment under time constraint, it contains only the basic functionalities you would expect from a note taking app. The application allows users to create, update and delete a note. Users can also set reminders for a note for a specified date and time.

## Tech and Tools used
- Flask (Python)
- Svelte & SvelteKit
- SQLAlchemy
- PostgreSQL (Supabase)
- Celery (For reminders)
- ShadCN (UI Library)

## Features
- Create new notes
- Edit existing notes
- Delete notes
- Set a reminder

## Limitations
- Any scaling issue have not been considered for this assignment purpose. So you wont see any pagination on the notes page. All the notes are fetched via a single API at once.
- No user authentication (login, signup, forgot password) has been added because of the time limit. The core features have been provided though.
- The reminders are not set up for time precision. Which means, a user might not get a reminder at the exact specified time. This is because the reminders are sent every 5 minutes via a scheduler.

## How to run the scheduler ?
Run the following commands:
```
> python app.py #to start the flask sever
> celery -A app.celery worker --pool=solo -l info
> celery -A app.celery beat -l info
```

