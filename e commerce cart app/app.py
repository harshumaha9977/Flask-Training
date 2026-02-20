from flask import Flask, render_template, session, redirect, url_for, request, flash
from config import Config
from models import db, Product, User, Order


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# ---------------- HOME ----------------
@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for("register"))

        new_user = User(
            full_name = full_name,
            username=username,
            email=email
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for("login"))

    return render_template("register.html")



# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("home"))



# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    orders = Order.query.filter_by(user_id=user.id).all()

    return render_template("profile.html", user=user, orders=orders)


# ---------------- ADD SAMPLE PRODUCTS ----------------
@app.route("/add-sample-products")
def add_products():
    if Product.query.count() == 0:
        p1 = Product(name="Laptop", price=50000, image="laptop.png")
        p2 = Product(name="Mobile", price=20000, image="mobile.jpeg")
        p3 = Product(name="Headphones", price=2000, image="headphones.jpeg")
        p4 = Product(name="Smart Watch", price=5000, image="watch.jpeg")

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        return "Sample products added!"
    else:
        return "Products already exist!"


# ---------------- ADD TO CART ----------------
@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product_id)
    session.modified = True

    return redirect(url_for("home"))


# ---------------- VIEW CART ----------------
@app.route("/cart")
def view_cart():
    cart_items = []
    total = 0

    if "cart" in session:
        for product_id in session["cart"]:
            product = Product.query.get(product_id)
            if product:
                cart_items.append(product)
                total += product.price

    return render_template("cart.html", cart_items=cart_items, total=total)


# ---------------- REMOVE FROM CART ----------------
@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    if "cart" in session:
        session["cart"].remove(product_id)
        session.modified = True

    return redirect(url_for("view_cart"))


# ---------------- CHECKOUT ----------------
# ---------------- CHECKOUT ----------------
@app.route("/checkout")
def checkout():
    if "user_id" not in session:
        flash("Please login to checkout.")
        return redirect(url_for("login"))

    if "cart" not in session or len(session["cart"]) == 0:
        flash("Cart is empty.")
        return redirect(url_for("home"))

    total = 0
    for product_id in session["cart"]:
        product = Product.query.get(product_id)
        if product:
            total += product.price

    new_order = Order(user_id=session["user_id"], total_amount=total)
    db.session.add(new_order)
    db.session.commit()

    session.pop("cart", None)

    flash("Order placed successfully!")
    return redirect(url_for("home"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
