from flask import Blueprint, render_template, request
from sqlalchemy import or_
from app.models import Product, Category

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    q = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    query = Product.query.filter_by(active=True)
    if q:
        query = query.filter(or_(Product.name.ilike(f"%{q}%"), Product.description.ilike(f"%{q}%")))
    if category_id:
        query = query.filter_by(category_id=category_id)
    products = query.order_by(Product.created_at.desc()).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template("index.html", products=products, categories=categories, q=q, category_id=category_id)
