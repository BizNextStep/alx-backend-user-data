# Session Authentication API

This project demonstrates the implementation of a simple session-based authentication system using Flask. The API allows for basic CRUD operations on user data and includes an endpoint for retrieving the authenticated user's data.

## Features

- **User Authentication**: Basic authentication to access user data.
- **User Management**: Create, read, update, and delete user records.
- **Current User Endpoint**: Retrieve data for the currently authenticated user.

## Setup

- Clone the repository.
- Install dependencies using `pip install -r requirements.txt`.
- Run the application using the command: `API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app`.

## Usage

- Access the API endpoints using tools like `curl` or Postman.
- Use the `/api/v1/users/me` endpoint to retrieve data for the authenticated user.


