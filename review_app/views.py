from django.http import JsonResponse
from django.views import View


class ReviewView(View):
    def get(self, request, pk=None):
        if pk:
            return JsonResponse({'message': f'Details der Rezension mit ID {pk}'})
        else:
            return JsonResponse({'message': 'Liste aller Rezensionen'})

    def post(self, request):
        return JsonResponse({'message': 'Neue Rezension erstellt'})

    def patch(self, request, pk):
        return JsonResponse({'message': f'Rezension mit ID {pk} aktualisiert'})

    def delete(self, request, pk):
        return JsonResponse({'message': f'Rezension mit ID {pk} gelöscht'})