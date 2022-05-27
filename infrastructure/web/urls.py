from django.urls import path
from .order.views import HomePageView
from .nomenclature.views import (
    NomenclatureCreate, NomenclatureImportView,
    NomenclaturesServiceListView,
    NomenclatureItemsFilterApiView,
    NomenclatureExportView,
)
from .own.views import OwnDeleteView, OwnCreate
from .contractor.views import ContractorCreate, ContractorList, ContractorDetail
from .trade_point.views import TradePointCreate

nomenclature_urls = [
    path('nomenclature/export/', NomenclatureExportView.as_view(), name='nomenclature_export'),
    path('nomenclature/import/', NomenclatureImportView.as_view(), name="nomenclature_import"),
    path('nomenclature/create/', NomenclatureCreate.as_view(), name="nomenclature_create"),
    path(
        'nomenclature/<int:id>/services/filter/',
        NomenclatureItemsFilterApiView.as_view()
    ),
    path('nomenclature/list/', NomenclaturesServiceListView.as_view(), name="nomenclature_list"),
]

trade_point_urls = [
    path('trade_point/create/', TradePointCreate.as_view(), name="trade_point_create")
]

contractor_urls = [
    path('contractor/create/', ContractorCreate.as_view(), name="contractor_create"),
    path('contractor/list/', ContractorList.as_view(), name="contractors"),
    path('contractor/<int:contrID>/', ContractorDetail.as_view(), name="contractor_detail")
]

own_urls = [
    path('contractor/<int:contrID>/own/create/', OwnCreate.as_view(), name="own_create"),
    path(
        'contractor/<int:contrID>/own/<int:ownID>/delete/',
        OwnDeleteView.as_view(), name="own_delete"
    )
]

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]

urlpatterns += nomenclature_urls
urlpatterns += trade_point_urls
urlpatterns += contractor_urls
urlpatterns += own_urls
