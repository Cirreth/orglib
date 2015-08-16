import re
from app.models import Comment
from flask import render_template, request, url_for
# app
from app import app, Order
from flask_login import login_required, current_user
from webargs.flaskparser import abort
from werkzeug.utils import redirect


@app.route("/comment/add/<order_id>", methods=['POST'])
@login_required
def comment_add(order_id):
    text = request.form['text']
    c = Comment()
    o = Order.get(order_id)
    if not o:
        abort(404)
    c.text = text
    c.order_id = order_id
    c.user_login = current_user.login
    return redirect(url_for('main'))
