from django.contrib import admin
from django.apps import apps
from import_export import resources, fields, widgets
from . import models
from import_export.admin import ImportExportModelAdmin, ExportMixin

app = apps.get_app_config('main')

for model_name, model in app.models.items():
    admin.site.register(model)


class OrderResource(resources.ModelResource):
    class Meta:
        model = models.Order
        fields = (
            'order_number', 'profile', 'selection', 'status', 'transaction_date', 'amount', 'prn', 'bid', 'pid', 'tnc',
            'notInCollege', 'refund_requested', 'refund_processed', 'refund_reason', 'refund_approved_by', 'refund_approved_on'
        )


class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource


admin.site.unregister(models.Order)
admin.site.register(models.Order, OrderAdmin)


class SelectionResource(resources.ModelResource):
    class Meta:
        model = models.Selection
        fields = (
            'coupon_code', 'college', 'scholarship', 'fee', 'final_fee', 'course_name', 'college_qualification',
            'search', 'savings', 'total_savings', 'seats'
        )


class SelectionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SelectionResource


admin.site.unregister(models.Selection)
admin.site.register(models.Selection, SelectionAdmin)


class SearchResource(resources.ModelResource):
    class Meta:
        model = models.Search
        fields = (
            'level', 'city', 'course_type', 'course', 'q_exm', 'q_exm_score', 'compt_exm_type_1',
            'compt_exm_score_1', 'compt_exm_type_2', 'compt_exm_score_2', 'screen_6_text'
        )


class SearchAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SearchResource


admin.site.unregister(models.Search)
admin.site.register(models.Search, SearchAdmin)


class ProfileResource(resources.ModelResource):
    class Meta:
        model = models.Profile
        fields = (
            'user', 'name', 'id_type', 'id_no', 'dob', 'gender', 'otp', 'mobile', 'house', 'street', 'city',
            'district', 'state', 'country', 'pin', 'college', 'college_location', 'school', 'school_location',
            'class_12_year', 'graduation_year', 'terms_conditions', 'profile_image', 'tab_flag', 'phone',
            'parent_email', 'mobile_verified', 'email_verified'
        )


class ProfileAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProfileResource


admin.site.unregister(models.Profile)
admin.site.register(models.Profile, ProfileAdmin)
