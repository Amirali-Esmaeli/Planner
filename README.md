<div dir="rtl">

# پلنر توسعه فردی

## توضیحات
پلنر توسعه فردی یه وب‌اپلیکیشن مبتنی بر Djangoه که به کاربران کمک می‌کنه اهداف، عادت‌ها، وظایف، و دسته‌بندی‌هاشون رو مدیریت کنن. این پروژه شامل قابلیت‌هایی مثل فیلتر کردن اهداف و وظایف، صفحه‌بندی (Pagination)، تقویم رویدادها، تاریخچه عادت‌ها و وظایف، و یه API برای مدیریت عادت‌هاست. همچنین از API عمومی adviceslip.com برای نمایش نقل‌قول‌های انگیزشی استفاده می‌کنه.

این پروژه با MySQL کار می‌کنه و محیط‌های لوکال با داکر تنظیم شده. تست‌های واحد برای مدل‌ها، ویوها، و API نوشته شده تا کیفیت کد تضمین بشه.

## دمو
- **لینک دمو:** http://amiraliesmailii.pythonanywhere.com/
- **میزبانی:** پروژه روی PythonAnywhere با دیتابیس MySQL میزبانی شده.

## ویژگی‌ها
- **مدیریت اهداف:** ایجاد، ویرایش، حذف، و فیلتر اهداف با دسته‌بندی.
- **مدیریت عادت‌ها:** ثبت عادت‌های روزانه، هفتگی، و ماهانه با قابلیت تیک زدن.
- **مدیریت وظایف:** ایجاد، ویرایش، حذف، و فیلتر وظایف با اولویت و هدف ها.
- **دسته‌بندی‌ها:** سازمان‌دهی اهداف با دسته‌بندی‌های سفارشی.
- **تقویم:** نمایش رویدادهای وظایف و عادت‌ها.
- **تاریخچه:** بررسی وضعیت عادت‌ها و وظایف.
- **نقل‌قول انگیزشی:** نمایش نقل‌قول روزانه از adviceslip.com.
- **صفحه‌بندی:** نمایش ۳ آیتم در هر صفحه برای اهداف، عادت‌ها، و وظایف.
- **احراز هویت:** ثبت‌نام، ورود، خروج، تغییر رمز عبور و بازنشانی رمز عبور
- **تست:** تست‌ ها(Tests) برای اطمینان از عملکرد صحیح ویوها و مدل‌ها

## پیش‌نیازها
- **Python 3.11**
- **Git**(برای کلون کردن پروژه)
- **MySQL** (برای استفاده از دیتابیس MySQL در پروژه)
- **داکر و Docker Compose** (برای اجرای لوکال)

## نصب و راه‌اندازی (لوکال با داکر)
1. **نصب داکر:**
    - ویندوز/مک: Docker Desktop رو نصب کن.
    - لینوکس:
    ```bash
    sudo apt update
    sudo apt install docker.io
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    ```
    - نصب Docker Compose:
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```
2. **کلون کردن پروژه:**
    ```bash
    git clone https://github.com/Amirali-Esmaeli/Planner
    cd Planner
    ```
3. **ساخت و اجرای پروژه:**
    ```bash
    docker-compose up --build
    ```
    - پروژه روی http://localhost:8000 اجرا می‌شه.

4. **اجرای migrations:**
    ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

5. **تست پروژه:**
    - به http://localhost:8000 برو.

6. **اجرای تست‌ها:**
    ```bash
    docker-compose exec web python manage.py test core
    ```

7. **توقف کانتینرها:**
    ```bash
    docker-compose down
    ```

## نصب و راه‌اندازی (بدون داکر، لوکال)
1. **کلون کردن پروژه:**
   ```bash
   git clone https://github.com/Amirali-Esmaeli/Planner
   cd planner

2. **ایجاد محیط مجازی (اختیاری اما توصیه شده):**
    ```bash
    python -m venv venv
    ```
    در Windows:
    ```cmd
    venv\Scripts\activate
    ```
    در Linux/Mac:
    ```bash
    source venv/bin/activate
    ```

3. **نصب وابستگی‌ها:**
    ```bash
    pip install -r requirements.txt
    ```

