import datetime
import json
import random
import time
import csv
import os
from datetime import date

from flask import abort, flash, jsonify, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required
from pharmbase import app, db
from flask_paginate import Pagination, get_page_parameter
from . import admin
from pharmbase.admin.forms import DrugForm, MovementForm

from sqlalchemy.exc import IntegrityError
from pharmbase.models import User, Drug, Order



@admin.route('/')
@login_required
def admin_page():

    drug = Drug.query.count()
    total_number_of_drugs = drug
    return render_template('admin/dashboard/index.html', title='Dashboard', total_number_of_drugs=total_number_of_drugs)


@admin.route('/drugs', methods=['GET', 'POST'])
@login_required
def list_drugs():
    ROWS_PER_PAGE = 10

    page = request.args.get('page', 1, type=int)
    drugs = Drug.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('admin/dashboard/drugs.html',  title="Drugs", drugs=drugs)


@admin.route('/drugs/add', methods=['GET', 'POST'])
@login_required
def add_drug():

    form = DrugForm(request.form)

    if form.validate_on_submit():
        drug = Drug(name=form.name.data, description=form.description.data, date_added=datetime.datetime.now(
        ), quantity_received=form.quantity.data, available_quantity=form.quantity.data, expiry_date=form.expiry_date.data)
        db.session.add(drug)
        db.session.commit()
        flash('drug has been added successfully', 'success')
        return redirect(url_for('admin.list_drugs'))

    return render_template("admin/dashboard/drug.html", form=form, title="Add Drug")


@admin.route('drugs/<string:id>')
def single_drug(id):

    drug = Drug.query.get_or_404(id)
    name = drug.name
    expiry_date = drug.expiry_date
    expiry_date = expiry_date.date()
    current_date = datetime.date.today()
    def calculate_expirydate(expiry_date, current_date):
        result= expiry_date - current_date
        result= result.days      
        return result
    day = calculate_expirydate(expiry_date=expiry_date, current_date=current_date)
    # days_to_expire = day.calculate_expirydate( expiry_date, current_date)
    print(day)
    return render_template('admin/dashboard/single_drug.html', drug=drug, title=name, days_to_expire=day)


@admin.route('/drugs/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_drug(id):
    drug_to_be_deleted = Drug.query.get(id)
    name = drug_to_be_deleted.name
    db.session.delete(drug_to_be_deleted)
    db.session.commit()
    flash(f'{name} has been deleted')
    return redirect(url_for('admin.list_drugs'))


@admin.route('/dashboard/movement/<int:id>', methods=['GET', 'POST'])
@login_required
def movement(id):
    drug = Drug.query.get_or_404(id)

    form = MovementForm(request.form)

    if form.validate_on_submit():
        # name = form.drug.data
        # location = form.location.data
        quantity = form.quantity.data
        # print(name)
        current_quantity = drug.available_quantity

        def check_quantity(quantity, current_quantity):
            if quantity <= current_quantity:
                return True

        pass_check = check_quantity(
            quantity=quantity, current_quantity=current_quantity)
        if pass_check:
            update_drug = Drug.query.filter_by(id=id).first()
            print(update_drug)
            # new_quantity=
            # print(new_quantity)
            update_drug.available_quantity -= quantity
            db.session.commit()
            print(
                f'drug quantity has been updated, new quantity = {drug.available_quantity}')

            order = Order(drug_id=id, quantity_received=form.quantity.data,
                          location=form.location.data, time_shipped=datetime.datetime.now())
            db.session.add(order)
            db.session.commit()
            flash(f'Order has been made', 'success')
            return redirect(url_for('admin.list_drugs'))
        else:
            error = "reduce quantity to make an order"
            return render_template('admin/dashboard/movement.html',  drug=drug,  form=form, error=error, title="Move Drug")
    return render_template('admin/dashboard/movement.html', drug=drug,  form=form, title="Move Drug")


@admin.route('/orders')
@login_required
def list_orders():
    ROWS_PER_PAGE = 10

    page = request.args.get('page', 1, type=int)
    result = db.session.query(Order.id, Order.drug_id, Order.quantity_received, Order.location, Order.time_shipped, Drug.name).join(
        Order).filter(Order.drug_id == Drug.id).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('admin/dashboard/orders.html', title="Orders", result=result)


@admin.route('/charts')
def charting():
    # cur = mysql.get_db().cursor()
    
    drug_name= db.session.query(Drug.name)   
    labels = list()
    for row in drug_name:
        labels.append(row)
    physical_quantity = db.session.query(Drug.available_quantity).order_by(Drug.name) 
    values = list()
    for row in physical_quantity:
        values.append(row)

    line_labels = labels
    line_values = values
    return render_template('admin/dashboard/charts.html', title='Drugs and physical quantity in stock', max=700, labels=line_labels, values=line_values)
