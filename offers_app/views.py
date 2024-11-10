from django.http import JsonResponse
from django.views import View

class OfferView(View):
    def get(self, request, pk=None):
        if pk:
            return JsonResponse({'message': f'Details des Angebots mit ID {pk}'})
        else:
            return JsonResponse({'message': 'Liste aller Angebote'})

    def post(self, request):
        return JsonResponse({'message': 'Neues Angebot erstellt'})

    def patch(self, request, pk):
        return JsonResponse({'message': f'Angebot mit ID {pk} aktualisiert'})

    def delete(self, request, pk):
        return JsonResponse({'message': f'Angebot mit ID {pk} gelöscht'})

class OfferDetailView(View):
    def get(self, request):
        return JsonResponse({'message': 'Liste aller Angebotsdetails'})