from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime
from geoinfo.models import Country,City,State
from django.contrib import messages
from core.models import SystemStatus
from housing_society.models import Society
from housing_society.models import BankAttribute
from application_form.models import PaymentScheduleDetail,PaymentChallan
from payment_module.models import PaymentChallanDetail,TransactionDetail,Billing
from payment_module.utils.IPGInstallmentPaymentChallan import IPGInstallmentPaymentChallan
from payment_module.utils.IPGBillingPaymentChallan import IPGBillingPaymentChallan
from payment_module.utils.PaymentScheduleUpdate import PaymentScheduleUpdate
from payment_module.utils.OneLinkPaymentChallan import OneLinkInstallmentPaymentChallan
from payment_module.utils.RDAPaymentChallan import RDAInstallmentPaymentChallan
from housing_society.utils.MasterCardApi import MasterCardApi
from include.getGenericForeignKeyMeta import getGenericForeignKeyMeta
from django.http import HttpResponse,JsonResponse
from include.getIP import get_client_ip,get_country_state_city_ip
from notifications.helper.NotificationBroadcaster import NotificationBroadcaster
from notifications.models import NotificationChannel

@login_required
def getBillingMasterCardPayment(request,id):
    if request.method == 'GET':
        if request.user.type.code == "new_member_user":
            if id is not None:
                billing = Billing.objects.filter(user_id=request.user.id,id=id).first()
                bank_attribute = BankAttribute.objects.filter(bank__status='active',payment_method__system_code='ipg').first()
                if billing is not None and bank_attribute is not None:
                    payment_challan = IPGBillingPaymentChallan(request, billing)
                    if payment_challan is not None:
                        notification_broadcaster = NotificationBroadcaster()
                        notification_broadcaster.Create(request, payment_challan)
                        master_card = MasterCardApi(payment_challan.serial_number, payment_challan)
                        session_data = master_card.getSession()
                        if payment_challan is not None and session_data is not None:
                            notification_broadcaster = NotificationBroadcaster()
                            notification_broadcaster.Create(request, payment_challan)
                            data = {}
                            data['society'] = Society.objects.filter(status='active').first()
                            data['billing'] = billing
                            data['payment_challan'] = payment_challan
                            data['session_id'] = session_data['session']['id']
                            return render(request, 'admin/member/utility_billing/ipg_payment_template.html', data)
                        return HttpResponse("Sorry! Payment Gateway not Available this Time, Try again Later ")
                    else:
                        return HttpResponse("Sorry! Payment Challan Already in Process")
                return HttpResponse("Sorry! Data Not Founded 1")
            return HttpResponse("Sorry! Data Not Founded 2")
        return HttpResponse("Sorry! Your Role not Allowed")
    return HttpResponse("Sorry! Method not Allowed")

def getMasterCardPayment(request,id):
    if request.method == 'GET':
            if id is not None:
                payment_schedule_detail = PaymentScheduleDetail.objects.filter(user_id=request.user.id,id=id).first()
                bank_attribute = BankAttribute.objects.filter(bank__status='active',payment_method__system_code='ipg').first()
                if payment_schedule_detail is not None and bank_attribute is not None:
                    payment_challan = IPGInstallmentPaymentChallan(request, payment_schedule_detail)
                    if payment_challan is not None:
                        # notification_broadcaster = NotificationBroadcaster()
                        # notification_broadcaster.Create(request, payment_challan)
                        master_card = MasterCardApi(payment_challan.serial_number, payment_challan)
                        session_data = master_card.getSession()
                        if payment_challan is not None and session_data is not None:
                            data = {}
                            data['society'] = Society.objects.filter(status='active').first()
                            data['payment_schedule_detail'] = payment_schedule_detail
                            data['payment_challan'] = payment_challan
                            data['session_id'] = session_data['session']['id']
                            return render(request, 'admin/member/payment_schedule/ipg_payment_template.html', data)
                        return HttpResponse("Sorry! Payment Gateway not Available this Time, Try again Later ")
                    else:
                        return HttpResponse("Sorry! Payment Challan Already in Process")
                return HttpResponse("Sorry! Data Not Founded")
            return HttpResponse("Sorry! Data Not Founded")
    return HttpResponse("Sorry! Method not Allowed")



