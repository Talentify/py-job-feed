from flask import render_template, Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'ok'})
