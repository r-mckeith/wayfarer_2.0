from .models import City

cities = City.objects.all()


def add_variable_to_context(request):
    return {
        'testme': 'Hello world!',
        'cities': cities
    }