"""
URL configuration for inkagrowth project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from front import views as front_views
from crm import views as crm_views
from django.conf.urls.static import static

# =========================================================
# FRONTEND VIEWS
# =========================================================
urlpatterns = [

    # =====================================================
    # ADMIN PANEL
    # =====================================================

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        "sitemap.xml",
        front_views.sitemap_xml,
        name="sitemap"
    ),

    path(
        "sitemap-services.xml",
        front_views.sitemap_services_xml,
        name="sitemap_services"
    ),

    path(
        "sitemap-pages.xml",
        front_views.sitemap_pages_xml,
        name="sitemap_pages"
    ),

path("ping/", front_views.ping),

path(
    'robots.txt',
    front_views.robots_txt,
    name='robots_txt'
),

    # =====================================================
    # WEBSITE FRONTEND
    # =====================================================

    path(
        '',
        front_views.index,
        name='index'
    ),

    path(
        'seo-services/',
        front_views.service_page,
        {'slug': 'seo-services'},
        name='seo_services'
    ),

    path(
        'social-media-marketing/',
        front_views.service_page,
        {'slug': 'social-media-marketing'},
        name='social_media_marketing'
    ),

    path(
        'google-ads-services/',
        front_views.service_page,
        {'slug': 'google-ads-services'},
        name='google_ads_services'
    ),

    path(
        'website-development/',
        front_views.service_page,
        {'slug': 'website-development'},
        name='website_development'
    ),

    path(
        'digital-marketing-services/',
        front_views.service_page,
        {'slug': 'digital-marketing-services'},
        name='digital_marketing_services'
    ),

    path(
        'privacy-policy/',
        front_views.legal_page,
        {'slug': 'privacy-policy'},
        name='privacy_policy'
    ),

    path(
        'terms-and-conditions/',
        front_views.legal_page,
        {'slug': 'terms-and-conditions'},
        name='terms_and_conditions'
    ),

    path(
        'disclaimer/',
        front_views.legal_page,
        {'slug': 'disclaimer'},
        name='disclaimer'
    ),

    path(
        'cookie-policy/',
        front_views.legal_page,
        {'slug': 'cookie-policy'},
        name='cookie_policy'
    ),

    path(
        'contact/',
        front_views.contact_page,
        name='contact'
    ),

    path(
        'team/',
        front_views.team_page,
        name='team'
    ),


    # =====================================================
    # CRM AUTHENTICATION
    # =====================================================

    path(
        'crm/login/',
        crm_views.login_view,
        name='login'
    ),

    path(
        'crm/logout/',
        crm_views.logout_view,
        name='logout'
    ),


    # =====================================================
    # CRM DASHBOARD
    # =====================================================

    path(
        'crm/dashboard/',
        crm_views.dashboard,
        name='dashboard'
    ),


    # =====================================================
    # LEADS
    # =====================================================

    path(
        'crm/leads/',
        crm_views.lead_list,
        name='lead_list'
    ),

    path(
        'crm/leads/add/',
        crm_views.add_lead,
        name='add_lead'
    ),

    path(
        'crm/leads/export/csv/',
        crm_views.export_leads_csv,
        name='export_leads_csv'
    ),

    path(
        'crm/leads/<uuid:pk>/',
        crm_views.lead_detail,
        name='lead_detail'
    ),

    path(
        'crm/leads/<uuid:pk>/edit/',
        crm_views.edit_lead,
        name='edit_lead'
    ),

    path(
        'crm/leads/<uuid:pk>/delete/',
        crm_views.delete_lead,
        name='delete_lead'
    ),

    path(
        'crm/leads/<uuid:pk>/convert/',
        crm_views.convert_lead_to_client,
        name='convert_lead_to_client'
    ),


    # =====================================================
    # FOLLOWUPS
    # =====================================================

    path(
        'crm/leads/<uuid:pk>/followup/add/',
        crm_views.add_followup,
        name='add_followup'
    ),

    path(
        'crm/followup/<uuid:pk>/complete/',
        crm_views.complete_followup,
        name='complete_followup'
    ),


    # =====================================================
    # LEAD NOTES
    # =====================================================

    path(
        'crm/leads/<uuid:pk>/note/add/',
        crm_views.add_lead_note,
        name='add_lead_note'
    ),


    # =====================================================
    # COMMUNICATIONS
    # =====================================================

    path(
        'crm/leads/<uuid:pk>/communication/add/',
        crm_views.add_communication,
        name='add_communication'
    ),


    # =====================================================
    # CLIENTS
    # =====================================================

    path(
        'crm/clients/',
        crm_views.client_list,
        name='client_list'
    ),

    path(
        'crm/clients/add/',
        crm_views.add_client,
        name='add_client'
    ),

    path(
        'crm/clients/<uuid:pk>/',
        crm_views.client_detail,
        name='client_detail'
    ),

    path(
        'crm/clients/<uuid:pk>/edit/',
        crm_views.edit_client,
        name='edit_client'
    ),

    path(
        'crm/clients/<uuid:pk>/delete/',
        crm_views.delete_client,
        name='delete_client'
    ),


    # =====================================================
    # CLIENT FILES
    # =====================================================

    path(
        'crm/clients/<uuid:pk>/upload-file/',
        crm_views.upload_client_file,
        name='upload_client_file'
    ),

    path(
        'crm/files/<uuid:pk>/delete/',
        crm_views.delete_client_file,
        name='delete_client_file'
    ),


    # =====================================================
    # TASKS
    # =====================================================

    path(
        'crm/tasks/',
        crm_views.task_list,
        name='task_list'
    ),

    path(
        'crm/tasks/add/',
        crm_views.add_task,
        name='add_task'
    ),

    path(
        'crm/tasks/<uuid:pk>/edit/',
        crm_views.edit_task,
        name='edit_task'
    ),

    path(
        'crm/tasks/<uuid:pk>/delete/',
        crm_views.delete_task,
        name='delete_task'
    ),

    path(
        'crm/tasks/<uuid:pk>/status/update/',
        crm_views.update_task_status,
        name='update_task_status'
    ),


    # =====================================================
    # PAYMENTS
    # =====================================================

    path(
        'crm/payments/',
        crm_views.payment_list,
        name='payment_list'
    ),

    path(
        'crm/clients/<uuid:pk>/payment/add/',
        crm_views.add_payment,
        name='add_payment'
    ),

    path(
        'crm/payments/<uuid:pk>/delete/',
        crm_views.delete_payment,
        name='delete_payment'
    ),


    # =====================================================
    # SERVICES
    # =====================================================

    path(
        'crm/services/',
        crm_views.service_list,
        name='service_list'
    ),

    path(
        'crm/services/add/',
        crm_views.add_service,
        name='add_service'
    ),


    # =====================================================
    # ACTIVITY LOGS
    # =====================================================

    path(
        'crm/activity-logs/',
        crm_views.activity_logs,
        name='activity_logs'
    ),


    # =====================================================
    # DYNAMIC WEBSITE PAGES
    # =====================================================

    # IMPORTANT:
    # This route MUST stay at the bottom.
    # Otherwise it will capture all CRM URLs.
    path(
        '<slug:slug>/',
        front_views.dynamic_page,
        name='dynamic_page'
    ),

]


# =========================================================
# MEDIA FILES
# =========================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
