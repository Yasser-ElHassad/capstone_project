# Task Management API Documentation



## Project Overview

The Task Management API is a robust backend solution built with Django and Django REST Framework. It provides a set of endpoints for managing tasks, including creating, updating, deleting, and marking tasks as complete or incomplete. The API also includes user authentication and authorization features to ensure that users can only access and modify their own tasks.

Key Features:
- User registration and authentication
- CRUD operations for tasks
- Marking tasks as complete or incomplete
- Filtering and sorting tasks
- Token-based authentication for secure API access

## Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- virtualenv (recommended for creating isolated Python environments)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/task-management-api.git
   cd task-management-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

The API should now be accessible at `http://localhost:8000/api/`.

## API Endpoints

### User Management

- `POST /api/users/`: Register a new user
  - Required fields: `username`, `email`, `password`
  - Returns: User details and authentication token

- `GET /api/users/`: List all users (admin only)
- `GET /api/users/{id}/`: Retrieve a specific user (admin or owner)
- `PUT /api/users/{id}/`: Update a user (admin or owner)
- `DELETE /api/users/{id}/`: Delete a user (admin or owner)

### Authentication

- `POST /api/login/`: Obtain an authentication token
  - Required fields: `username`, `password`
  - Returns: Authentication token

### Task Management

- `GET /api/tasks/`: List all tasks for the authenticated user
- `POST /api/tasks/`: Create a new task
  - Required fields: `title`, `due_date`
  - Optional fields: `description`, `priority`, `status`

- `GET /api/tasks/{id}/`: Retrieve a specific task
- `PUT /api/tasks/{id}/`: Update a task
- `DELETE /api/tasks/{id}/`: Delete a task

- `POST /api/tasks/{id}/mark_complete/`: Mark a task as complete
- `POST /api/tasks/{id}/mark_incomplete/`: Mark a task as incomplete

## Models

### User

The API uses Django's built-in User model, which includes the following fields:
- `username`
- `email`
- `password`

### Task

- `title`: CharField, max length 200 characters
- `description`: TextField, optional
- `due_date`: DateTimeField
- `priority`: CharField with choices (LOW, MEDIUM, HIGH), default MEDIUM
- `status`: CharField with choices (PENDING, COMPLETED), default PENDING
- `user`: ForeignKey to User model
- `created_at`: DateTimeField, auto-generated
- `updated_at`: DateTimeField, auto-updated
- `completed_at`: DateTimeField, null=True, blank=True

## Authentication

The API uses token-based authentication. To access protected endpoints, include the token in the Authorization header of your requests:

```
Authorization: Token <your_token_here>
```

## Filtering and Sorting

You can filter and sort tasks using query parameters:

- Filter by status: `?status=PENDING` or `?status=COMPLETED`
- Filter by priority: `?priority=LOW`, `?priority=MEDIUM`, or `?priority=HIGH`
- Filter by due date: `?due_date=YYYY-MM-DD`
- Sort by due date: `?sort_by=due_date`
- Sort by priority: `?sort_by=priority`

Example: `GET /api/tasks/?status=PENDING&sort_by=due_date`

## Deployment

The project is configured for deployment on Heroku. To deploy:

1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku CLI: `heroku login`
3. Create a new Heroku app: `heroku create your-app-name`
4. Set environment variables:
   ```
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your_secret_key_here
   ```
5. Push to Heroku: `git push heroku main`
6. Run migrations: `heroku run python manage.py migrate`

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- 200: OK - The request was successful
- 201: Created - A new resource was successfully created
- 400: Bad Request - The request was invalid or cannot be served
- 401: Unauthorized - Authentication is required and has failed or has not been provided
- 403: Forbidden - The request is understood, but it has been refused or access is not allowed
- 404: Not Found - The requested resource could not be found
- 500: Internal Server Error - The server encountered an unexpected condition

Detailed error messages are provided in the response body for client errors (4xx status codes).

## Future Enhancements

- Implement refresh tokens for enhanced security
- Add support for task categories or tags
- Develop team collaboration features
- Create a front-end application to interact with the API

For any questions or issues, please open an issue on the GitHub repository or contact the project maintainers.