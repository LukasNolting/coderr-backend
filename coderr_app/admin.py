from django.contrib import admin
from auth_app.models import CustomUser, PasswordReset
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from review_app.models import Review
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for managing CustomUser instances.
    """
    model = CustomUser

    list_display = ('username', 'email', 'type', 'is_active', 'created_at', 'first_name', 'last_name')
    list_filter = ('type', 'is_active', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours', 'file')
        }),
        ('Permissions and Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at')
        }),
        ('User Type', {
            'fields': ('type',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'type', 'is_active')
        }),
    )

    search_fields = ('username', 'email', 'type')

    ordering = ('created_at',)
    
admin.site.register(CustomUser, CustomUserAdmin)



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
