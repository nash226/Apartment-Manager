import bcrypt
from database import DatabasePersistence
from functools import wraps
from flask import (
    flash,
    Flask,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import secrets
from utils import (
    validate_apartment_form,
    paginate,
    validate_tenant_form
)


app = Flask(__name__)
app.secret_key= secrets.token_hex(32)

db = DatabasePersistence()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("You must be signed in to view that page.", "error")

            return redirect(url_for("signin", next=request.full_path))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/users/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = db.find_user_by_username(username)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            session["username"] = username

            get_flashed_messages()

            flash("Welcome!", "success")
            next_page = request.form.get("next") or request.args.get("next")
            return redirect(next_page or url_for("list_apartments"))
        else:
            flash("Invalid username or password.", "error")
            return render_template("signin.html")

    return render_template("signin.html")

@app.route("/users/signout", methods=["GET", "POST"])
def signout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route('/')
@login_required
def index():
    return redirect(url_for('list_apartments'))

@app.route('/apartments')
@login_required
def list_apartments():
    apartments = db.all_apartments()

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        flash('Invalid page number, showing page 1')
        page = 1
        
    paged_apartments, page, total_pages, redirect_response = paginate(apartments, page, "list_apartments")

    if redirect_response:
        return redirect_response
    
    return render_template("apartments.html",
                           apartments=paged_apartments,
                           page=page,
                           total_pages=total_pages)

@app.route("/apartments/new", methods=["GET", "POST"])
@login_required
def new_apartment():
    if request.method == "POST":
        unit_number = request.form["unit_number"].strip()
        building_name = request.form["building_name"].strip().title()
        rent = request.form["rent"].strip()

        errors = validate_apartment_form(unit_number, building_name, rent, db)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("new_apartment.html",
                                   unit_number=unit_number,
                                   building_name=building_name,
                                   rent=rent)

        db.create_apartment(unit_number, building_name, rent)
        flash("Apartment created successfully!", "success")
        return redirect(url_for("list_apartments"))

    return render_template("new_apartment.html")


@app.route("/apartments/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_apartment(id):
    apt = db.find_apartment(id)
    if not apt:
        flash("Apartment not found.", "error")
        return redirect(url_for("list_apartments"))

    if request.method == "POST":
        unit_number = request.form["unit_number"].strip()
        building_name = request.form["building_name"].strip().title()
        rent = request.form["rent"].strip()

        errors = validate_apartment_form(unit_number, building_name, rent, db)

        if not errors:
            existing = db.find_apartment_by_unit_and_building(unit_number, building_name)
            if existing and existing["id"] != id:
                errors.append("Another apartment with that unit and building already exists.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("edit_apartment.html",
                                   apartment=apt,
                                   unit_number=unit_number,
                                   building_name=building_name,
                                   rent=rent)

        db.update_apartment(id, unit_number, building_name, rent)
        flash("Apartment updated successfully!", "success")
        return redirect(url_for("list_apartments"))

    return render_template("edit_apartment.html", apartment=apt)

@app.route("/apartments/<int:id>/delete", methods=["POST"])
@login_required
def delete_apartment(id):
    db.delete_apartment(id)
    flash("Apartment deleted successfully!", "success")
    return redirect(url_for("list_apartments"))

@app.route("/tenants")
@login_required
def list_tenants():
    tenants = db.all_tenants()

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        flash('Invalid page number, showing page 1')
        page = 1

    paged_tenants, page, total_pages, redirect_response = paginate(tenants, page, "list_tenants")

    if redirect_response:
        return redirect_response

    return render_template("tenants.html",
                           tenants=paged_tenants,
                           page=page,
                           total_pages=total_pages)

@app.route("/apartments/<int:id>/tenant/new", methods=["GET", "POST"])
@login_required
def new_tenant(id):
    apartments = db.all_apartments()

    if request.method == "POST":
        tenant_name = request.form["name"].strip()

        errors = validate_tenant_form(tenant_name, id)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "new_tenant.html",
                tenant_name=tenant_name,
                apartment_id=id,
                apartments=apartments
            )

        db.create_tenant(tenant_name, id)
        flash("Tenant added successfully!", "success")
        return redirect(url_for("list_apartments"))

    return render_template(
        "new_tenant.html",
        apartment_id=id,
        apartments=apartments
    )

@app.route("/tenants/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_tenant(id):
    tenant = db.find_tenant(id)
    if not tenant:
        flash("Tenant not found.", "error")
        return redirect(url_for("list_tenants"))

    if request.method == "POST":
        tenant_name = request.form["name"].strip()
        errors = validate_tenant_form(tenant_name, tenant["apartment_id"])

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("edit_tenant.html",
                                   tenant=tenant,
                                   tenant_name=tenant_name)

        db.update_tenant(id, tenant_name)
        flash("Tenant updated successfully!", "success")
        return redirect(url_for("list_tenants"))

    return render_template("edit_tenant.html",
                           tenant=tenant,
                           tenant_name=tenant["name"])

@app.route("/tenants/<int:id>/delete", methods=["POST"])
@login_required
def delete_tenant(id):
    tenant = db.find_tenant(id)
    if not tenant:
        flash("Tenant not found.", "error")
        return redirect(url_for("list_tenants"))

    db.delete_tenant(id)
    flash("Tenant deleted successfully!", "success")
    return redirect(url_for("list_tenants"))

@app.errorhandler(404)
def page_not_found(e):
    flash("The page you requested was not found.", "error")
    return redirect(url_for("list_apartments"))

@app.errorhandler(500)
def internal_error(e):
    flash("An unexpected error occurred. Please try again.", "error")
    return redirect(url_for("list_apartments"))


if __name__ == '__main__':
    app.run(debug=True, port=5003)