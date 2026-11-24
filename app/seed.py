from slugify import slugify
from app import db
from app.models import User, Category, Product

def seed_database():
    if Category.query.first():
        return
    categories = {}
    for name in ["Electronics", "Fashion", "Home & Living", "Books"]:
        c = Category(name=name, slug=slugify(name))
        db.session.add(c)
        categories[name] = c
    db.session.flush()
    samples = [
        ("Wireless Headphones", "Immersive sound, comfortable fit and long battery life.", 2499, 25, "Electronics", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=900"),
        ("Smart Watch", "Track your activity, notifications and daily goals.", 3999, 18, "Electronics", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=900"),
        ("Everyday Backpack", "A durable, minimalist backpack for work and travel.", 1499, 40, "Fashion", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=900"),
        ("Desk Lamp", "Warm adjustable lighting for your workspace.", 999, 30, "Home & Living", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=900"),
        ("Clean Code", "A practical guide to writing maintainable software.", 699, 15, "Books", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=900"),
        ("Running Shoes", "Lightweight everyday trainers with cushioned support.", 2899, 22, "Fashion", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=900"),
    ]
    for name, desc, price, stock, cat, image in samples:
        db.session.add(Product(name=name, slug=slugify(name), description=desc,
            price=price, stock=stock, category=categories[cat], image_url=image))
    admin = User(name="ShopVerse Admin", email="admin@shopverse.local", role="admin")
    admin.set_password("Admin@12345")
    db.session.add(admin)
    db.session.commit()
