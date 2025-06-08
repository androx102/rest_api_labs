# Restaurant Application

Full-stack restaurant application with Django REST API backend and Vue.js frontend.

## Backend Setup

### 1. Python Environment Setup

Using venv (Option 1):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
```

Using Conda (Option 2):
```bash

#Install conda
#For linux
sudo apt install conda

#For MacOS
brew install --cask anaconda



# Create new conda environment
conda create -n restaurant_env python=3.10

# Activate conda environment
conda activate restaurant_env
```

### 2. Install Dependencies
```bash
# Navigate to project directory
cd restaurant_app

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
#Make migrations
python manage.py makemigrations rest_api

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## Frontend Setup

### 1. Install Node.js Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 2. Development Server
```bash
# Start development server
npm run serve
```

Frontend will be available at: http://localhost:8080/

### 3. Production Build
```bash
# Create production build
npm run build
```

## Netowrk
Backend will be available at: http://localhost:8000/
Frontend will be avaliable at: http://localhost:8080/
Admin interface: http://localhost:8000/admin
API Documentation: http://localhost:8000/swagger/

After crating production build of the frontend, everything is accesible under: http://localhost:8000/

## Testing

Backend:
```bash
python manage.py test
```
