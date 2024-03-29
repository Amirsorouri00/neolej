'''
 .d8888b.  888          888               888      8888888                                         888             
d88P  Y88b 888          888               888        888                                           888             
888    888 888          888               888        888                                           888             
888        888  .d88b.  88888b.   8888b.  888        888   88888b.d88b.  88888b.   .d88b.  888d888 888888 .d8888b  
888  88888 888 d88""88b 888 "88b     "88b 888        888   888 "888 "88b 888 "88b d88""88b 888P"   888    88K      
888    888 888 888  888 888  888 .d888888 888        888   888  888  888 888  888 888  888 888     888    "Y8888b. 
Y88b  d88P 888 Y88..88P 888 d88P 888  888 888        888   888  888  888 888 d88P Y88..88P 888     Y88b.       X88 
 "Y8888P88 888  "Y88P"  88888P"  "Y888888 888      8888888 888  888  888 88888P"   "Y88P"  888      "Y888  88888P' 
                                                                         888                                       
                                                                         888                                       
                                                                         888                                       
'''                                                                         
from education.serializers.payment_serializer import WorkshopInvoiceSerializer as WIS, WorkshopPaymentSerializer as WPS
from education.models import WorkshopInvoice, WorkshopPayment
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

'''
88888888888                888             
    888                    888             
    888                    888             
    888   .d88b.  .d8888b  888888 .d8888b  
    888  d8P  Y8b 88K      888    88K      
    888  88888888 "Y8888b. 888    "Y8888b. 
    888  Y8b.          X88 Y88b.       X88 
    888   "Y8888   88888P'  "Y888  88888P'                                                                       
'''                                                                  

def test2(request, format=None):
    print(request.POST)
    invoices = WorkshopInvoice.objects.all()
    invoices_serializer = WIS(invoices, many=True)
    print('Discount serialized result = {0}'.format(invoices_serializer.data)) 
    return JsonResponse({'received data': invoices_serializer.data}, safe=False, status=200)

def test1(request, format=None):
    print(request.POST)
    serializer = WIS(data = request.POST)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()
    return JsonResponse({'received data': request.POST}, safe=False, status=200)




from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from commons.permission_controllers import RestFrameworkPermissionController
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import status   
from rest_framework.decorators import api_view, throttle_classes
class WorkshopInvoiceApi(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, RestFrameworkPermissionController)
    serializer_class = WIS
    model = WorkshopInvoice
    errors = []
    messages = []

    # def dispatch(self, request):
    #     return super().dispatch(request)
    # @throttle_classes([OncePerDayUserThrottle])

    def get(self, request, format=None, *args, **kwargs):
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshop_invoices = self.model.objects.all()
                workshop_invoices_serialized = self.serializer_class(workshop_invoices, many=True)
            elif 'uuid' == field:
                workshop_invoices = get_object_or_404(self.model, uuid = request.GET.get('uuid'))
                workshop_invoices_serialized = self.serializer_class(workshop_invoices)
            # elif 'workshop_uuid' == field:
            #     workshop_invoices = get_object_or_404(self.model, workshops__uuid = request.GET.get('user_uuid'))
            #     workshop_invoices_serialized = self.serializer_class(workshop_invoices)
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            workshop_invoices = self.model.objects.all()
            workshop_invoices_serialized = self.serializer_class(workshop_invoices, many=True)
        return JsonResponse({'response': workshop_invoices_serialized.data}, safe=False, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None, *args, **kwargs):
        self.errors = []
        print(request.data)
        print(request.data.get('invoices'))
        valid = True
        approved_invoices = []
        for invoice in request.data.get('invoices'):
            invoice_serializer = self.serializer_class(data = invoice)
            if invoice_serializer.is_valid():
                invoice = invoice_serializer.save()
                approved_invoices.append(invoice)
            else:
                valid = False
                self.errors.append({'invoice_serializer_errors': invoice_serializer.errors})
        if(valid):
            payment_serializer = self.get_workshop_payment_serializer()(data=request.data)
            if payment_serializer.is_valid():
                payment = payment_serializer.save()
                for invoice in approved_invoices:
                    invoice.payment = payment
                    invoice.save()
                return JsonResponse({'received data': request.data, 'errors': self.errors}, safe=False, status=status.HTTP_200_OK)
            else:
                self.errors.append({'workshop_payment_serializer_errors': payment_serializer.errors})
        else:
            for invoice in approved_invoices:
                self.messages.append(self.delete(request, invoice.uuid))
                # invoice.delete()
            print('workshop_invoice_serializer_errors: {0}'.format(invoice_serializer.errors))
            self.errors.append({'workshop_invoice_serializer_errors': invoice_serializer.errors})
        return JsonResponse({'received data': request.data, 'errors': self.errors, 'messages': self.messages}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid, format=None, *args, **kwargs):
        invoice = get_object_or_404(self.model, pk=uuid)
        invoice_serializer = self.serializer_class(invoice, data=request.data, partial=True)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_201_CREATED)
        else:
            self.errors.append({'invoice_serialzier_errors': invoice_serializer.errors})
            print('invoice_serialzier_errors: {0}'.format(invoice_serializer.errors))
            return JsonResponse({'received data': request.POST, 'errors': self.errors}, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        try:
            # get_object_or_404(self.model, uuid=uuid).delete()            
            # return JsonResponse({'deleted data': uuid}, safe=False, status=200)
            return JsonResponse({'deleted data': 'this object could not be deleted alone.'}, safe=False, status=400)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=500)
        except Exception as e:
            error_message = {'errors': [str(val)] for val in e}
            return JsonResponse(error_message, safe=False, status=500)

    
    def get_workshop_payment_serializer(self):
        if 'get' == self.request.method:
            return WPS
        else: return WPS

