from app import create_app

app = create_app()

@functions_framework.http
def app(request):
    return app(request.environ, lambda x, y: y) 