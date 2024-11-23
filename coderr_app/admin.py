from django.contrib import admin
from auth_app.models import CustomUser, PasswordReset
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from review_app.models import Review


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the CustomUser model.

    Displays user-specific fields such as email, username, and status,
    and provides filtering, searching, and ordering options.
    """
    list_display = ('email', 'username', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('email',)


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the PasswordReset model.

    Provides a view of password reset requests, including token and creation date,
    and supports searching and filtering by email and creation date.
    """
    list_display = ('email', 'token', 'created_at')
    search_fields = ('email', 'token')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Offer model.

    Displays offers created by users with fields such as title and timestamps.
    """
    list_display = ('user', 'title', 'created_at', 'updated_at')


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the OfferDetail model.

    Provides detailed information about offers, such as price,
    delivery time, and number of revisions.
    """
    list_display = ('title', 'offer_type', 'offer', 'price', 'delivery_time_in_days', 'revisions')


@admin.register(Order)
class OrderDetailAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Order model.

    Displays customer and business user interactions, including order status,
    and creation and update timestamps.
    """
    list_display = ('customer_user', 'business_user', 'title', 'status', 'created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Review model.

    Displays reviews with fields such as business user, reviewer,
    rating, and timestamps. Supports searching and filtering by user and rating.
    """
    list_display = ('business_user', 'reviewer_id', 'rating', 'created_at', 'updated_at')
    search_fields = ('business_user__username', 'reviewer_id__username', 'rating', 'description')
    list_filter = ('rating', 'created_at')