'''
8888888b.     d8888 Y88b   d88P 888b     d888 8888888888 888b    888 88888888888 
888   Y88b   d88888  Y88b d88P  8888b   d8888 888        8888b   888     888     
888    888  d88P888   Y88o88P   88888b.d88888 888        88888b  888     888     
888   d88P d88P 888    Y888P    888Y88888P888 8888888    888Y88b 888     888     
8888888P" d88P  888     888     888 Y888P 888 888        888 Y88b888     888     
888      d88P   888     888     888  Y8P  888 888        888  Y88888     888     
888     d8888888888     888     888   "   888 888        888   Y8888     888     
888    d88P     888     888     888       888 8888888888 888    Y888     888     
'''                                                                                                                                                               

from education.models import Workshop
import datetime
class WorkshopPaymentApi(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )
    serializer_class = WPS
    model = WorkshopPayment
    errors = []
    messages = []

    def get(self, request, format=None, *args, **kwargs):
        if request.GET.get('field'):
            field = request.GET.get('field')
            if 'all' == field:
                workshop_payments = self.model.objects.all()
                workshop_payments_serialized = self.serializer_class(workshop_payments, many=True)
            elif 'uuid' == field:
                workshop_payments = get_object_or_404(WorkshopPayment, uuid = request.GET.get('uuid'))
                workshop_payments_serialized = self.serializer_class(workshop_payments)
            elif 'user_workshop_uuid' == field:
                user = get_object_or_404(User, uuid=request.GET.get('user'))
                workshop = get_object_or_404(Workshop, uuid=request.GET.get('workshop'))
                workshop_payments = WorkshopPayment.objects.filter(workshop__id = workshop.id, user_id = user.id)
                for workshop in workshop_payments:
                    workshop_payments = workshop
                workshop_payments_serialized = self.serializer_class(workshop_payments)
            else:
                return JsonResponse({'error': "This url doesn't provide information based on your request information."}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            workshop_payments = self.model.objects.filter(user_id = request.user.id)
            workshop_payments_serialized = self.serializer_class(workshop_payments, many=True)
        return JsonResponse({'response': workshop_payments_serialized.data}, safe=False, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None, *args, **kwargs):
        self.errors = []
        print(request.data)
        workshop = get_object_or_404(Workshop, uuid=request.data.get('workshop'))
        user = get_object_or_404(User, uuid=request.data.get('user'))
        payment_serializer = self.serializer_class(data={'workshop': workshop.id, 'user': user.id})
        if payment_serializer.is_valid():
            from django.db.models import ProtectedError
            try:
                payment = payment_serializer.save()
                workshop = get_object_or_404(Workshop, uuid = request.data.get('workshop'))
                # from education.services import get_price
                # result = get_price(user, workshop)
                invoice = WorkshopInvoice.objects.create(amount_to_pay = workshop.price.get_price('rial'), index = 1, \
                    due_date = datetime.datetime.now().strftime('%Y-%m-%d'), created_by = request.user, payment = payment)
                invoice_serializer = WIS(invoice)
                return JsonResponse({'received data': request.data, 'invoice': invoice_serializer.data, 'errors': self.errors, 'messages': self.messages}, safe=False, status=status.HTTP_201_CREATED)
                
            except ProtectedError:
                error_message = "This object can't be deleted!!"
                return JsonResponse(error_message, status=500)
            except Exception as e:
                print(e)
                error_message = {'errors': '[str(val)] for val in e'}
                # return HttpResponse({'error_message': error_message, 'e': e}, safe=False, status=500)
                return HttpResponse({'error_message': error_message, 'e': e})

        else:
            self.errors.append({'workshop_payment_serializer_errors': payment_serializer.errors})
            print('workshop_payment_serializer_errors: {0}'.format(invoice_serializer.errors))
            return JsonResponse({'received data': request.data, 'invoice': 'There is bug on creating payment from server. Plz Call Us ASAP for any help.', 'errors': self.errors, 'messages': self.messages}, safe=False, status=status.HTTP_400_BAD_REQUEST)



        
