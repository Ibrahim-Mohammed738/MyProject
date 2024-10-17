# MyProject
Movie Review API
Project Overview
The Movie Review API allows users to:

Submit reviews for movies.
Rate movies on a scale.
View all submitted reviews.
Edit or delete reviews (only for the user who submitted them).
Securely log in and authenticate using token-based authentication.
This project is built with Django and the Django REST Framework. It demonstrates how to create, read, update, and delete (CRUD) movie reviews while using Django's built-in authentication system to associate reviews with users.

Features
Authentication: Token-based authentication with the Django REST framework. Only authenticated users can post, edit, or delete their reviews.
Review Submission: Users can submit a review along with a rating for a specific movie.
CRUD Operations: Users can create, retrieve, update, and delete their own reviews.
User Permissions: Users can edit or delete only their own reviews. Admin users have full access.
Movie Title Validation: Ensures that users can only review movies that exist in the system (case-insensitive validation).
Technologies Used
Backend Framework: Django, Django REST Framework
Database: SQLite (default Django database)
Authentication: Django Rest Framework's Token Authentication
Development Tools: Postman for API testing
Setup and Installation
Prerequisites
Python (version 3.8+)
Django (version 4.0+)
Django REST Framework (latest version)
Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/movie-review-api.git
cd movie-review-api
Set up a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply database migrations:

bash
Copy code
python manage.py migrate
Create a superuser (admin) account:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Open the API in your browser at:

arduino
Copy code
http://127.0.0.1:8000/
Endpoints
List Reviews: GET /main/reviews-list/
Create Review: POST /main/reviews-list/
Review Detail (Retrieve, Update, Delete): GET, PUT, DELETE /main/reviews-detail/<id>/
Usage
Register a new user or log in with an existing account.
Use the authentication token in the headers for any POST, PUT, or DELETE requests:
makefile
Copy code
Authorization: Token your_token_here
Submit reviews, update or delete your existing reviews.
Example API Request (Create Review):
bash
Copy code
POST /main/reviews-list/
{
   "movie_title": "Inception",
   "review_content": "Amazing movie with stunning visuals!",
   "rating": 5
}
Project Structure
graphql
Copy code
movie-review-api/
│
├── main/                # Main Django app for reviews
│   ├── migrations/      # Database migrations
│   ├── models.py        # Review model definitions
│   ├── serializers.py   # DRF serializers for reviews
│   ├── views.py         # API view logic
│   ├── urls.py          # API routes
│
├── movie_review/        # Django project configuration
│   ├── settings.py      # Project settings
│   ├── urls.py          # Project URL configurations
│
├── requirements.txt     # Python dependencies
├── manage.py            # Django management commands
└── README.md            # Project documentation
Future Enhancements
Add support for movie search and filtering.
Implement pagination for review lists.
Integrate third-party movie databases (like OMDB API) for real-time movie information.
Add user profile and activity tracking features.
License
This project is licensed under the MIT License.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Author
Ibrahim Mohammed