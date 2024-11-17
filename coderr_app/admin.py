from django.contrib import admin
from auth_app.models import CustomUser, PasswordReset
from offers_app.models import Offer, OfferDetail

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('email',)

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at')
    search_fields = ('email', 'token')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer_type', 'offer', 'price', 'delivery_time_in_days','revisions')