from django.contrib import admin
from auth_app.models import CustomUser, PasswordReset
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from review_app.models import Review


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
    
@admin.register(Order)
class OrderDetailAmin(admin.ModelAdmin):
    list_display = ('customer_user', 'business_user', 'title', 'status', 'created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business_user', 'reviewer_id', 'rating', 'created_at', 'updated_at')
    search_fields = ('business_user__username', 'reviewer_id__username', 'rating', 'description')
    list_filter = ('rating', 'created_at')