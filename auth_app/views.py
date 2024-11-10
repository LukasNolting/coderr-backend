from django.http import JsonResponse
from django.views import View

class LoginView(View):
    def post(self, request):
        return JsonResponse({'message': 'Login erfolgreich'})


class RegistrationView(View):
    def post(self, request):
        return JsonResponse({'message': 'Registrierung erfolgreich'})