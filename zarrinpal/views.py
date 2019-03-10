# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status   
from education.models import WorkshopInvoice

MERCHANT = '9f35b4e2-4022-11e9-ad5c-000c295eb8fc'
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'amirsorouri26@gmail.com'  # Optional
# mobile = '09128048897'  # Optional
CallbackURL = 'http://neolej.ir/payment/verify/' # Important: need to edit for realy server.


from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def send_request(request):
    email = request.user.email
    mobile = request.user.cell_phone
    # return HttpResponse(request.data.get('invoice'))
    invoice = get_object_or_404(WorkshopInvoice, uuid = request.data.get('invoice'))
    amount = invoice.amount_to_pay
    if amount is not None:
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        if result.Status == 100:
            invoice.authority = result.Authority
            invoice.save()
            return JsonResponse({'auth': result.Authority}, safe=False, status=status.HTTP_200_OK)
            # return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return JsonResponse({'Error':  'from zarrinpal'}, safe=False, status = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'Error': "from us. payment has no amount set on it's invoice."}, safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def verify(request):
    if request.GET.get('Status') == 'OK':
        invoice = get_object_or_404(WorkshopInvoice, authority = request.GET.get('Authority'))
        amount = invoice.amount_to_pay
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
        # if True:
            invoice.ref_id = result.RefID
            invoice.payed_or_not = True
            invoice.save()
            valid = True
            payment_invoices = invoice.payment.invoice.all()
            print(payment_invoices.count())
            if 0 == payment_invoices.count():
                print(None)
            # elif 1 == payment_invoices.count():
            #     print(payment_invoices)
            #     if payment_invoices.payed_or_not is False:
            #         print('here2')
            #         valid = False
            else:
                for tmp_invoice in payment_invoices:
                    print('here')
                    if tmp_invoice.payed_or_not is False:
                        print('here2')
                        valid = False
            if payment_invoices and valid:
                print('here3')
                invoice.payment.pending = False
                
            return JsonResponse({'RefID': result.RefID}, safe=False, status=status.HTTP_200_OK)
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return JsonResponse({'message': 'Transaction failed'}, safe=False, status=result.Status)
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return JsonResponse({'message': 'Transaction failed or canceled by user'}, safe=False, status=status.HTTP_417_EXPECTATION_FAILED)
        # return HttpResponse('Transaction failed or canceled by user')

