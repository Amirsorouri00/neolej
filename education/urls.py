from django.urls import include, path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from education.views.rest.workshop import test1 as workshop_test1, test2 as workshop_test2, WorkshopAPI
from education.views.rest.workshop_file import test2 as workshop_file_test2
from education.views.rest.discount import test2 as discount_file_test2, test1 as discount_file_test1
from education.views.rest.payment import test1 as invoice_test1, test2 as invoice_test2, WorkshopInvoiceApi, WorkshopPaymentApi
from education.views.rest.discount import WorkshopDateDiscountAPI, WorkshopPersonalDiscountAPI, WorkshopRaceDiscountAPI
from education.views.rest.buy_workshop import BuyAPI

app_name = 'education'

urlpatterns = [
    # path('form/', include(([
    # ], 'education'), namespace='form')),
    
    path('rest/', include(([

        path('workshop/', include(([
            path('test2/', workshop_test2, name='rest_workshop_test2'),
            path('test1/', workshop_test1, name='rest_workshop_test1'),
            path('<int:uuid>/', WorkshopAPI.as_view(), name='rest_workshop_put'),
            path('', WorkshopAPI.as_view(), name='rest_workshop'),

            path('buy/', include(([
                path('', BuyAPI.as_view(), name='rest_workshop_buy_post'),
                path('<int:workshop_uuid>/<int:user_uuid>/', BuyAPI.as_view(), name='rest_workshop_buy_delete'),
                # path('test2/', discount_file_test2, name='rest_discount_test2'),
                # path('test1/', discount_file_test1, name='rest_discount_test1'),

                path('invoice/', include(([
                    path('', WorkshopInvoiceApi.as_view(), name='rest_workshop_invoice'),
                    path('<int:uuid>/', WorkshopInvoiceApi.as_view(), name='rest_workshop_invoice_pud'),
                    # path('test2/', discount_file_test2, name='rest_discount_test2'),
                    # path('test1/', discount_file_test1, name='rest_discount_test1'),
                ], 'education'), namespace='rest_workshop_invoice')),     
                path('payment/', include(([
                    path('', WorkshopPaymentApi.as_view(), name='rest_workshop_payment'),
                    path('<int:uuid>/', WorkshopPaymentApi.as_view(), name='rest_workshop_payment_pud'),
                    # path('test2/', discount_file_test2, name='rest_discount_test2'),
                    # path('test1/', discount_file_test1, name='rest_discount_test1'),
                ], 'education'), namespace='rest_workshop_payment')), 
            ], 'education'), namespace='rest_workshop_buy')),


            path('discount/', include(([
                path('personal/', WorkshopPersonalDiscountAPI.as_view(), name='rest_workshop_personal_discount'),
                path('personal/<str:uuid>/', WorkshopPersonalDiscountAPI.as_view(), name='rest_workshop_personal_discount_pud'),

                path('date/', WorkshopDateDiscountAPI.as_view(), name='rest_workshop_date_discount'),
                path('date/<str:uuid>/', WorkshopDateDiscountAPI.as_view(), name='rest_workshop_date_discount_pud'),

                path('race/', WorkshopRaceDiscountAPI.as_view(), name='rest_workshop_race_discount'),
                path('race/<str:uuid>/', WorkshopRaceDiscountAPI.as_view(), name='rest_workshop_race_discount_pud'),

                # path('test2/', discount_file_test2, name='rest_discount_test2'),
                # path('test1/', discount_file_test1, name='rest_discount_test1'),
            ], 'education'), namespace='rest_workshop_discount')),    

            
        ], 'education'), namespace='rest_workshops')),

        path('workshop_file/', include(([
            path('test2/', workshop_file_test2, name='rest_workshop_file_test2'),
        ], 'education'), namespace='rest_workshop_files')),

        path('discount/', include(([
            path('test2/', discount_file_test2, name='rest_discount_test2'),
            path('test1/', discount_file_test1, name='rest_discount_test1'),
        ], 'education'), namespace='rest_discount')),

    ], 'education'), namespace='rest')),
]