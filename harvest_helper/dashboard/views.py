# dashboard/views.py
import requests
from django.conf import settings
from django.http import JsonResponse
from .models import MarketPrice, FeaturedCrop

def get_weather(request):
    # Get location from query params (e.g., ?lat=30.31&lon=78.03)
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and Longitude are required'}, status=400)

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={settings.WEATHER_API_KEY}"
        response = requests.get(url)
        response.raise_for_status() # Raises an error for bad responses
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_market_prices(request):
    mandi = request.GET.get('mandi', 'Dehradun')
    try:
        # Query your database
        prices = MarketPrice.objects.filter(mandi=mandi).order_by('-last_updated')[:4] # Get top 4
        
        # Format for JSON
        data = [
            {
                'crop': p.crop,
                'variety': p.variety,
                'price': f"₹ {p.price:,.0f}", # Format as "₹ 3,800"
                'trend': p.get_trend_display(), # Gets the human-readable value (e.g., "Up")
                'trend_icon': 'trending-up' if p.trend in ['UP', 'STABLE', 'HIGH'] else 'trending-down'
            } 
            for p in prices
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# <-- FIX: This function must be at the top level (no indentation)
def get_featured_crops(request):
    district = request.GET.get('district', 'general')
    try:
        # Try to find district-specific crops
        crops = FeaturedCrop.objects.filter(district__iexact=district)
        if not crops.exists():
            # If none, get the 'general' ones
            crops = FeaturedCrop.objects.filter(district__isnull=True)

        data = [
            {
                'name': c.name,
                'desc': c.description,
                'tag': c.tag,
                'searchTerm': c.image_search_term
            }
            for c in crops[:3] # Get top 3
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)