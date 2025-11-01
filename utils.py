from flask import (
    flash,
    redirect,
    url_for
)
import re

def paginate(items, page, endpoint, page_size=5):
    """Paginate a list of items. Returns (paged_items, page, total_pages, redirect)."""
    total_pages = (len(items) + page_size - 1) // page_size or 1

    if page < 1 or page > total_pages:
        flash("Invalid page number, showing page 1.", "error")
        redirect_response = redirect(url_for(endpoint, page=1))
        return None, None, None, redirect_response

    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], page, total_pages, None


def validate_apartment_form(unit_number, building_name, rent, db):
    errors = []
    MAX_RENT = 999999.99

    if not unit_number:
        errors.append("Unit number is required.")
    elif not re.match(r'^[0-9]+[A-Za-z]?$' , unit_number):
        errors.append("Unit number must be numeric, optionally with one letter (e.g., 101, 3B).")

    if not building_name:
        errors.append("Building name is required.")

    if not rent:
        errors.append("Rent is required.")
    else:
        try:
            rent_val = float(rent)
            if rent_val <= 0:
                errors.append("Rent must be a positive number.")
            elif rent_val > MAX_RENT:
                errors.append(f"Rent cannot exceed {MAX_RENT:,.2f}.")
        except ValueError:
            errors.append("Rent must be a valid number.")
    
    if not errors:
        existing = db.find_apartment_by_unit_and_building(unit_number, building_name)
        if existing:
            errors.append("An apartment with that unit and building already exists.")

    return errors


def validate_tenant_form(name, apartment_id):
    errors = []

    if not name:
        errors.append("Tenant name is required.")
    elif not re.search(r"[A-Za-z]", name):
        errors.append("Tenant name must include at least one letter.")

    if not apartment_id:
        errors.append("Apartment is required.")
    
    return errors
