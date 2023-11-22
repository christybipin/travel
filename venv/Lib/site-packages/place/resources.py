from place.api_resource import APIResource


class AccessToken(APIResource):
    resource = '/access_tokens'
    object_type = 'access_token'


class AutopayEnrollment(APIResource):
    resource = '/autopay_enrollments'
    object_type = 'autopay_enrollment'


class Event(APIResource):
    resource = '/events'
    object_type = 'event'


class Account(APIResource):
    resource = '/accounts'
    object_type = 'account'


class DepositAccount(APIResource):
    resource = '/deposit_accounts'
    object_type = 'deposit_account'


class Transaction(APIResource):
    resource = '/transactions'
    object_type = 'transaction'


class TransactionAllocation(APIResource):
    resource = '/transaction_allocations'
    object_type = 'transaction_allocation'


class PaymentMethod(APIResource):
    resource = '/payment_methods'
    object_type = 'payment_method'


class Address(APIResource):
    resource = '/addresses'
    object_type = 'address'


class RecurringInvoice(APIResource):
    resource = '/recurring_invoices'
    object_type = 'recurring_invoice'


class Invoice(APIResource):
    resource = '/invoices'
    object_type = 'invoice'


class InvoiceItem(APIResource):
    resource = '/invoice_items'
    object_type = 'invoice_item'


class InvoicePayer(APIResource):
    resource = '/invoice_payers'
    object_type = 'invoice_payer'


class InvoiceItemAllocation(APIResource):
    resource = '/invoice_item_allocations'
    object_type = 'invoice_item_allocation'
