from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.contrib.auth.models import User, Group
from django.views.generic import UpdateView, ListView, TemplateView, RedirectView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.urls import reverse
from django.utils.dateparse import parse_datetime, parse_date

import django_filters.rest_framework
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from drf_yasg2.inspectors.query import CoreAPICompatInspector


import django_excel as excel
import pyexcel
import xlrd
# import pyexcel.ext.xls # in order to handle 'xls' format
# import pyexcel.ext.xlsx # in order to handle 'xlsx' format
# import pyexcel.ext.ods # in order to handle 'ods' format


from custom_script_extensions.drf_permissions import CheckGroupPermissions__dynamic__ORM, CheckGroupPermissions__ORM
from custom_script_extensions.drf_serializers import (
	Generic__Serializer,
	test_table_model__Serializer, 
	processing_module_pipeline_user_content_history__Serializer)
from .models import (
    databaseConnections,
	test_table_model, 
	processing_module_pipeline_user_content_history)

from django.db.models import Case, Sum, Min, Max, Count, When, Q, F, Value, IntegerField, CharField, DateField, DateTimeField
#from .models import zs_dashboards_Users
from custom_script_extensions.group_permission_check import user_group_access_check

import uuid
from django.utils.crypto import get_random_string

from datetime import datetime
import json

import os
from django.core.exceptions import ValidationError



#@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
@login_required
@permission_required('app_zs_examples.view_app')
def index(request):

	template = 'app_zs_examples/index.html'

	return render(request, template)





#CRUD DRF UTILS ======================================================================================================================
# test upload files
#@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
@login_required
@permission_required('app_zs_examples.view_app')
def test_upload_to_model(request):
    return render(request, 'app_zs_examples/drf_test_upload_to_model/drf_test_upload_to_model_template.html')

# Dynamic model #####################################
def django_models_search(request_orm_model):
	model = None
	this_app_name = __package__.rsplit('.', 1)[-1]
	#search model in this app
	try:
		model = apps.get_model(this_app_name, request_orm_model)
	except Exception as e:
		#search model in all django project
		for app_name, app in apps.app_configs.items():
			try:
				model = apps.get_model(app_name, request_orm_model)
				break
			except Exception as e:
				pass
	return model



# Dynamic Filters ##################################
def GetFilterType(field, fieldType):
    if fieldType == 'AutoField':
        filter_type = ['exact', 'range']
    elif fieldType == 'CharField':
        filter_type = ['icontains']
    elif fieldType == 'DateTimeField':
        filter_type = ['year__gt', 'year__lt', 'range']
    elif fieldType == 'DateField':
        filter_type = ['year__gt', 'year__lt', 'range']
    elif fieldType == 'IntegerField':
        filter_type = ['gte', 'lte', 'range']
    elif fieldType == 'BooleanField':
        filter_type = ['exact']
    elif fieldType == 'TextField':
        filter_type = ['icontains']
    else:
        filter_type = ['exact']
    return filter_type



