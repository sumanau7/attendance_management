from app import app
from app import views

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(views.AttendanceAPI, 'attendance_api', '/attendance/')
register_api(views.BreakAPI, 'break_api', '/breaks/')

if __name__ == '__main__':
    app.run(debug=True)