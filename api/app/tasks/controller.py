# Import flask dependencies
from flask import Blueprint, request, make_response, Response

# from .lstm import LSTM
# from .yahoo import Finance

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod = Blueprint('auth', __name__, url_prefix='/finance')


@mod.route('/')
def main_index():
    return 'hello world 123'