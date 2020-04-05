from django.contrib import admin
from core.models import *

# Register your models here.

class LoaneeAdmin(admin.ModelAdmin):
    list_display = (
                    'first_name',
                    'last_name',
                    'phone_number',
                    'email'
                    )
admin.site.register(Loanee, LoaneeAdmin)


class LenderAdmin(admin.ModelAdmin):
    list_display = (
                    'name',
                    'account_number',
                    )
admin.site.register(Lender, LenderAdmin)

class WalletAdmin(admin.ModelAdmin):
    list_display = (
                    'account_balance',
                    'savings_balance',
                    'total_spending',
                    )
admin.site.register(Wallet, WalletAdmin)

class OutboxAdmin(admin.ModelAdmin):
    list_display = (
                    'recipient',
                    'message',
                    'message_type',
                    'sent',
                    'sent_time',
                    'delivered',
                    'delivered_time',
                    'ait_delivery_status',
                    'ait_failure_reason',
                   )
admin.site.register(Outbox, OutboxAdmin)

class SavingMethodTypeAdmin(admin.ModelAdmin):
    list_display = (
                    'name',
                    )
admin.site.register(SavingMethodType, SavingMethodTypeAdmin)

class SavingFrequencyAdmin(admin.ModelAdmin):
    list_display = (
                    'name',
                    'duration'
                    )
admin.site.register(SavingFrequency, SavingFrequencyAdmin)


class SavingMethodAdmin(admin.ModelAdmin):
    list_display = (
                    'saving_type',
                    'saving_rate',
                    'frequency',
                    )
admin.site.register(SavingMethod, SavingMethodAdmin)


class PhoneOtpAdmin(admin.ModelAdmin):
    list_display = (
                    'phone_number',
                    'otp_code',
                    'count',
                    'validated'
                    )
admin.site.register(PhoneOtp, PhoneOtpAdmin)

class LoanAdmin(admin.ModelAdmin):
    list_display = (
                    'reference_number',
                    'amount',
                    'financier',
                    'interest_rate',
                    'interest_rate',
                    'period',
                    'disbursement_date',
                    )
admin.site.register(Loan, LoanAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
                    'reference_number',
                    'amount',
                    'recipient',
                    'successful',
                    'time',
                    )
admin.site.register(Transaction, TransactionAdmin)


admin.site.site_header = 'Habahaba Admin Panel '
