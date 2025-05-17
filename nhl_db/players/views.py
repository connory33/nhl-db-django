from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Player
from .serializers import PlayerSerializer

class PlayerPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'
    max_page_size = 100

class PlayerListView(APIView):
    pagination_class = PlayerPagination
    
    def get(self, request):
        # Get query parameters for filtering
        filter_name = request.GET.get('filter_name', '')
        filter_team = request.GET.get('filter_team', '')
        filter_hand = request.GET.get('filter_hand', '')
        filter_country = request.GET.get('filter_country', '')
        filter_status = request.GET.get('filter_status', '')
        filter_number = request.GET.get('filter_number', '')
        filter_weight_min = request.GET.get('filter_weight_min', '')
        filter_weight_max = request.GET.get('filter_weight_max', '')
        search_term = request.GET.get('search_term', '')
        
        # Start with all players
        queryset = Player.objects.all()
        
        # Apply search term if provided
        if search_term:
            queryset = queryset.filter(
                Q(firstName__icontains=search_term) | 
                Q(lastName__icontains=search_term) |
                Q(firstName__icontains=search_term, lastName__icontains=search_term)
            )
        
        # Apply various filters
        if filter_name:
            queryset = queryset.filter(
                Q(firstName__icontains=filter_name) | 
                Q(lastName__icontains=filter_name) |
                Q(firstName__icontains=filter_name, lastName__icontains=filter_name)
            )
            
        if filter_team:
            queryset = queryset.filter(currentTeamID__triCode__icontains=filter_team)
            
        if filter_hand:
            queryset = queryset.filter(shootsCatches__icontains=filter_hand)
            
        if filter_country:
            queryset = queryset.filter(birthCountry__icontains=filter_country)
            
        if filter_status:
            queryset = queryset.filter(isActive=filter_status)
            
        if filter_number:
            queryset = queryset.filter(sweaterNumber=filter_number)
            
        if filter_weight_min:
            queryset = queryset.filter(weightInPounds__gte=filter_weight_min)
            
        if filter_weight_max:
            queryset = queryset.filter(weightInPounds__lte=filter_weight_max)
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        
        # Serialize the data
        serializer = PlayerSerializer(paginated_queryset, many=True)
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
