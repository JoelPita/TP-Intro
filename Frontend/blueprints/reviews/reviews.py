from flask import Blueprint, jsonify, render_template
from utils import api_URL
import requests

reviewsBp = Blueprint("reviewsBp", __name__, template_folder='templates')

@reviewsBp.route('/', methods=["GET", "POST"])
def reviews():
    return render_template('reviews.html')