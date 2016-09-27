# coding: utf-8
"""
    stripe for heroku
    ~~~~~~~~~~~~~~~~~

    A simple stripe charge system on heroku

    :copyright: (c) 2016 by Hsiaoming Yang
"""
import os
import stripe
from flask import Flask, request, session
from flask import render_template, Response, redirect, send_from_directory

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')

stripe_pub_key = os.environ['STRIPE_PUB_KEY']
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


@app.route('/')
def index():
    amount = request.args.get('amount', 0)
    reason = request.args.get('reason', '')
    try:
        amount = int(amount * 100)
    except:
        amount = 0

    session['reason'] = reason
    session['amount'] = amount
    return render_template(
        'index.html',
        key=stripe_pub_key,
        amount=amount,
        reason=reason,
    )


@app.route('/charge', methods=['GET', 'POST'])
def charge():
    if request.method == 'GET':
        return redirect('/')
    email = request.form['stripeEmail']
    token = request.form['stripeToken']
    reason = session.get('reason') or 'A Charge'
    amount = int(session['amount'])
    stripe.Charge.create(
        receipt_email=email,
        source=token,
        amount=amount,
        currency='usd',
        description=reason,
    )
    return render_template('success.html')


@app.route('/robots.txt')
def robots():
    text = 'User-Agent: *\nDisallow: /\n'
    return Response(text, mimetype='text/plain')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.root_path, 'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
