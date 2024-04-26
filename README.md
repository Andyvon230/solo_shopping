
# Shopping Site Project

Welcome to the repository for our Django-based shopping site. This project is designed to provide a comprehensive e-commerce platform with robust features for both users and administrators. Below you will find the necessary information to get started with setting up, developing, and contributing to the project.

## Features

- **Merchandise Listing**: Products are displayed with pagination and can be searched using specific criteria.
- **User Authentication**: Supports user registration, login, and logout, along with separate administrative access.
- **Shopping Cart**: Allows registered users to add, edit, and remove products before purchasing.
- **Checkout Process**: Facilitates the completion of purchases with integrated payment options.
- **Admin Dashboard**: Provides analytics and order management capabilities to administrators.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or later
- Django 3.2 or later
- PostgreSQL
- Additional Python packages as listed in `requirements.txt`

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/your-username/shopping-site.git
   cd shopping-site
   ```

2. **Set up a Python Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the Database**
   - Ensure PostgreSQL is running.
   - Create a database named `shopping_site_db`.
   - Configure database settings in `settings.py`.

5. **Run Migrations**
   ```
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```
   python manage.py runserver
   ```

## Usage

Access the web application at `http://127.0.0.1:8000/` in your browser to start using the shopping site.

## Testing

To run tests, use the following command:
```
python manage.py test
```
For behavior-driven development tests with Behave:
```
behave
```

## Contributing

Contributions are welcome! Please read our CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Support

For support, email contact@shopping-site.com or open an issue in the GitHub repository.

Feel free to fork the project, submit pull requests, and make this shopping site better for everyone!
