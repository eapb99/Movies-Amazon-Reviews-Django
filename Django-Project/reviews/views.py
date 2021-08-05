import datetime

from django.http import JsonResponse
from django.db import connection
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import TemplateView
from .utils import *


class ContextMixin(object):
    data = None
    context = {}

    def get_context_data(self):
        self.context['title'] = self.data[0]
        self.context['form'] = self.data[1]
        self.context['list_url'] = reverse_lazy(self.data[2])
        self.context['fetch'] = reverse_lazy(self.data[3])
        return self.context


class GeneralFilterView(ContextMixin, TemplateView):
    pass


class ProductFilterView(ContextMixin, TemplateView):
    pass


class UserFilterView(ContextMixin, TemplateView):
    pass


class DateFilterView(ContextMixin, TemplateView):
    pass


def response(qs1, qs2, values):
    if len(qs1) and len(qs2) and len(values):
        return JsonResponse(
            {'data': [qs1, qs2],
             'cantidad': {'Registros': values[0], 'Score Maximo': values[1], 'Score Minimo': values[3],
                          'Score Promedio': round(values[2], 2)}},
            safe=False)
    else:
        return JsonResponse(
            {'data': '',
             'cantidad': 0},
            safe=False)


def usuario(request):
    if request.method == 'POST':
        print('dentro')
        field = request.POST.get('dato')
        extra = request.POST.get('valor')
        with connection.cursor() as cursor:
            if field != '':
                if extra == 'user':
                    cursor.execute(queryUser('a'), [field])
                    qs1 = cursor.fetchall()
                    cursor.execute(queryUser('d'), [field])
                    qs2 = cursor.fetchall()
                else:
                    cursor.execute(queryProduct('a'), [field])
                    qs1 = cursor.fetchall()
                    cursor.execute(queryProduct('d'), [field])
                    qs2 = cursor.fetchall()
            else:
                cursor.execute(GLOBAL_QUERY + ORDER_ASC, [field])
                qs1 = cursor.fetchall()
                cursor.execute(GLOBAL_QUERY + ORDER_DESC, [field])
                qs2 = cursor.fetchall()
            if extra == 'user':
                qs = METRIC_QUERY + WHERE_CLAUSE + USER_FIELD + """ = %s"""
            else:
                qs = METRIC_QUERY + WHERE_CLAUSE + PRODUCT_FIELD + """ = %s"""
            cursor.execute(qs, [field])
            values = cursor.fetchone()
            cursor.close()
        print('saliendo')
        return response(qs1, qs2, values)


def date(request):
    if request.method == 'POST':
        a = request.POST.get('start')
        b = request.POST.get('end')
        start = ''
        end = ''
        if a and b != '':
            a = a.split("-")
            b = b.split("-")
            start = datetime.date(int(a[0]), int(a[1]), int(a[2]))
            end = datetime.date(int(b[0]), int(b[1]), int(b[2]))
        print(datetime.datetime.now())
        with connection.cursor() as cursor:
            if a != '' and b != '':
                cursor.execute(
                    GLOBAL_QUERY + WHERE_CLAUSE + ' "reviews"."timed" BETWEEN %s AND %s ' + ORDER_ASC,
                    [start, end])
                qs1 = cursor.fetchall()
                cursor.execute(
                    GLOBAL_QUERY + WHERE_CLAUSE + ' "reviews"."timed" BETWEEN %s AND %s ' + ORDER_DESC,
                    [start, end])
                qs2 = cursor.fetchall()
            else:
                cursor.execute(GLOBAL_QUERY + ORDER_ASC)
                qs1 = cursor.fetchall()
                cursor.execute(GLOBAL_QUERY + ORDER_DESC)
                qs2 = cursor.fetchall()
            qs = METRIC_QUERY + WHERE_CLAUSE + """ "reviews"."timed" BETWEEN %s AND %s"""
            cursor.execute(qs, [start, end])
            values = cursor.fetchone()
            cursor.close()
        print(datetime.datetime.now())
        return response(qs1, qs2, values)


def generalfilter(request):
    if request.method == 'POST':
        user = request.POST.get('usuario')
        producto = request.POST.get('producto')
        start = request.POST.get('date_start')
        end = request.POST.get('date_end')
        with connection.cursor() as cursor:
            cursor.execute(
                GLOBAL_QUERY + WHERE_CLAUSE + USER_FIELD + ' =%s AND ' + PRODUCT_FIELD +
                '=%s AND "reviews"."timed" BETWEEN %s AND %s ' + ORDER_ASC, [user, producto, start, end])
            qs1 = cursor.fetchall()
            cursor.execute(
                GLOBAL_QUERY + WHERE_CLAUSE + USER_FIELD + ' =%s AND ' + PRODUCT_FIELD +
                '=%s AND "reviews"."timed" BETWEEN %s AND %s ' + ORDER_DESC, [user, producto, start, end])
            qs2 = cursor.fetchall()
            qs = METRIC_QUERY + WHERE_CLAUSE + USER_FIELD + ' =%s AND' + PRODUCT_FIELD + '=%s AND "reviews"."timed" BETWEEN %s AND %s'
            cursor.execute(qs, [user, producto, start, end])
            values = cursor.fetchone()
            cursor.close()
        return response(qs1, qs2, values)
