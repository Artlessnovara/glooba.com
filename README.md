# GLOOBA 🌀

GLOOBA is a social media platform built with Flask and SQLite, inspired by modern social apps. This project was developed to showcase a full-stack application with user authentication, a dynamic home feed, and interactive post features.

## Features

-   **User Authentication:** Full registration, login, and session management flow.
-   **Onboarding:** Multi-step onboarding process including profile setup and personalization.
-   **Dynamic Home Feed:** A home feed that displays posts and stories from users.
-   **Post Interactions:** Users can like, glow, and share posts.
-   **Seamless UI:** A modern, non-carded UI inspired by leading social apps.

## Project Structure

The project is organized into a `glooba/backend` directory containing the Flask application.

-   `app.py`: The main application factory.
-   `models/`: SQLAlchemy database models.
-   `routes/`: (Placeholder for future blueprint organization)
-   `templates/`: Jinja2 HTML templates.
-   `static/`: CSS, JavaScript, and image assets.
-   `migrations/`: Flask-Migrate database migration scripts.

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r glooba/backend/requirements.txt
    ```

4.  **Set up the database:**
    From the `glooba/backend` directory, run the database migrations:
    ```bash
    cd glooba/backend
    export PYTHONPATH=/path/to/project/root
    export FLASK_APP=app:create_app
    flask db upgrade
    ```
    *Note: The `PYTHONPATH` should point to the directory containing the `glooba` folder.*

5.  **(Optional) Create dummy data:**
    To populate the application with sample users, stories, and posts, run the following command from the `glooba/backend` directory:
    ```bash
    flask create-dummy-data
    ```

## Running the Application

1.  Navigate to the `glooba/backend` directory.
2.  Set the necessary environment variables.
3.  Run the Flask development server:
    ```bash
    cd glooba/backend
    export PYTHONPATH=/path/to/project/root
    export FLASK_APP=app:create_app
    flask run
    ```
4.  Open your browser and navigate to `http://127.0.0.1:5000`.