5. **پیکربندی دیتابیس:**
    ```cmd
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'planner_db',  # نام دیتابیست رو بسازید
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }

6. **اجرای مهاجرت‌ها:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate

7. **ایجاد کاربر ادمین:**
    ```bash
    python manage.py createsuperuser

8. **اجرای پروژه:**
    ```bash
    python manage.py runserver
    ```
    برو http://127.0.0.1:8000/ حالا به آدرس 

9. **اجرای تست ها:**
    ```bash
    python manage.py test

**توسعه‌دهنده**

- **نام:** امیرعلی اسماعیلی  
- **ایمیل:** [amiraliesmaeli741@gmail.com](mailto:amiraliesmaeli741@gmail.com)  
- **گیت‌هاب:** [github.com/Amirali-Esmaeli](https://github.com/Amirali-Esmaeli?tab=repositories)
</div> 

# Personal Development Planner

## Overview
The Personal Development Planner is a Django-based web application designed to help users manage their goals, habits, tasks, and categories. It includes features like filtering goals and tasks, pagination, an event calendar, habit and task history, and a REST API for habit management. The app also integrates with the adviceslip.com API to display daily motivational quotes.

The project uses MySQL as the database and is configured for local development with Docker and deployment on PythonAnywhere (free tier). Unit tests for models, views, and APIs ensure code quality.

## Demo
- **Demo Link:** http://amiraliesmailii.pythonanywhere.com/
- **Hosting:** Hosted on PythonAnywhere with MySQL database.

## Features
- **Goal Management:** Create, edit, delete, and filter goals with categories.
- **Habit Management:** Track daily, weekly, or monthly habits with a toggle feature. 
- **Task Management:** Create, edit, delete, and filter tasks with priorities and associated goals.
- **Categories:**: Organize goals with custom categories.
- **Calendar:** Visualize tasks and habits as events.
- **History:** Review the status of habits and tasks.
- **Motivational Quotes:** Display daily quotes from adviceslip.com.
- **Pagination:** Display 3 items per page for goals, habits, and tasks.
- **Authentication**: Sign up, login, logout, password change, and password reset  
- **Unit Tests:**: Tests for views, models, and APIs to ensure functionality.

## Prerequisites
- **Python 3.11**
- **Git** For cloning the repository
- **MySQL** For the database
- **Docker and Docker Compose:** For local containerized setup

## Setup and Installation (Local with Docker)
1. **Install Docker:**
    - Windows/Mac: Install Docker Desktop.
    - Linux:
    ```bash
    sudo apt update
    sudo apt install docker.io
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    ```
    - Install Docker Compose:
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```
2. **Clone the Repository:**
    ```bash
    git clone https://github.com/Amirali-Esmaeli/Planner
    cd planner
    ```
3. **Build and Run:**
    ```bash
    docker-compose up --build
    ```
    - The app runs at http://localhost:8000.

4. **Run Migrations:**
    ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Test the App:**
    - Visit http://localhost:8000.

6. **Run Tests:**
    ```bash
    docker-compose exec web python manage.py test core
    ```

7. **Stop Containers:**
    ```bash
    docker-compose down
    ```
# Setup and Installation (Local without Docker)
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Amirali-Esmaeli/Planner.git
    cd Planner

2. **Create a Virtual Environment (optional but recommended):**
    ```bash
    python -m venv venv
    ```
    On Windows:
    ```cmd
    venv\Scripts\activate
    ```
    On Linux/Mac:
    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Configuration: In settings.py:**
   ```cmd
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'planner_db',  # Create your database
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
        }
    }

6. **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate

7. **Create Admin User:**
    ```bash
    python manage.py createsuperuser

8. **Run the Project:**
    ```bash
    python manage.py runserver
    ```
    Go to http://127.0.0.1:8000/.

9. **Run Tests:**
    ```bash
    python manage.py test 

**Developer**

- **Name**: Amirali Esmaili
- **Email**: [amiraliesmaeli741@gmail.com](mailto:amiraliesmaeli741@gmail.com)
- **GitHub**: [https://github.com/Amirali-Esmaeli](https://github.com/Amirali-Esmaeli?tab=repositories)

