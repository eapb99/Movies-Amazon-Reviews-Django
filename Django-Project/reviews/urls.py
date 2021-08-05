from django.urls import path

from reviews.views import *

urlpatterns = [
    path('', GeneralFilterView.as_view(template_name='index.html',
                                       data=['Filtros Generales', ReportForm(), 'index', 'api-general']), name='index'),
    path('product/', ProductFilterView.as_view(template_name='product.html',
                                               data=['Filtro por Producto', FieldForm(), 'product', 'api-user']),
         name='product'),
    path('user/', UserFilterView.as_view(template_name='product.html',
                                         data=['Filtro por Usuario', FieldForm(), 'usuario', 'api-user']),
         name='usuario'),
    path('date/',
         DateFilterView.as_view(template_name='user.html', data=['Filtro por Fechas', FieldForm(), 'date', 'api-date']),
         name='date'),

    # api
    path('api/user/', usuario, name='api-user'),
    path('api/date/', date, name='api-date'),
    path('api/general/', generalfilter, name='api-general')
]
