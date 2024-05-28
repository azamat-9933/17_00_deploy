from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from services.serializers import *


category_id = openapi.Parameter(
    'category_id',
    openapi.IN_QUERY,
    description="This path parameter is used to filter data by category id",
    type=openapi.TYPE_INTEGER,
)

for_home_page = openapi.Parameter(
    'for_home_page',
    openapi.IN_QUERY,
    description="This path parameter is used to filter data by home page",
    type=openapi.TYPE_BOOLEAN,
)



class ServiceHomeListView(ListAPIView):
    queryset = Service.objects.filter(is_home_page=True)
    serializer_class = ServiceHomeListSerializer


class ServiceCategoryListAPIView(ListAPIView):
    queryset = ServiceCategory.objects.filter(parent__isnull=True)
    serializer_class = ServiceCategoryListSerializer


class ServiceDetailView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceDetailSerializer


class OrderServiceAPIView(CreateAPIView):
    queryset = OrderService.objects.all()
    serializer_class = OrderServiceSerializer


class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer

    @swagger_auto_schema(manual_parameters=[category_id, for_home_page])
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id', None)
        for_home_page = request.GET.get('for_home_page', None)
        if category_id is not None:
            self.queryset = self.queryset.filter(category_id=category_id)

        if for_home_page is not None and for_home_page == 'true':
            self.queryset = self.queryset.filter(is_home_page=True)

        return super().get(request, *args, **kwargs)
