from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Product, CartItem, Order, OrderItem, Review

shop_bp = Blueprint("shop", __name__)

@shop_bp.get("/product/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, active=True).first_or_404()
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
    return render_template("shop/product.html", product=product, reviews=reviews)

@shop_bp.post("/cart/add/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.filter_by(id=product_id, active=True).first_or_404()
    qty = max(1, request.form.get("quantity", 1, type=int))
    if qty > product.stock:
        flash("Requested quantity is not available.", "warning")
        return redirect(request.referrer or url_for("main.index"))
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if item:
        if item.quantity + qty > product.stock:
            flash("Not enough stock for that quantity.", "warning")
            return redirect(request.referrer or url_for("main.index"))
        item.quantity += qty
    else:
        db.session.add(CartItem(user_id=current_user.id, product_id=product.id, quantity=qty))
    db.session.commit()
    flash("Added to cart.", "success")
    return redirect(request.referrer or url_for("main.index"))

@shop_bp.get("/cart")
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum((i.product.price * i.quantity for i in items), Decimal("0.00"))
    return render_template("shop/cart.html", items=items, total=total)

@shop_bp.post("/cart/update/<int:item_id>")
@login_required
def update_cart(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    qty = request.form.get("quantity", 1, type=int)
    if qty <= 0:
        db.session.delete(item)
    elif qty <= item.product.stock:
        item.quantity = qty
    else:
        flash("Quantity exceeds available stock.", "warning")
    db.session.commit()
    return redirect(url_for("shop.cart"))

@shop_bp.post("/cart/remove/<int:item_id>")
@login_required
def remove_cart_item(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("shop.cart"))

@shop_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash("Your cart is empty.", "info")
        return redirect(url_for("shop.cart"))
    total = sum((i.product.price * i.quantity for i in items), Decimal("0.00"))
    if request.method == "POST":
        address = request.form.get("address", "").strip()
        if len(address) < 12:
            flash("Please enter a complete shipping address.", "danger")
            return render_template("shop/checkout.html", items=items, total=total)
        # Re-check inventory at checkout to avoid stale cart quantities.
        for item in items:
            if item.quantity > item.product.stock:
                flash(f"Insufficient stock for {item.product.name}. Update your cart.", "danger")
                return redirect(url_for("shop.cart"))
        order = Order(user_id=current_user.id, total=total, shipping_address=address)
        db.session.add(order)
        db.session.flush()
        for item in items:
            db.session.add(OrderItem(order_id=order.id, product_id=item.product_id,
                product_name=item.product.name, unit_price=item.product.price, quantity=item.quantity))
            item.product.stock -= item.quantity
            db.session.delete(item)
        db.session.commit()
        flash(f"Order #{order.id} placed successfully. Payment is set to Cash on Delivery for this demo.", "success")
        return redirect(url_for("shop.orders"))
    return render_template("shop/checkout.html", items=items, total=total)

@shop_bp.get("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("shop/orders.html", orders=orders)

@shop_bp.post("/review/<int:product_id>")
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "").strip()
    if rating not in range(1, 6):
        flash("Choose a rating from 1 to 5.", "danger")
    else:
        existing = Review.query.filter_by(user_id=current_user.id, product_id=product.id).first()
        if existing:
            existing.rating, existing.comment = rating, comment
        else:
            db.session.add(Review(user_id=current_user.id, product_id=product.id, rating=rating, comment=comment))
        db.session.commit()
        flash("Review saved.", "success")
    return redirect(url_for("shop.product_detail", slug=product.slug))
