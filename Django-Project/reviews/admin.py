from django.contrib import admin

# Register your models here.
from reviews.models import Reviews


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('productid','userid','profilename','score')
    ordering = ('id',)

admin.site.register(Reviews, ReviewsAdmin)
