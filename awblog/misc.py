from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('misc', __name__)

@bp.route('/about')
def about_me():
    return render_template('about.html', title="About Me")

@bp.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Information")

@bp.route('/donate')
def donate():
    return render_template('donate.html', title="Donate")