from django.conf.urls import url

from . import views

app_name= 'googleSheetIntoDB'
urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^index.html$',views.index, name='index'),
    url(r'^data_index.html$', views.data_index, name='data_index'),
    # ex: /googleSheetIntoDB/5/
    url(r'^(?P<metadata_id>[0-9]+)/$', views.detailView, name='detailView'),
    url(r'^detail/$', views.detail, name='detail'),
   # url(r'^toc/$', views.toc, name='toc'),
    #url(r'^first_choice/$', views.first_choice, name='first_choice'),
    url(r'^detail_view/$', views.detail_view, name='detail_view'),
    url(r'^agro_detail_view/$', views.agro_detail_view, name='agro_detail_view'),
    url(r'^index_google_sheet_list/$', views.index_google_sheet_list, name='index_google_sheet_list'),
    url(r'^choose/$', views.choose, name='choose'),
    url(r'^choose/index.html', views.index, name='index'),
    url(r'^choose_to_input_data',views.choose_to_input_data,name='choose_to_input_data'),
   # url(r'^choose/data_already_exist.html$', views.data_already_exist, name='data_already_exist'),
   # url(r'^choose/data_in_db_success.html$', views.data_in_db_success, name='choose_data_in_db_success'),
    url(r'^choose_to_overwrite.html$', views.choose_to_overwrite, name='choose_to_overwrite'),
    url(r'^data_in_db_success.html$', views.data_in_db_success, name='data_in_db_success'),
    url(r'^choose_to_refresh$', views.choose_to_refresh, name='choose_to_refresh'),
    url(r'^choose_to_refresh_agro', views.choose_to_refresh_agro, name='choose_to_refresh_agro'),
    url(r'^refresh_data_in_db_success.html$',views.refresh_data_in_db_success, name='refresh_data_in_db_success'),
    url(r'^googleSheetIntoDB/no_list_to_select.html$',views.no_list_to_select, name='no_list_to_select'),
    url(r'^choose_worksheet', views.choose_worksheet, name='choose_worksheet'),
    url(r'^agro_index',views.agro_index,name='agro_index'),
]