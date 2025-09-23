**Deployed link:**  
[https://khayru-rafa-football-shop.pbp.cs.ui.ac.id](https://khayru-rafa-football-shop.pbp.cs.ui.ac.id)

step by step
1. Create Django Project and App
   - Started a new project `football_shop`.
   - Created app `main`.
   - Registered `main` inside `INSTALLED_APPS` in `settings.py`.

2. Define the Product Model
   - Added `Product` model in `main/models.py` with required fields:  
     `name`, `price`, `description`, `thumbnail`, `category`, `is_featured`.  
   - Added `id` (UUID primary key) for uniqueness.
   - Ran `python manage.py makemigrations` and `python manage.py migrate`.

3. Create Views
   - `show_main`: renders homepage with app name, my name, my class, and product list.
   - `create_product`: form page to add new product.
   - `show_product`: detail page for a single product.

4. Forms
   - Created `ProductForm` (ModelForm) in `forms.py` to simplify product creation.

5. Routing
   - Configured `main/urls.py` with paths for:
     - `""` → homepage (`show_main`)
     - `"create-product/"` → add form
     - `"product/<uuid:id>/"` → detail view
   - Included `main.urls` in `football_shop/urls.py`.

6. Templates
   - Created `base.html` (skeleton layout with pistachio green header).
   - Created `main.html` to display list of products with “Add” and “Detail” buttons.
   - Created `create_product.html` for form input.
   - Created `product_detail.html` for details of each product.

7. Deployment
   - Added `requirements.txt`, `Procfile`, and `runtime.txt`.
   - Pushed to GitHub and deployed to PWS.
   - Configured `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in `settings.py`.
   - Configured `DATABASES` to use PostgreSQL on PWS.
