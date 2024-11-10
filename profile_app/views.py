from django.http import JsonResponse
from django.views import View

class ProfileView(View):
    def get(self, request, pk):
        return JsonResponse({'message': f'Profilinformationen für Benutzer mit ID {pk}'})

class BusinessProfileView(View):
    def get(self, request):
        return JsonResponse({'message': 'Profilinformationen für alle Geschäftskunden'})

class CustomerProfileView(View):
    def get(self, request):
        return JsonResponse({'message': 'Profilinformationen für alle Endkunden'})