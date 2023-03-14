from flask import Blueprint, render_template
from application.models import shop

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html', products=shop.all_products())

@web.route('/view/<product_id>')
def product_details(product_id):
    return render_template('item.html', product=shop.select_by_id(product_id))