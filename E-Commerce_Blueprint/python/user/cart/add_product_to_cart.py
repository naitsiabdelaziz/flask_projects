

from python.website.login.login_check import *
from python.database.flask_database import *

add_product = Blueprint('add_product', __name__)


# add product to the cart

@add_product.route('/add_product_to_cart/<id>', methods=['post', 'get'])
@is_user_logged_in
def add_product_to_cart(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT product_name FROM orders WHERE product_id = %s AND user_name = %s ", [id, session['user_username']])
    if result > 0:
        cur.close()
        flash('You can not add this product because its already added before!', 'danger')
        return redirect(url_for('cart.add_to_cart'))
    if result == 0:
        cur.execute("SELECT * FROM products WHERE id = %s", [id])
        product = cur.fetchone()
        product_id = product['id']
        product_name = product['product_name']
        product_price = product['price']
        product_discount = product['discount']
        product_files = product['files']
        user_name = session['user_username']
        cur.execute("SELECT id FROM users WHERE username = %s", [session['user_username']])
        res = cur.fetchone()
        user_id = res['id']
        cur.execute("INSERT INTO orders(user_id, user_name, status, product_id, quantity,\
                                     product_name, price, discount, files)\
                                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                    (user_id, user_name, 'Pending', product_id, 1, product_name, \
                     product_price, product_discount, product_files))
        mysql.connection.commit()
        cur.close()
        flash('Added successfully to your cart', 'success')
        return redirect(url_for('cart.add_to_cart'))
    return redirect(url_for('web_home.home'))