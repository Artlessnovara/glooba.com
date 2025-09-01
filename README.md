# GLOOBA 🌀

GLOOBA is a social media platform built with Flask and SQLite, inspired by modern social apps. This project was developed to showcase a full-stack application with user authentication, a dynamic home feed, and interactive post features.

## Features

-   **User Authentication:** Full registration, login, and session management flow.
-   **Onboarding:** Multi-step onboarding process including profile setup and personalization.
-   **Dynamic Home Feed:** A home feed that displays posts and stories from users.
-   **Post Creation:** Users can create posts with text and upload images/videos.
-   **Post Interactions:** Users can like, comment, glow, and share posts.
-   **Seamless UI:** A modern, non-carded UI inspired by leading social apps.

## Project Structure

The project is organized into a `glooba/backend` directory containing the Flask application.

-   `app.py`: The main application factory.
-   `models/`: SQLAlchemy database models.
-   `templates/`: Jinja2 HTML templates.
-   `static/`: CSS, JavaScript, and image assets.
-   `migrations/`: Flask-Migrate database migration scripts.

## Setup and Installation

To run this project locally, please follow these steps carefully.

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment.
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r glooba/backend/requirements.txt
```

### 4. Configure Environment Variables
This is the most critical step. The application needs to know where to find its own packages.

**First, navigate into the `backend` directory:**
```bash
cd glooba/backend
```

**Next, set the required environment variables.** The `FLASK_APP` variable tells Flask how to load the application. The `PYTHONPATH` variable tells Python where to look for the `glooba` package.

**On macOS/Linux:**
```bash
export FLASK_APP=app:create_app
export PYTHONPATH=$(pwd)/../..
```
*(This sets the `PYTHONPATH` to the root of the project, two levels above the current `backend` directory.)*

**On Windows Command Prompt:**
```bash
set FLASK_APP=app:create_app
set PYTHONPATH=%cd%\..\..
```

**On Windows PowerShell:**
```bash
$env:FLASK_APP="app:create_app"
$env:PYTHONPATH=(Get-Location).Path + "\..\.."
```

### 5. Set Up the Database
With the environment variables set correctly, you can now create the database tables by running the migrations. **Make sure you are still inside the `glooba/backend` directory.**
```bash
flask db upgrade
```

### 6. (Optional) Create Dummy Data
To populate the application with sample users, stories, and posts, run the following command.
```bash
flask create-dummy-data
```

## Running the Application
1.  Ensure you are in the `glooba/backend` directory.
2.  Ensure your environment variables (`FLASK_APP` and `PYTHONPATH`) are set correctly as described in step 4.
3.  Run the Flask development server:
    ```bash
    flask run
    ```
4.  Open your browser and navigate to `http://127.0.0.1:5000`.
