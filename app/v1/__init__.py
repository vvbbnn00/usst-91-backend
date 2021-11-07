import werkzeug
from flask import Blueprint, request
from app.v1.recriutment import bp as rec_bp
from app.v1.meet_table import bp as mtt_bp
from app.v1.welink import bp as wlk_bp
from utils.welink import *
from config import flaskConfig


def get_user_ip(request):
    if request.headers.get('X-Forwarded-For'):
        return request.headers['X-Forwarded-For']
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


class NestableBlueprint(Blueprint):
    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']
            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)

        self.record(deferred)


v1 = NestableBlueprint('v1', __name__, url_prefix='/v1')
v1.register_blueprint(rec_bp)
v1.register_blueprint(mtt_bp)
v1.register_blueprint(wlk_bp)


@v1.before_app_request
def sec_check():
    if request.method == "OPTIONS":
        return None
    need_welink_param = ['v1_welink.http_get_welink_card']  # 需要welink免登验证的函数
    need_welink_headers = ['v1_welink.http_get_calendar_list',
                           'v1_welink.http_add_calendar',
                           'v1_welink.http_delete_calendar',
                           'v1_meet_table.http_query_meet_table',
                           'v1_meet_table.http_count_meet_table',
                           'v1_recruitment.http_query_recruitment',
                           'v1_recruitment.http_count_recruitment']  # 需要welink Header免登验证的函数
    rep = request.endpoint

    if need_welink_param.__contains__(rep):
        code = request.args.get("code")
        if not code:
            raise werkzeug.exceptions.Forbidden
        if code == "development_header_token" and flaskConfig['ENV'] == 'development':
            return None
        welink_data = get_welink_user(code)
        if welink_data['code'] != 0:
            return welink_data, 403
        cache.set("welink_user_code_" + code, welink_data['welink_id'], ex=10)

    if need_welink_headers.__contains__(rep):
        code = request.headers.get("x-wlk-code")
        if not code:
            raise werkzeug.exceptions.Forbidden
        if code == "development_header_token" and flaskConfig['ENV'] == 'development':
            return None
        welink_data = get_welink_user(code)
        if welink_data['code'] != 0:
            return welink_data, 403
        cache.set("welink_user_code_" + code, welink_data['welink_id'], ex=10)
    return None
