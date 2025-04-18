# DjangoProject

## Overview
DjangoProject is a multi-app Django-based web application designed as a modern online shop. It features user authentication, product management, shopping cart, blog, and a customizable homepage. The project uses Django 5.1.7 and is structured to separate concerns across several Django apps for maintainability and scalability.

## Features
- **User Authentication**: Registration, login, logout, and address management (`account` app).
- **Product Catalog**: Product listing, detail pages, categories, likes, and comments (`product` app).
- **Shopping Cart**: Add/remove products, order management, discounts, and payment simulation (`cart` app).
- **Blog**: Basic blogging functionality and contact form (`blog` app).
- **Homepage**: Landing page and general site navigation (`home` app).
- **Static & Media Management**: Organized static files (CSS, JS, images) and media uploads.
- **Responsive UI**: Utilizes Bootstrap and custom CSS for a modern, responsive design.
- **Caching**: Uses Redis for caching template fragments and improving performance.

## Project Structure
```
DjangoProject/
├── DjangoProject/        # Main project config (settings, urls, wsgi, asgi)
├── account/             # User accounts, authentication, and addresses
├── blog/                # Blog and contact functionality
├── cart/                # Shopping cart, orders, and payments
├── home/                # Homepage and general views
├── product/             # Product catalog, categories, likes, comments
├── statics/             # Static assets (css, js, images, libs)
├── templates/           # Shared HTML templates (base, includes)
├── media/               # Uploaded media files
├── db.sqlite3           # SQLite database (default)
├── manage.py            # Django management script
```

## Setup Instructions
1. **Clone the repository** and create a virtual environment:
   ```bash
   git clone <repo-url>
   cd DjangoProject
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
2. **Install dependencies** (create `requirements.txt` if not present):
   ```bash
   pip install django==5.1.7 widget-tweaks django-render-partial django-social-share redis
   ```
3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
6. **Access the app** at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Configuration
- **Settings**: Configured in `DjangoProject/settings.py`.
- **Database**: Uses SQLite by default; can be changed in settings.
- **Static & Media**: Static files in `statics/`, media uploads in `media/`.
- **Caching**: Requires Redis server running at `redis://127.0.0.1:6379`.
- **Custom User Model**: The project uses a custom user model (`account.User`).

## Main Dependencies
- Django 5.1.7
- widget-tweaks
- django-render-partial
- django-social-share
- redis (for caching)

## Apps
- `account`: User management (login, register, profile, address)
- `product`: Products, categories, likes, comments
- `cart`: Cart, orders, discounts, payments
- `blog`: Blog posts and contact form
- `home`: Homepage and general pages

## License
This project is for educational and demonstration purposes. Please review and update the license as needed.

---
*Generated on 2025-04-18*
