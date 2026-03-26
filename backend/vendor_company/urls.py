from django.urls import path,include
# from .api.login import urls as api_login_urls
from payment_module.views import getVendorMasterCardPayment,getMasterCardTransactionStatus,getMasterCardTransactionStatus

urlpatterns = [
    path('mastercard_transaction_status/', getMasterCardTransactionStatus, name='mastercard_transaction_status'),
    path('vendor_mastercard_payment/<uuid:id>/', getVendorMasterCardPayment, name='vendor_mastercard_payment'),
    path('public_mastercard_transaction_status/', getMasterCardTransactionStatus, name='public_mastercard_transaction_status'),
    # path('billing_mastercard_payment/<uuid:id>/', getBillingMasterCardPayment, name='billing_mastercard_payment'),
    # path('property_onelink_payment/<uuid:id>/', getOneLinkPayment, name='property_onelink_payment'),
    # path('property_rda_payment/<uuid:id>/', getRDAPayment, name='property_rda_payment'),
    # path('property_payment_voucher_number/<uuid:id>/', getChallanNumber, name='property_payment_voucher_number'),
    # path('property_payment_voucher_info/<uuid:id>/', getPaymentVoucherInfo, name='property_payment_voucher_info'),
    # path('property_payment_voucher_info_update/', updatePaymentVoucherInfo, name='property_payment_voucher_info_update'),
    # path('property_payment_voucher_download/<uuid:id>/', DownloadPropertyPaymentVoucher, name='property_payment_voucher_download'),
    # path('property_paid_payment_challan_upload/', PaidPropertyPaymentVoucherUpload, name='property_paid_payment_challan_upload'),
]