# Pagination ########################################
class Searchpagination__2__(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'p'
    max_page_size = 100

class Searchpagination__5__(PageNumberPagination):
    page_size = 5

class Searchpagination__10__(PageNumberPagination):
    page_size = 10

class Searchpagination__20__(PageNumberPagination):
    page_size = 20

class Searchpagination__50__(PageNumberPagination):
    page_size = 50



# SWAGGER UTILS #####################################
class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
   def get_filter_parameters(self, filter_backend):
      if isinstance(filter_backend, DjangoFilterBackend):
         result = super(DjangoFilterDescriptionInspector, self).get_filter_parameters(filter_backend)
         for param in result:
            if not param.get('description', ''):
               param.description = "Filter the returned list by {field_name}".format(field_name=param.name)

         return result

      return NotHandled



@method_decorator(swagger_auto_schema(
    manual_parameters=[openapi.Parameter( name='users_count', in_=openapi.IN_QUERY, type='int', description='Count of users')],
    filter_inspectors=[DjangoFilterDescriptionInspector],
    responses={'200': 'ok'}), name='list')


#CRUD DRF DYNAMIC ======================================================================================================================
#CRUD DRF - READ ==================== DYNAMIC ORM  
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class genericTable__RestApi__View(generics.ListAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__dynamic__ORM]
    pagination_class = Searchpagination__5__

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filterset_fields = {}
    search_fields = []
    ordering_fields = '__all__'
    ordering = ['id']

    lookup_field = 'id'    
    lookup_url_kwarg = 'id'


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = django_models_search(str(self.kwargs['request_orm_model'])).__name__

        for key in data:
            if key == 'name':
                data[key] = 'DYNAMIC ORM API'
            elif key == 'description':
                data[key] = f'Get rows list or by id. data in orm model: {orm_model__name}'

        return Response(data=data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        try:
            model = django_models_search(str(self.kwargs['request_orm_model']))
            genericTable__RestApi__View.search_fields = [f.name for f in model._meta.get_fields()]
            filterset_fields_temp = {}
            for field in model._meta.get_fields():
                filter_type = GetFilterType(field, field.get_internal_type())
                filterset_fields_temp[field.name] = filter_type
            genericTable__RestApi__View.filterset_fields = filterset_fields_temp

            if self.kwargs.get(self.lookup_url_kwarg):
                _id = self.kwargs.get(self.lookup_url_kwarg)
                queryset = model.objects.filter(id=_id)

            else:
                queryset = model.objects.all()#.order_by('-id')
            
            return queryset
        except Exception as e:
            raise Http404


    def get_serializer_class(self):
        Generic__Serializer.Meta.model = django_models_search(str(self.kwargs['request_orm_model']))
        return Generic__Serializer



#CRUD DRF - CREATE ==================== DYNAMIC ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class genericTable__RestApi__Create(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__dynamic__ORM]


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        orm_model__name = django_models_search(str(self.kwargs['request_orm_model'])).__name__

        for key in data:
            if key == 'name':
                data[key] = 'DYNAMIC ORM API'
            elif key == 'description':
                data[key] = f'Create single row. data in orm model: {orm_model__name}'

        return Response(data=data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = Generic__Serializer(data=request.data, context={
            'request': request,
            'id': self.kwargs.get(self.lookup_url_kwarg)})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 


    def get_serializer_class(self):
        Generic__Serializer.Meta.model = django_models_search(str(self.kwargs['request_orm_model']))
        return Generic__Serializer



#CRUD DRF - UPDATE ==================== DYNAMIC ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class genericTable__RestApi__Update(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__dynamic__ORM]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


    def get_queryset(self):
        try:
            model = django_models_search(str(self.kwargs['request_orm_model']))
            return model.objects.all()
        except Exception as e:
            raise Http404


    def get_serializer_class(self):
        Generic__Serializer.Meta.model = django_models_search(str(self.kwargs['request_orm_model']))
        return Generic__Serializer


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = django_models_search(str(self.kwargs['request_orm_model'])).__name__

        for key in data:
            if key == 'name':
                data[key] = 'DYNAMIC ORM API'
            elif key == 'description':
                data[key] = f'Update by id. data in orm model: {orm_model__name}'

        return Response(data=data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        _id = self.kwargs.get(self.lookup_url_kwarg)
        model = django_models_search(str(self.kwargs['request_orm_model']))
        serializer = Generic__Serializer(model.objects.get(id=_id), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#CRUD DRF - DELETE ==================== DYNAMIC ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class genericTable__RestApi__Delete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__dynamic__ORM]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


    def get_queryset(self):
        try:
            model = django_models_search(str(self.kwargs['request_orm_model']))
            return model.objects.all()
        except Exception as e:
            raise Http404


    def get_serializer_class(self):
        Generic__Serializer.Meta.model = django_models_search(str(self.kwargs['request_orm_model']))


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = django_models_search(str(self.kwargs['request_orm_model'])).__name__

        for key in data:
            if key == 'name':
                data[key] = 'DYNAMIC ORM API'
            elif key == 'description':
                data[key] = f'Delete by id. data in orm model: {orm_model__name}'


        return Response(data=data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)



#CRUD DRF - EXPORT XLS ==================== DYNAMIC ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class genericTable__RestApi__export(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__dynamic__ORM]
    pagination_class = Searchpagination__5__

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filterset_fields = {}
    search_fields = []
    ordering_fields = '__all__'
    ordering = ['id']

    lookup_field = 'id'    
    lookup_url_kwarg = 'id'


    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


    def get_serializer_class(self):
        Generic__Serializer.Meta.model = django_models_search(str(self.kwargs['request_orm_model']))
        return Generic__Serializer


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = django_models_search(str(self.kwargs['request_orm_model'])).__name__

        for key in data:
            if key == 'name':
                data[key] = 'DYNAMIC ORM API'
            elif key == 'description':
                data[key] = f'Export from file. data in orm model: {orm_model__name}'
        data['avalilable formats'] = {'excel': ['xls', 'xlsx']}

        return Response(data=data, status=status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        model = django_models_search(str(self.kwargs['request_orm_model']))

        try:
            document_type = self.kwargs['document_type']
            if document_type and document_type in ['xlsx', 'xls']:
                if self.kwargs.get(self.lookup_url_kwarg):
                    _id = self.kwargs.get(self.lookup_url_kwarg)
                    queryset = model.objects.filter(id=_id)
                else:
                    queryset = model.objects.all().order_by('-id')
            else:
                return Response(data=queryset, status=status.HTTP_404_NOT_FOUND)

            # filterset_fields_temp = {}
            # for field in model._meta.get_fields():
            #     filter_type = GetFilterType(field, field.get_internal_type())
            #     filterset_fields_temp[field.name] = filter_type
            # test_table_model__RestApi__View.search_fields = [f.name for f in model._meta.get_fields()]
            # test_table_model__RestApi__View.filterset_fields = filterset_fields_temp
            export_queryset = self.filter_queryset(queryset)
            column_names = list(export_queryset[0].__dict__.keys())[1:]
            filename = model.__name__ + '__' + datetime.now().strftime("%Y-%m-%d__%H-%M")
            if len(filename) > 230: filename = 'data' + '__' +datetime.now().strftime("%Y-%m-%d__%H-%M")
            response = excel.make_response_from_query_sets(export_queryset, column_names, f"{document_type}", file_name="template")
            response['Content-Disposition'] = f'attachment; filename="{filename}.{document_type}"' 
            return response
            #return Response({'message': 'test response'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, 'error output ==============================')
            if 'list index out of range' in str(e):
                return Response({'message': 'no data'}, status=status.HTTP_404_NOT_FOUND)
            else:
                raise Http404



#CRUD DRF - IMPORT XLS ==================== DYNAMIC ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class genericTable__RestApi__import(APIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__dynamic__ORM]
    parser_classes = (MultiPartParser,FormParser,)
    #parser_classes = (MultiPartParser,FileUploadParser,)
    #parser_classes = [FileUploadParser]


    def get_serializer_class(self):
        Generic__Serializer.Meta.model = django_models_search(str(self.kwargs['request_orm_model']))
        return Generic__Serializer


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = django_models_search(str(self.kwargs['request_orm_model'])).__name__

        for key in data:
            if key == 'name':
                data[key] = 'DYNAMIC ORM API'
            elif key == 'description':
                data[key] = f'Upload from file. Update/create data in orm model: {orm_model__name}'
        data['valid formats'] = {'excel': ['xls', 'xlsx']}

        return Response(data=data, status=status.HTTP_200_OK)



    def post(self, request, format=None, *args, **kwargs):
        #print(request.FILES, 'ZZZZZZZZZZZZZ')
        file, f_name, f_type, f_size = (None,)*4
        for filename in request.FILES:
            file = request.FILES[filename]
            f_name = file.name           # Gives name
            f_type = file.content_type   # Gives Content type text/html etc
            f_size = file.size           # Gives file's size in byte
            #file.read()         # Reads file
           # print('1======', file)
            #print('2======', f_name)
            #print('3======', f_type)
            #print('4======', f_size)


        valid__f_types = {
            'excel': [
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
            'word': ['-']
            }

        group__f_types = None
        group__f_types_valid = []
        for k in valid__f_types:
            group__f_types_valid.append(k)
            group__f_types_check_list = valid__f_types[k]
            if f_type in group__f_types_check_list:
                group__f_types = k
        if group__f_types is None: return Response({'message': f'invalid file-type. Valid: {group__f_types_valid}'}, status=status.HTTP_400_BAD_REQUEST)
        

        model = django_models_search(str(self.kwargs['request_orm_model']))
        orm__column_names = []
        for col in model._meta.fields:
            orm__column_names.append(col.name)


        orm__column_datatypes = {} 
        for col in orm__column_names:
            orm__column_datatypes[col] = model._meta.get_field(col).get_internal_type()

        try:
            if group__f_types == 'excel':
                wb = xlrd.open_workbook(file_contents=file.read())
                ws = wb.sheet_by_index(0)

                ws__column_names = []
                for col in range(ws.ncols):
                    ws__column_names.append(ws.cell_value(0,col))

                ws__data =[]
                for row in range(1, ws.nrows):
                    elm = {}
                    for col in range(ws.ncols):
                        elm[ws__column_names[col]]=ws.cell_value(row,col)
                    if len([k for k in elm if elm[k] != None and elm[k] != '']) > 0:
                        ws__data.append(elm)

                #print(ws__data, 'UUUUUUUUUUUU')
                #print(orm__column_names, 'NNNNNNNNNNNNNNNN')
                #print(ws__column_names, 'QQQQQQQQQQQQQQQQQQQQQQQQ')
                #print(orm__column_datatypes, '===========================')

                #for row in ws__data:
                bulk_create = []
                bulk_update = []
                count_updated_rows, count_inserted_rows = (0,)*2
                for row_index, row in enumerate(ws__data):
                    _id = row.get('id')

                    valid_row = {}
                    for col in orm__column_names:
                        if col in ws__column_names:
                            value = row[col]
                            value_datatype = orm__column_datatypes[col]
                            if value_datatype == 'DateTimeField':
                                if parse_datetime(value):
                                    pass
                                else:
                                    value = None
                            elif value_datatype == 'DateField':
                                if parse_date(value):
                                    pass
                                else:
                                    value = None
                            elif value_datatype == 'BooleanField':
                                if type(value).__name__  == 'int':
                                    pass
                                else:
                                    value = None
                            elif value_datatype == 'IntegerField':
                                if type(value).__name__  in ['int', 'float']:
                                    pass
                                else:
                                    value = None
                            if value == '': value = None
                            valid_row[col] = value

                    #update - insert rows

                    if _id:
                        #model.objects.filter(id=_id).update(**valid_row)
                        bulk_update.append(model.objects.filter(id=_id).update(**valid_row))
                    else:
                        bulk_create.append(valid_row)

                    if (row_index+1)==len(ws__data):
                        if len(bulk_create) > 0:
                            model.objects.bulk_create([model(**kv) for kv in bulk_create])
                            count_inserted_rows = len(bulk_create)
                        if len(bulk_update) > 0:
                            count_updated_rows = len(bulk_update)


        except Exception as e:
            print(str(e),'eeeeeeeeeeeeeeeeeeee')
            return Response({'message': f'data inserting error.'}, status=status.HTTP_400_BAD_REQUEST)



        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return Response({
            'message': f'{group__f_types} uploaded. created count: {count_inserted_rows}, updated count: {count_updated_rows}'}, 
            status=status.HTTP_200_OK)







#CRUD DRF ======================================================================================================================
#CRUD DRF - READ ==================== ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class test_table_model__RestApi__View(generics.ListAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__ORM]
    serializer_class = test_table_model__Serializer
    model = serializer_class.Meta.model
    pagination_class = Searchpagination__2__

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filterset_fields = ['test_field', 'datetime_start_field', 'datetime_end_field']#{'test_field':['icontains'], } 
    search_fields = ['test_field', 'integer_choice_field']
    ordering_fields = ['test_field', 'datetime_start_field', 'datetime_end_field']
    ordering = ['id']

    lookup_field = 'id'
    lookup_url_kwarg = 'id'


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = self.serializer_class.Meta.model.__name__

        for key in data:
            if key == 'name':
                data[key] = 'ORM API'
            elif key == 'description':
                data[key] = f'Get rows list or by id. data in orm model: {orm_model__name}'

        return Response(data=data, status=status.HTTP_200_OK)


    def get_queryset(self):
        try:
            if self.kwargs.get(self.lookup_url_kwarg):
                _id = self.kwargs.get(self.lookup_url_kwarg)
                queryset = self.model.objects.filter(id=_id)
            else:
                queryset = self.model.objects.all().order_by('-id')

        # filterset_fields_temp = {}
        # for field in self.model._meta.get_fields():
        #     filter_type = GetFilterType(field, field.get_internal_type())
        #     filterset_fields_temp[field.name] = filter_type
        # test_table_model__RestApi__View.search_fields = [f.name for f in self.model._meta.get_fields()]
        # test_table_model__RestApi__View.filterset_fields = filterset_fields_temp

            return queryset
        except Exception as e:
            raise Http404



#CRUD DRF - CREATE ==================== ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class test_table_model__RestApi__Create(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__ORM]
    serializer_class = test_table_model__Serializer
    queryset = test_table_model.objects.all()


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = self.serializer_class.Meta.model.__name__

        for key in data:
            if key == 'name':
                data[key] = 'ORM API'
            elif key == 'description':
                data[key] = f'Create single row. data in orm model: {orm_model__name}'

        return Response(data=data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={
            'request': request,
            'id': self.kwargs.get(self.lookup_url_kwarg)})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



#CRUD DRF - UPDATE ==================== ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class test_table_model__RestApi__Update(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__ORM]
    serializer_class = test_table_model__Serializer
    queryset = test_table_model.objects.all()

    lookup_field = 'id'
    lookup_url_kwarg = 'id'


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = self.serializer_class.Meta.model.__name__

        for key in data:
            if key == 'name':
                data[key] = 'ORM API'
            elif key == 'description':
                data[key] = f'Update by id. data in orm model: {orm_model__name}'

        return Response(data=data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        _id = self.kwargs.get(self.lookup_url_kwarg)
        serializer = test_table_model__Serializer(test_table_model.objects.get(id=_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#CRUD DRF - DELETE ==================== ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class test_table_model__RestApi__Delete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__ORM]
    serializer_class = test_table_model__Serializer
    queryset = test_table_model.objects.all()

    lookup_field = 'id'
    lookup_url_kwarg = 'id'


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = self.serializer_class.Meta.model.__name__

        for key in data:
            if key == 'name':
                data[key] = 'ORM API'
            elif key == 'description':
                data[key] = f'Delete by id. data in orm model: {orm_model__name}'


        return Response(data=data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)



#CRUD DRF - EXPORT XLS ==================== ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class test_table_model__RestApi__export(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__ORM]
    serializer_class = test_table_model__Serializer
    model = serializer_class.Meta.model
    pagination_class = Searchpagination__2__

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filterset_fields = ['test_field', 'datetime_start_field', 'datetime_end_field', 'boolean_field', 'integer_field']#{'test_field':['icontains'], } 
    search_fields = ['test_field', 'integer_choice_field', 'integer_field']
    ordering_fields = ['test_field', 'datetime_start_field', 'datetime_end_field']
    ordering = ['id']

    lookup_field = 'id'
    lookup_url_kwarg = 'id'


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = self.serializer_class.Meta.model.__name__

        for key in data:
            if key == 'name':
                data[key] = 'ORM API'
            elif key == 'description':
                data[key] = f'Export from file. data in orm model: {orm_model__name}'
        data['avalilable formats'] = {'excel': ['xls', 'xlsx']}

        return Response(data=data, status=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        try:
            document_type = self.kwargs['document_type']
            if document_type and document_type in ['xlsx', 'xls']:
                if self.kwargs.get(self.lookup_url_kwarg):
                    _id = self.kwargs.get(self.lookup_url_kwarg)
                    queryset = self.model.objects.filter(id=_id)
                else:
                    queryset = self.model.objects.all().order_by('-id')
            else:
                return Response(data=queryset, status=status.HTTP_404_NOT_FOUND)

            # filterset_fields_temp = {}
            # for field in self.model._meta.get_fields():
            #     filter_type = GetFilterType(field, field.get_internal_type())
            #     filterset_fields_temp[field.name] = filter_type
            # test_table_model__RestApi__View.search_fields = [f.name for f in self.model._meta.get_fields()]
            # test_table_model__RestApi__View.filterset_fields = filterset_fields_temp
            export_queryset = self.filter_queryset(queryset)
            column_names = list(export_queryset[0].__dict__.keys())[1:]
            filename = self.model.__name__ + '__' + datetime.now().strftime("%Y-%m-%d__%H-%M")
            if len(filename) > 230: filename = 'data' + '__' +datetime.now().strftime("%Y-%m-%d__%H-%M")
            response = excel.make_response_from_query_sets(export_queryset, column_names, f"{document_type}", file_name="template")
            response['Content-Disposition'] = f'attachment; filename="{filename}.{document_type}"' 
            return response
            #return Response({'message': 'test response'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, 'error output ==============================')
            if 'list index out of range' in str(e):
                return Response({'message': 'no data'}, status=status.HTTP_404_NOT_FOUND)
            else:
                raise Http404



#CRUD DRF - IMPORT XLS ==================== ORM 
@method_decorator([login_required, permission_required("app_zs_examples.view_app")], name="dispatch")
class test_table_model__RestApi__import(APIView):
    permission_classes = [IsAuthenticated, CheckGroupPermissions__ORM]
    serializer_class = test_table_model__Serializer
    queryset = test_table_model.objects.all()
    parser_classes = (MultiPartParser,FormParser,)
    #parser_classes = (MultiPartParser,FileUploadParser,)
    #parser_classes = [FileUploadParser]


    def options(self, request, *args, **kwargs):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)

        orm_model__name = self.serializer_class.Meta.model.__name__

        for key in data:
            if key == 'name':
                data[key] = 'ORM API'
            elif key == 'description':
                data[key] = f'Upload from file. Update/create data in orm model: {orm_model__name}'
        data['valid formats'] = {'excel': ['xls', 'xlsx']}

        return Response(data=data, status=status.HTTP_200_OK)



    def post(self, request, format=None, *args, **kwargs):
        #print(request.FILES, 'ZZZZZZZZZZZZZ')
        file, f_name, f_type, f_size = (None,)*4
        for filename in request.FILES:
            file = request.FILES[filename]
            f_name = file.name           # Gives name
            f_type = file.content_type   # Gives Content type text/html etc
            f_size = file.size           # Gives file's size in byte
            #file.read()         # Reads file
           # print('1======', file)
            #print('2======', f_name)
            #print('3======', f_type)
            #print('4======', f_size)


        valid__f_types = {
            'excel': [
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
            'word': ['-']
            }

        group__f_types = None
        group__f_types_valid = []
        for k in valid__f_types:
            group__f_types_valid.append(k)
            group__f_types_check_list = valid__f_types[k]
            if f_type in group__f_types_check_list:
                group__f_types = k
        if group__f_types is None: return Response({'message': f'invalid file-type. Valid: {group__f_types_valid}'}, status=status.HTTP_400_BAD_REQUEST)
        


        orm__column_names = self.serializer_class.Meta.fields
        orm__column_datatypes = {}
        for col in orm__column_names:
            orm__column_datatypes[col] = self.serializer_class.Meta.model._meta.get_field(col).get_internal_type()

        try:
            if group__f_types == 'excel':
                wb = xlrd.open_workbook(file_contents=file.read())
                ws = wb.sheet_by_index(0)

                ws__column_names = []
                for col in range(ws.ncols):
                    ws__column_names.append(ws.cell_value(0,col))

                ws__data =[]
                for row in range(1, ws.nrows):
                    elm = {}
                    for col in range(ws.ncols):
                        elm[ws__column_names[col]]=ws.cell_value(row,col)
                    if len([k for k in elm if elm[k] != None and elm[k] != '']) > 0:
                        ws__data.append(elm)

                #print(ws__data, 'UUUUUUUUUUUU')
                #print(orm__column_names, 'NNNNNNNNNNNNNNNN')
                #print(ws__column_names, 'QQQQQQQQQQQQQQQQQQQQQQQQ')
                #print(orm__column_datatypes, '===========================')

                #for row in ws__data:
                bulk_create = []
                bulk_update = []
                count_updated_rows, count_inserted_rows = (0,)*2
                for row_index, row in enumerate(ws__data):
                    _id = row.get('id')

                    valid_row = {}
                    for col in orm__column_names:
                        if col in ws__column_names:
                            value = row[col]
                            value_datatype = orm__column_datatypes[col]
                            if value_datatype == 'DateTimeField':
                                if parse_datetime(value):
                                    pass
                                else:
                                    value = None
                            elif value_datatype == 'DateField':
                                if parse_date(value):
                                    pass
                                else:
                                    value = None
                            elif value_datatype == 'BooleanField':
                                if type(value).__name__  == 'int':
                                    pass
                                else:
                                    value = None
                            elif value_datatype == 'IntegerField':
                                if type(value).__name__  in ['int', 'float']:
                                    pass
                                else:
                                    value = None
                            if value == '': value = None
                            valid_row[col] = value

                    #update - insert rows
                    model = self.serializer_class.Meta.model

                    if _id:
                        #model.objects.filter(id=_id).update(**valid_row)
                        bulk_update.append(model.objects.filter(id=_id).update(**valid_row))
                    else:
                        bulk_create.append(valid_row)

                    if (row_index+1)==len(ws__data):
                        if len(bulk_create) > 0:
                            model.objects.bulk_create([model(**kv) for kv in bulk_create])
                            count_inserted_rows = len(bulk_create)
                        if len(bulk_update) > 0:
                            count_updated_rows = len(bulk_update)


        except Exception as e:
            return Response({'message': f'data inserting error.'}, status=status.HTTP_400_BAD_REQUEST)



        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return Response({
            'message': f'{group__f_types} uploaded. created count: {count_inserted_rows}, updated count: {count_updated_rows}'}, 
            status=status.HTTP_200_OK) 
