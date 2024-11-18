# Project Title

A minimal Django-based project with a RESTful API for book management and user interactions, including user authentication, book listing, book details, submitting reviews, and listing reviews for a particular book.

## Features
- User authentication (signup, login)
- View book listings
- Retrieve detailed information on individual books
- Submit reviews for books by authenticated users
- List reviews for a specific book

## Project Structure
```
root/
|-- bookstore/
|   |-- settings.py
|   |-- urls.py
|-- bookstorevault/
|   |-- models.py
|   |-- views.py
|   |-- serializers.py
|   |-- urls.py
|
|-- reviews/
|   |-- models.py
|   |-- views.py
|   |-- serializers.py
|   |-- urls.py
|
|-- users/
|   |-- models.py
|   |-- views.py
|   |-- serializers.py
|   |-- urls.py
||
|-- manage.py
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual_bookstore_django.git
```

2. Navigate to the project directory:
```bash
cd virtual_bookstore_django
```

3. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate # .\Scripts\activate for windows
```

4. Install the project dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Endpoints
### Postman collections
**you can find the postman collections with instructions under `postman/` directory where you will find collections of users app, booksvault app and reviews app**

### Auth Endpoints
**NOTE** 
### [WIP] Please note for now all users don't get verified for, so we've to do it manually.
- `POST v1/users/auth/signup/` - Register a new user
- `POST v1/users/auth/login/` - Log in and receive a token
- `POST v1/users/auth/token/refresh` - generate access and refresh token

### Book Endpoints
- `GET v1/books/list/` - List all books
- `GET v1/books/<book_id>/` - Retrieve details of a specific book

### Review Endpoints
- `POST v1/reviews/submit/` - Submit a review for a book (authenticated users only)
- `GET v1/reviews/book/<book_id>/` - List reviews for a specific book


## Testing
### Using Pytest
This project uses `pytest` for running tests. You can run the tests as follows:

1. Install `pytest`:
```bash
pip install pytest pytest-django
```

2. Run all tests in the parent directory of the project:
```bash
pytest
```

### Example Test Command
```bash
pytest --verbose --ds=project_name.settings
```

Ensure you have test cases in `tests/` directories within your app folders (e.g., `books/tests.py`, `reviews/tests.py`).



## Running the Project Using Docker

1. **Build the Docker image:**
   ```bash
   docker build -t virtual_bookstore:latest .
   ```

2. **Run the Docker container:**
  for now before using docker compose, we can run it on the local host so that the docker container can identify our local postgres and avoid different networks connectivity issues.
   ```bash
   docker run --network=host \
    -e DB_NAME=local_db_name \
    -e DB_USER=local_db_user \
    -e DB_PASSWORD=local_db_pw \
    -e DB_HOST=localhost \
    -e DB_PORT=5432 \
    --name bookstore-container \
    image_name:tag

   ```

3. **Access the API:**
   The API will be available at `http://localhost:8000`.



## Future Enhancements

1. **Implement email verification:** We will add an endpoint to verify user email addresses, enhancing security and user trust.
2. **Ensure that the authentication cycle is fully developed**
3. **Add `docker-compose` support:** We plan to add a `docker-compose.yml` file to streamline the development environment setup. 
4. **Add BookReading model** to keep track of users readings  
5. **Add Proper Logging middleware** Add request/response proper logging in the app
6. **Add Proper Throttling**

