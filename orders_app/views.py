from django.http import JsonResponse
from django.views import View


class OrderView(View):
    def get(self, request, pk=None):
        if pk:
            return JsonResponse({'message': f'Details der Bestellung mit ID {pk}'})
        else:
            return JsonResponse({'message': 'Liste aller Bestellungen'})

    def post(self, request):
        return JsonResponse({'message': 'Neue Bestellung erstellt'})

    def patch(self, request, pk):
        return JsonResponse({'message': f'Bestellung mit ID {pk} aktualisiert'})

    def delete(self, request, pk):
        return JsonResponse({'message': f'Bestellung mit ID {pk} gelöscht'})
    
class OrderCountView(View):
    def get(self, request, pk):
        return JsonResponse({'message': f'Anzahl der Bestellungen für Profil {pk}'})


class CompletedOrderCountView(View):
    def get(self, request, pk):
        return JsonResponse({'message': f'Anzahl abgeschlossener Bestellungen für Profil {pk}'})
