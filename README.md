# LevoNotes
Levonotes is a simple and clean note taking application. Built as a assignment under time constraint, it contains only the basic functionalities you would expect from a note taking app. The application allows users to create, update and delete a note. Users can also set reminders for a note for a specified date and time.

## Tech and Tools used
- Flask (Python)
- Svelte & SvelteKit
- SQLAlchemy
- PostgreSQL

## Features
- Create new notes
- Edit existing notes
- Delete notes
- Set a reminder

## Limitations
- Any of the scaling issues have not been considered for this assignment purpose. So you wont see any pagination on the notes page. All the notes are fetched via a single API at once.
- No user authentication (login, signup, forgot password) has been added because of the time limit. The core features have been provided though.
- The reminders are not set up for time precision. Which means, a user might not get a reminder at the exact specified time. This is because the online service I was trying to host the project on had limited features regarding celery or cron job setup. So, I had to do a less effective solution. The solution I came up with was: **Github Actions**. A github actions has been set up to run every 5 minutes on a schedule. One run of the action sends mail to all the due reminders from the database. 
