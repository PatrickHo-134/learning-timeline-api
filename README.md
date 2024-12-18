# Learning Timeline API [3.0.0]
This repository contains the backend API for the Learning Note application. The API is designed to manage learning notes, labels, and collections. It provides endpoints for creating, reading, updating, and deleting notes, as well as managing user authentication, note categorization through collections, and labeling features.

The API is built using Django and Django REST Framework (DRF), ensuring scalability, security, and ease of integration with the frontend. It also includes user management, collection archiving, and a robust system for associating labels with notes.

## Table of Contents
1. Prerequisites
2. Setup and Installation
3. API Documentation
4. Contributing
5. License


## Prerequisites

Before setting up and running the Learning Timeline API locally, ensure you have the following installed on your machine:

### 1. Python 3.8+
The backend is built with Python 3.8 or later. Ensure you have Python installed by running:

```
python --version
```

If Python is not installed, you can download it [here](https://www.python.org/downloads/).

### 2. Django
The project uses Django as the web framework. It will be installed automatically when you install the project dependencies (explained later).

Verify if Django is installed by running:
```
python -m django --version
```

### 3. Django REST Framework
This API uses Django REST Framework (DRF) for building RESTful endpoints. Like Django, this will also be installed with the project dependencies.

### 4. PostgreSQL
The project uses PostgreSQL as the database in production. You'll need to install and configure PostgreSQL on your machine. Ensure that you:
- Install PostgreSQL ([Download PostgreSQL](https://www.postgresql.org/download/))
- Set up a new database for the project
- Configure the connection details in the project's environment file.

### 5. Virtual Environment (Optional, but Recommended)
Using a Python virtual environment is recommended to manage dependencies. You can set up a virtual environment using venv or any preferred tool. For `venv`:

```
python -m venv venv
```

### 6. Environment Variables
The project requires some environment variables to be set. These include:
- `SECRET_KEY`: The secret key for your Django project.
- `DATABASE_URL`: The URL connection string to the PostgreSQL database.
- `DEBUG`: Set to True for development and False for production.

You can use a `.env` file to configure these variables locally.

### 7. pip
The project dependencies are managed with pip. Make sure pip is installed:

```
pip --version
```

If not, install pip by following the instructions [here](https://pip.pypa.io/en/stable/installation/).

## Setup and Installation

Follow these steps to set up the Learning Timeline API project on your local machine.

### 1. Clone the Repository
First, clone the backend repository from GitHub to your local machine using the following command:

```
git clone https://github.com/PatrickHo-134/learning-timeline-api.git
```

Navigate into the project directory:

```
cd learning-note-api
```

### 2. Set Up a Virtual Environment
It's recommended to use a virtual environment to isolate the project dependencies. You can create a virtual environment using the following command:

```
python -m venv venv
```

Activate the virtual environment:

On Windows:
```
venv\Scripts\activate
```

On macOS/Linux:

```
source venv/bin/activate
```

### 3. Install Dependencies
After activating the virtual environment, install the required dependencies using `pip`:

```
pip install -r requirements.txt
```

This command will install all necessary packages, including Django, Django REST Framework, and any other dependencies defined in the `requirements.txt` file.

### 4. Set Up Environment Variables
Create a `.env` file in the root directory of the project to store your environment variables. The `.env` file should contain the following variables:

```
SECRET_KEY=<your-secret-key>
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/YOUR_DATABASE_NAME
DEBUG=True
```

- Replace <your-secret-key> with a generated Django secret key (you can use this [tool](https://djecrety.ir/) to generate one).
- Replace USER, PASSWORD, localhost, and YOUR_DATABASE_NAME with your PostgreSQL credentials.
- Set DEBUG=True for local development and testing purposes.

### 5. Set Up PostgreSQL Database
Make sure you have PostgreSQL installed and running. Then, create a new PostgreSQL database:

```
psql
CREATE DATABASE your_database_name;
CREATE USER your_user WITH PASSWORD 'your_password';
ALTER ROLE your_user SET client_encoding TO 'utf8';
ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_user;
```

Replace your_database_name, your_user, and your_password with your actual database name, user, and password.

### 6. Run Migrations
Once your environment variables are set up and the database is created, apply the migrations to set up the database tables:

```
python manage.py migrate
```

### 7. Create a Superuser (Optional)
To access the Django admin interface, you can create a superuser by running:

```
python manage.py createsuperuser
```

Follow the prompts to set up the superuser account.

### 8. Start the Development Server
You can now run the development server locally using the following command:

```
python manage.py runserver
```

The API will be available at http://localhost:8000/. You can now test the available endpoints and interact with the API.

### 9. Access Django Admin Panel (Optional)
To access the Django Admin panel, navigate to http://localhost:8000/admin

Log in with the credentials of the superuser account you created earlier. Here, you can manage learning notes, labels, collections, and users.

### 10. Run Tests (Optional)
To ensure everything is working as expected, you can run the test suite using:

```
python manage.py test
```

This will run any unit tests included in the project to verify the core functionality.


7. API Documentation
Provide a brief description or link to the API documentation. You can either include a basic list of the available API endpoints or refer to an external documentation tool like Swagger, Postman, or ReDoc.

Example:

sql
Copy code

## API Documentation

To be updated

## Contributing

We welcome contributions to the Learning Timeline API! Whether it's fixing bugs, adding new features, improving documentation, or suggesting improvements, we appreciate your effort to help make this project better.

### How to Contribute

#### 1. Fork the Repository

Begin by forking the repository to your GitHub account.

```
git clone https://github.com/PatrickHo-134/learning-timeline-api.git
cd learning-note-api
```

#### 2. Set Up Your Local Environment

Ensure that the project is set up correctly on your machine. You can refer to the Setup and Installation section of this README to get started. Make sure that the tests run successfully before making changes.

```
# Create a virtual environment (if not already done)
python -m venv env

# Activate the virtual environment
source env/bin/activate  # On Linux/MacOS
# OR
.\env\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the test suite
python manage.py test
```

#### 3. Create a Branch

Create a new branch for your feature or bug fix. Choose a descriptive name for your branch that reflects the changes you're making.

```
git checkout -b feature/your-feature-name
```

#### 4. Make Your Changes

Now that your branch is set up, make the necessary code changes. Ensure you write clean, maintainable code and follow the coding standards used in the project.

- Code Style: Follow the PEP 8 guidelines for Python code.
- Testing: Ensure your code is covered by unit tests. This helps maintain the integrity of the codebase and ensures new contributions don't break existing functionality.

After making changes, run the test suite to verify everything works correctly:

```
python manage.py test
```

#### 5. Commit Your Changes

After you've made and tested your changes, commit your work. Write a clear and descriptive commit message that summarizes the changes you made.

```
git add .
git commit -m "Add feature to support pagination in learning notes API"
```

#### 6. Push Your Branch

Push your changes to your forked repository.

```
git push origin feature/your-feature-name
```

#### 7. Submit a Pull Request

Go to your forked repository on GitHub, and you'll see the option to open a Pull Request (PR). Submit your PR to the main branch of the original repository.

- Provide a detailed description of what you changed and why.
- Include references to any relevant issue tickets (e.g., Fixes #123).
- If your PR addresses part of a larger task, make sure to mention it.

One of the maintainers will review your PR, provide feedback if needed, and eventually merge it once it's approved.

### Guidelines for Contributions
To make the review process smoother and maintain the quality of the codebase, please adhere to the following guidelines:

- **Keep It Simple:** Stick to solving the problem or adding the specific feature at hand. Avoid making unnecessary changes.

- **Focus on Code Quality:** Ensure that your code is clean and maintainable. Follow the existing code structure and adhere to conventions used throughout the codebase.

- **Write Tests:** All new features or changes should be covered by unit tests. Ensure that existing tests pass and new tests adequately cover the functionality.

- **Documentation:** If your changes involve API modifications, make sure to update the relevant sections in the documentation. This includes updating docstrings, README files, or any relevant documentation pages.

- **Be Respectful:** We value a respectful and collaborative environment. Be open to feedback and willing to revise your PR based on suggestions from the maintainers.

### Reporting Issues
If you encounter a bug, have a feature request, or have any questions, feel free to open an issue on the GitHub repository. Please provide a detailed description of the issue and steps to reproduce if applicable.

1. Go to the Issues section of the repository.
2. Click "New Issue" and choose the appropriate template.
3. Provide detailed information and submit.

## License

This project is licensed under the MIT License.