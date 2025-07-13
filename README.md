# The Tennis Time

A modern, feature-rich blog application built with Django that allows users to read posts, register accounts, comment, and manage comments, with admin content management via Django's admin panel.

## 🚀 Features

### Blog Content
- **Paginated post list** with titles, excerpts, and images
- **Detailed post views** with rich text and approved comments
- **Search functionality** across posts, content, and authors
- **Responsive design** with modern UI/UX

### User Authentication
- **Signup, login, logout** using Django AllAuth
- **Email-based authentication** (no username required)
- **Custom authentication templates** with Bootstrap styling

### Comment System
- **Create, edit, delete comments** (user-specific)
- **Admin approval system** for comments
- **AJAX comment deletion** with confirmation
- **Comment moderation** with approval workflow

### Admin Management
- **Django admin panel** for posts, comments, users
- **Rich text editing** for posts using Django Summernote
- **Bulk comment approval/disapproval** actions
- **Image upload support** for posts and About page

### Technical Features
- **PostgreSQL database** support (with SQLite for development)
- **Cloudinary integration** for image hosting
- **Whitenoise** for static file serving
- **Responsive Bootstrap 5** design
- **Custom CSS/JavaScript** for enhanced UX
- **Comprehensive test suite**

## 🛠️ Technology Stack

- **Framework**: Django 5.2.3 (Python)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Image Hosting**: Cloudinary
- **Deployment**: Heroku
- **Authentication**: Django AllAuth
- **Form Styling**: Django Crispy Forms (Bootstrap 4)
- **Rich Text**: Django Summernote
- **Static Files**: Whitenoise
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JS

## 📋 Prerequisites

- Python 3.11+
- pip
- Git
- PostgreSQL (for production)
- Cloudinary account (for production)
- Heroku account (for deployment)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Django-Post
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (for local development)
DATABASE_URL=sqlite:///db.sqlite3

# Cloudinary (for production)
CLOUDINARY_URL=cloudinary://your-cloudinary-url

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see your blog!

## 🗄️ Database Models

### Post Model
- `title`: Post title (CharField, unique)
- `slug`: URL-friendly title (SlugField, unique)
- `author`: Foreign key to User
- `content`: Rich text content (TextField)
- `created_on`: Creation timestamp (DateTimeField)
- `image`: Optional post image (ImageField)
- `excerpt`: Short excerpt (TextField, optional)

### Comment Model
- `post`: Foreign key to Post
- `user`: Foreign key to User
- `content`: Comment text (TextField)
- `created_on`: Creation timestamp (DateTimeField)
- `approved`: Approval status (BooleanField)

### About Model
- `title`: Page title (CharField)
- `content`: Rich text content (TextField)
- `updated_on`: Last update timestamp (DateTimeField)
- `image`: Optional page image (ImageField)

## 🎨 Customization

### Styling
- Custom CSS in `static/css/style.css`
- Bootstrap 5 with custom theme
- Responsive design for all devices
- Modern gradient buttons and hover effects

### JavaScript Features
- AJAX comment deletion
- Auto-resizing comment forms
- Character counters
- Back-to-top button
- Keyboard shortcuts (Ctrl+K for search)
- Reading time calculator
- Social sharing functionality

### Templates
- Base template with navigation
- Post list with pagination and search
- Post detail with comments
- About page with dynamic content
- Custom authentication templates

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

The application includes comprehensive tests for:
- Model creation and methods
- Form validation
- View functionality
- Authentication and permissions
- Comment CRUD operations

## 🚀 Deployment to Heroku

### 1. Heroku Setup
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini
```

### 2. Environment Variables
Set environment variables in Heroku:
```bash
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False
heroku config:set CLOUDINARY_URL=your-cloudinary-url
```

### 3. Deploy
```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial deployment"

# Push to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput
```

### 4. Open Application
```bash
heroku open
```

## 📁 Project Structure

```
Django-Post/
├── config/               # Main project settings
│   ├── models.py        # Post and Comment models
│   ├── views.py         # Blog views
│   ├── forms.py         # Comment form
│   ├── admin.py         # Admin configuration
│   ├── urls.py          # URL patterns
│   └── tests.py         # Test cases
├── about/               # About app
│   ├── models.py        # About model
│   ├── views.py         # About view
│   ├── admin.py         # Admin configuration
│   └── urls.py          # URL patterns
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── blog/            # Blog templates
│   ├── about/           # About templates
│   └── account/         # Auth templates
├── static/              # Static files
│   ├── css/style.css    # Custom CSS
│   └── js/main.js       # Custom JavaScript
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment
├── runtime.txt         # Python version
└── README.md           # This file
```

## 🔧 Configuration

### Django Settings
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Configure for your domain
- **DATABASE_URL**: Automatically configured by Heroku
- **STATIC_ROOT**: Set to `staticfiles` for production

### AllAuth Configuration
- Email-based authentication
- No username required
- Email verification disabled (can be enabled)
- Custom login/logout redirects

### Summernote Configuration
- Rich text editor for post content
- Custom toolbar configuration
- Image upload support
- Code view and fullscreen modes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/Django-Post/issues) page
2. Create a new issue with detailed information
3. Contact the development team

---

**Built with ❤️ using Django and modern web technologies** 