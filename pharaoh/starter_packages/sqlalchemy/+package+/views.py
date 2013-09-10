
from pyramid.view import view_config

@view_config(route_name='app_route', renderer='templates/template.pt')
def app_view(request):
    return {}