@login_required
def getMasterCardTransactionStatus(request):
    if request.method == 'POST':
        if request.user.type.code == "new_member_user":
            order_id = request.POST.get('order_id', None)
            if order_id is not None:
                payment_challan = PaymentChallan.objects.filter(serial_number=order_id).first()
                if payment_challan is not None:
                    master_card = MasterCardApi(order_id,payment_challan)
                    order_data = master_card.getOrderStatus()
                    geo_dict = get_country_state_city_ip(request)
                    if order_data is not None and order_data['result'] == "SUCCESS":
                        amount = order_data['amount']
                        paid_time = order_data["creationTime"]
                        generic_foreign_key = getGenericForeignKeyMeta()
                        payment_challan.transaction_data = generic_foreign_key.getJson(order_data)
                        if payment_challan.challan_amount == amount:
                            payment_challan.paid_amount = amount
                            payment_challan.paid_at = paid_time
                            payment_challan.national_identity_number = request.user.national_identity_number
                            payment_challan.national_identity_type = request.user.national_identity_type
                            payment_status = SystemStatus.objects.filter(system_code='finance_pending').first()
                            payment_challan.status = payment_status
                            notification_broadcaster = NotificationBroadcaster()
                            notification_broadcaster.Create(request, payment_challan)
                            payment_challan.save()
                            if generic_foreign_key.getObjectModelKey(payment_challan.content_object) == "payment_module_paymentschedule":
                                payment_schedule_update = PaymentScheduleUpdate(payment_challan.member)
                                payment_schedule_update.UpdateStatus()

                            PaymentChallanDetail.objects.filter(payment_challan_id=payment_challan.id).update(status=payment_status)
                            payment_challan_details = PaymentChallanDetail.objects.filter(payment_challan_id=payment_challan.id)
                            for pcd in payment_challan_details:
                                related_object_detail = pcd.content_detail_object
                                related_object_detail.status = payment_status
                                related_object_detail.save()

                        
                            transaction_data = TransactionDetail.objects.filter(payment_challan_id=payment_challan.id).first()
                            if transaction_data is None:
                                transaction_data = TransactionDetail()
                            transaction_data.ip = get_client_ip(request)
                            transaction_data.user = request.user
                            transaction_data.member = payment_challan.member
                            transaction_data.society = payment_challan.society
                            transaction_data.project = payment_challan.project
                            transaction_data.property_info = payment_challan.property_info
                            transaction_data.category = payment_challan.category
                            transaction_data.area = payment_challan.area
                            transaction_data.payment_module_no = payment_challan.payment_module_no
                            transaction_data.consumerid = payment_challan.consumerid
                            transaction_data.serial_number = payment_challan.serial_number
                            transaction_data.payment_challan = payment_challan
                            transaction_data.challan_amount = payment_challan.challan_amount
                            transaction_data.received_amount = amount
                            transaction_data.remaining_amount = transaction_data.challan_amount - amount
                            transaction_data.transaction_creation_at = order_data['creationTime']
                            transaction_data.transaction_last_updated_at = order_data['lastUpdatedTime']
                            transaction_data.currency = order_data['merchantCurrency']
                            source_of_funds = order_data['sourceOfFunds']['provided']['card']
                            transaction_data.name_on_card = source_of_funds['nameOnCard']
                            transaction_data.card_number = source_of_funds['number']
                            transaction_data.status = str(order_data['status'])
                            transaction_data.save()


                            data = {'status': 1, 'data':{}}
                            return JsonResponse(data)
                        else:
                            data = {'status': 1, 'data': {}}
                            return JsonResponse(data)
                    else:
                        data = {'status': 0, 'data': {}}
                        return JsonResponse(data)
                else:
                    data = {'status': 0, 'data': {'msg': 'Order Not Founded'}}
                    return JsonResponse(data)
            else:
                data = {'status': 0, 'data': {'msg': 'Order Id is None'}}
                return JsonResponse(data)
        else:
            data = {'status': 0, 'data': {'msg': 'Request user not allowed'}}
            return JsonResponse(data)
    else:
        data = {'status': 0, 'data': {'msg': 'Request method not allowed'}}
        return JsonResponse(data)

