from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from slugify import slugify
from app import db
from app.models import Product, Category, Order

admin_bp = Blueprint("admin", __name__)

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.get("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html",
        products=Product.query.count(), orders=Order.query.count(),
        revenue=sum((o.total for o in Order.query.all()), 0))

@admin_bp.route("/products", methods=["GET", "POST"])
@admin_required
def products():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = request.form.get("price", type=float)
        stock = request.form.get("stock", type=int)
        category = Category.query.get(request.form.get("category_id", type=int))
        if not name or price is None or price <= 0 or stock is None or stock < 0 or not category:
            flash("Please provide valid product details.", "danger")
        else:
            db.session.add(Product(name=name, slug=slugify(name) + "-" + str(Product.query.count()+1),
                description=request.form.get("description", "").strip(), price=price,
                stock=stock, category=category, image_url=request.form.get("image_url", "").strip()))
            db.session.commit()
            flash("Product created.", "success")
            return redirect(url_for("admin.products"))
    return render_template("admin/products.html", products=Product.query.order_by(Product.id.desc()).all(),
        categories=Category.query.all())

@admin_bp.post("/products/<int:product_id>/toggle")
@admin_required
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.active = not product.active
    db.session.commit()
    return redirect(url_for("admin.products"))

@admin_bp.get("/orders")
@admin_required
def orders():
    return render_template("admin/orders.html", orders=Order.query.order_by(Order.created_at.desc()).all())

@admin_bp.post("/orders/<int:order_id>/status")
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get("status")
    if status in ["Placed", "Processing", "Shipped", "Delivered", "Cancelled"]:
        order.status = status
        db.session.commit()
    return redirect(url_for("admin.orders"))
