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
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
description = "خرید دوره مطالعات پایه."  # Required
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
    amount = (invoice.amount_to_pay - invoice.discount_amount) / 10 
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

from education.models import Workshop

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def verify(request):
    if request.GET.get('Status') == 'OK':
        from decimal import Decimal
        # message = [{
        #     "name": "نئولج",
        #     "amount": Decimal(1000.500).normalize() # amount*10
        # }]
        # to = request.user.cell_phone
        # from commons.services import sms_130
        # r = sms_130(message, to)
        invoice = get_object_or_404(WorkshopInvoice, authority = request.GET.get('Authority'))
        amount = (invoice.amount_to_pay - invoice.discount_amount) / 10
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        message = [{
            "name": "نئولج",
            "amount": int(amount*10)
        }]
        to = request.user.cell_phone
        from commons.services import sms_130
        r = sms_130(message, to)

        if result.Status == 100:
        # if True:
            invoice.ref_id = result.RefID
            invoice.payed_or_not = True
            invoice.save()
            valid = True
            log = 'none'
            payment_invoices = invoice.payment.invoice.all()

            print(payment_invoices.count())
            if 0 == payment_invoices.count():
                print(None)
            else:
                for tmp_invoice in payment_invoices:
                    print('here')
                    if tmp_invoice.payed_or_not is False:
                        print('here2')
                        valid = False
            if payment_invoices and valid:
                log = 'here'
                print('here3')
                payment = invoice.payment
                # return JsonResponse({'status': result.Status}, safe=False, status=200)
                payment.pending = False
                payment.save()
                workshop = Workshop.objects.get(id = payment.workshop_id)
                from accounts.models import User
                user = User.objects.get(id = payment.user_id)
                workshop.buyers.add(user)
            # r = sms_130(message, to)
            return JsonResponse({'RefID': result.RefID, 'log':log}, safe=False, status=status.HTTP_200_OK)
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            # invoice.ref_id = result.RefID
            invoice.payed_or_not = True
            invoice.save()
            valid = True
            log = 'none'
            payment_invoices = invoice.payment.invoice.all()
            print(payment_invoices.count())
            if 0 == payment_invoices.count():
                print(None)
            else:
                for tmp_invoice in payment_invoices:
                    print('here')
                    if tmp_invoice.payed_or_not is False:
                        print('here2')
                        valid = False
            if payment_invoices and valid:
                log = 'here'
                print('here3')
                payment = invoice.payment
                payment.pending = False
                payment.save()
                workshop = Workshop.objects.get(id = payment.workshop_id)
                from accounts.models import User
                user = User.objects.get(id = payment.user_id)
                workshop.buyers.add(user)
            # r = sms_130(message, to)
            return JsonResponse({'Transaction submitted : ':str(result.Status)}, safe=False, status=101)
        else:
            return JsonResponse({'message': 'Transaction failed'}, safe=False, status=101)
            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return JsonResponse({'message': 'Transaction failed or canceled by user'}, safe=False, status=status.HTTP_417_EXPECTATION_FAILED)
        # return HttpResponse('Transaction failed or canceled by user')


