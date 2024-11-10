from django.http import JsonResponse
from django.views import View

class BaseInfoView(View):
    def get(self, request):
        return JsonResponse({'message': 'Basisinformationen für die Anwendung'})