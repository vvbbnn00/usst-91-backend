from flask import Blueprint

bp = Blueprint("error_handler", __name__)


@bp.app_errorhandler(500)
def method_not_allowed(err):
    return {
               "code": 500,
               "msg": "Internal Server Error"
           }, 500


@bp.app_errorhandler(405)
def method_not_allowed(err):
    return {
               "code": 405,
               "msg": "Method Not Allowed"
           }, 405


@bp.app_errorhandler(404)
def method_not_allowed(err):
    return {
               "code": 404,
               "msg": "The requested URL was not found on the server."
           }, 404


@bp.app_errorhandler(403)
def method_not_allowed(err):
    return {
               "code": 403,
               "msg": "Permission Denied."
           }, 403
