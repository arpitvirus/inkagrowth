import csv

# Complete Django CRM `views.py`
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST

from .models import *
from .utils.google_sheets import sync_lead_to_google_sheet


def optional_value(value):
    return value or None


def decimal_value(value, default=0):
    return value if value not in (None, '') else default


def user_display_name(user):
    if not user:
        return ''

    return user.get_full_name() or user.username


def aware_datetime_value(value):
    parsed_datetime = parse_datetime(value) if value else None

    if parsed_datetime is None:
        return optional_value(value)

    if timezone.is_naive(parsed_datetime):
        return timezone.make_aware(
            parsed_datetime,
            timezone.get_current_timezone()
        )

    return parsed_datetime


# =========================================================
# AUTHENTICATION VIEWS
# =========================================================


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'crm/auth/login.html')


@login_required
def logout_view(request):

    logout(request)
    messages.success(request, 'Logout successful')

    return redirect('login')


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    total_leads = Lead.objects.filter(
        is_deleted=False
    ).count()

    total_clients = Client.objects.filter(
        is_deleted=False
    ).count()

    total_tasks = Task.objects.filter(
        is_deleted=False
    ).count()

    pending_followups = FollowUp.objects.filter(
        status='pending',
        is_deleted=False
    ).count()

    completed_tasks = Task.objects.filter(
        status='completed',
        is_deleted=False
    ).count()

    total_revenue = Payment.objects.filter(
        payment_status='paid',
        is_deleted=False
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    recent_leads = Lead.objects.filter(
        is_deleted=False
    ).order_by('-created_at')[:5]

    recent_tasks = Task.objects.filter(
        is_deleted=False
    ).order_by('-created_at')[:5]

    upcoming_followups = FollowUp.objects.filter(
        status='pending',
        is_deleted=False
    ).order_by('followup_date')[:5]

    lead_status_counts = {
        item['status']: item['total']
        for item in Lead.objects.filter(is_deleted=False)
        .values('status')
        .annotate(total=Count('id'))
    }

    task_status_counts = {
        item['status']: item['total']
        for item in Task.objects.filter(is_deleted=False)
        .values('status')
        .annotate(total=Count('id'))
    }

    context = {
        'total_leads': total_leads,
        'total_clients': total_clients,
        'total_tasks': total_tasks,
        'pending_followups': pending_followups,
        'completed_tasks': completed_tasks,
        'total_revenue': total_revenue,
        'recent_leads': recent_leads,
        'recent_tasks': recent_tasks,
        'upcoming_followups': upcoming_followups,
        'chart_data': {
            'lead_status_labels': [label for _, label in Lead.STATUS_CHOICES],
            'lead_status_values': [
                lead_status_counts.get(value, 0)
                for value, _ in Lead.STATUS_CHOICES
            ],
            'task_status_labels': [label for _, label in Task.STATUS_CHOICES],
            'task_status_values': [
                task_status_counts.get(value, 0)
                for value, _ in Task.STATUS_CHOICES
            ],
        }
    }

    return render(request, 'crm/dashboard/dashboard.html', context)


# =========================================================
# LEAD VIEWS
# =========================================================

@login_required
def lead_list(request):

    search = request.GET.get('search')
    status = request.GET.get('status')

    leads = Lead.objects.filter(
        is_deleted=False
    ).order_by('-created_at')

    if search:
        leads = leads.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(company_name__icontains=search)
        )

    if status:
        leads = leads.filter(status=status)

    paginator = Paginator(leads, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'status_choices': Lead.STATUS_CHOICES,
    }

    return render(request, 'crm/leads/lead_list.html', context)


@login_required
def add_lead(request):

    services = Service.objects.filter(is_deleted=False)
    users = User.objects.all()

    if request.method == 'POST':

        lead = Lead.objects.create(
            name=request.POST.get('name'),
            company_name=request.POST.get('company_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            website=optional_value(request.POST.get('website')),
            lead_source=request.POST.get('lead_source') or 'website',
            interested_service_id=optional_value(request.POST.get('service')),
            budget=decimal_value(request.POST.get('budget')),
            status=request.POST.get('status') or 'new',
            pipeline_stage=request.POST.get('pipeline_stage') or 'new_lead',
            assigned_to_id=optional_value(request.POST.get('assigned_to')),
            notes=request.POST.get('notes'),
            created_by=request.user
        )

        ActivityLog.objects.create(
            user=request.user,
            action='lead_created',
            description=f'Lead {lead.name} created'
        )

        sheet_result = sync_lead_to_google_sheet(lead)
        if not sheet_result.success and not sheet_result.skipped:
            messages.warning(
                request,
                'Lead saved, but Google Sheets sync failed. Please check server logs.'
            )

        messages.success(request, 'Lead added successfully')

        return redirect('lead_list')

    context = {
        'services': services,
        'users': users,
        'lead_source_choices': Lead.LEAD_SOURCE_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,
        'pipeline_choices': Lead.PIPELINE_CHOICES,
    }

    return render(request, 'crm/leads/add_lead.html', context)


@login_required
def lead_detail(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk,
        is_deleted=False
    )

    followups = lead.followups.filter(
        is_deleted=False
    ).order_by('-created_at')

    notes = lead.lead_notes.filter(
        is_deleted=False
    ).order_by('-created_at')

    communications = lead.communications.filter(
        is_deleted=False
    ).order_by('-created_at')

    context = {
        'lead': lead,
        'followups': followups,
        'notes': notes,
        'communications': communications,
    }

    return render(request, 'crm/leads/lead_detail.html', context)


@login_required
def edit_lead(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk,
        is_deleted=False
    )

    services = Service.objects.filter(is_deleted=False)
    users = User.objects.all()

    if request.method == 'POST':

        lead.name = request.POST.get('name')
        lead.company_name = request.POST.get('company_name')
        lead.email = request.POST.get('email')
        lead.phone = request.POST.get('phone')
        lead.website = optional_value(request.POST.get('website'))
        lead.lead_source = request.POST.get('lead_source') or 'website'
        lead.interested_service_id = optional_value(request.POST.get('service'))
        lead.budget = decimal_value(request.POST.get('budget'))
        lead.status = request.POST.get('status') or 'new'
        lead.pipeline_stage = request.POST.get('pipeline_stage') or 'new_lead'
        lead.assigned_to_id = optional_value(request.POST.get('assigned_to'))
        lead.notes = request.POST.get('notes')

        lead.save()

        ActivityLog.objects.create(
            user=request.user,
            action='lead_updated',
            description=f'Lead {lead.name} updated'
        )

        messages.success(request, 'Lead updated successfully')

        return redirect('lead_detail', pk=lead.pk)

    context = {
        'lead': lead,
        'services': services,
        'users': users,
        'lead_source_choices': Lead.LEAD_SOURCE_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,
        'pipeline_choices': Lead.PIPELINE_CHOICES,
    }

    return render(request, 'crm/leads/edit_lead.html', context)


@login_required
def export_leads_csv(request):

    timestamp = timezone.localtime().strftime('%Y%m%d-%H%M%S')
    filename = f'leads-export-{timestamp}.csv'

    response = HttpResponse(
        content_type='text/csv; charset=utf-8'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # UTF-8 BOM keeps Microsoft Excel from misreading non-ASCII text.
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow([
        'Lead ID',
        'Name',
        'Email',
        'Phone',
        'Company Name',
        'Lead Source',
        'Interested Service',
        'Budget',
        'Lead Status',
        'Pipeline Stage',
        'Assigned To',
        'Created By',
        'Created Date',
        'Notes',
    ])

    leads = Lead.objects.filter(
        is_deleted=False
    ).select_related(
        'interested_service',
        'assigned_to',
        'created_by',
    ).order_by('-created_at')

    for lead in leads:
        writer.writerow([
            str(lead.pk),
            lead.name,
            lead.email or '',
            lead.phone or '',
            lead.company_name or '',
            lead.get_lead_source_display(),
            lead.interested_service.name if lead.interested_service else '',
            lead.budget if lead.budget is not None else '',
            lead.get_status_display(),
            lead.get_pipeline_stage_display(),
            user_display_name(lead.assigned_to),
            user_display_name(lead.created_by),
            timezone.localtime(lead.created_at).strftime('%Y-%m-%d %H:%M:%S'),
            lead.notes or '',
        ])

    return response


@login_required
def delete_lead(request, pk):

    lead = get_object_or_404(Lead, pk=pk, is_deleted=False)

    lead.is_deleted = True
    lead.save()

    messages.success(request, 'Lead deleted successfully')

    return redirect('lead_list')


@login_required
def convert_lead_to_client(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk,
        is_deleted=False
    )

    client = Client.objects.create(
        name=lead.name,
        company_name=lead.company_name,
        email=lead.email,
        phone=lead.phone,
        website=lead.website,
        service=lead.interested_service,
        created_by=request.user
    )

    lead.status = 'converted'
    lead.pipeline_stage = 'won'
    lead.save()

    ActivityLog.objects.create(
        user=request.user,
        action='client_created',
        description=f'Lead {lead.name} converted to client'
    )

    messages.success(request, 'Lead converted successfully')

    return redirect('client_detail', pk=client.pk)


# =========================================================
# FOLLOWUP VIEWS
# =========================================================

@login_required
def add_followup(request, pk):

    lead = get_object_or_404(Lead, pk=pk, is_deleted=False)

    if request.method == 'POST':

        FollowUp.objects.create(
            lead=lead,
            followup_date=aware_datetime_value(request.POST.get('followup_date')),
            note=request.POST.get('note'),
            created_by=request.user
        )

        ActivityLog.objects.create(
            user=request.user,
            action='followup_added',
            description=f'Follow-up added for {lead.name}'
        )

        messages.success(request, 'Follow-up added successfully')

        return redirect('lead_detail', pk=lead.pk)

    context = {
        'lead': lead
    }

    return render(request, 'crm/followups/add_followup.html', context)


@login_required
def complete_followup(request, pk):

    followup = get_object_or_404(FollowUp, pk=pk, is_deleted=False)

    followup.status = 'completed'
    followup.save()

    messages.success(request, 'Follow-up completed')

    return redirect('lead_detail', pk=followup.lead.pk)


# =========================================================
# CLIENT VIEWS
# =========================================================

@login_required
def client_list(request):

    search = request.GET.get('search')
    status = request.GET.get('status')

    clients = Client.objects.filter(
        is_deleted=False
    ).order_by('-created_at')

    if search:
        clients = clients.filter(
            Q(name__icontains=search) |
            Q(company_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    if status:
        clients = clients.filter(status=status)

    paginator = Paginator(clients, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'status_choices': Client.STATUS_CHOICES,
    }

    return render(request, 'crm/clients/client_list.html', context)


@login_required
def add_client(request):

    services = Service.objects.filter(is_deleted=False)

    if request.method == 'POST':

        Client.objects.create(
            name=request.POST.get('name'),
            company_name=request.POST.get('company_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            website=optional_value(request.POST.get('website')),
            address=request.POST.get('address'),
            service_id=optional_value(request.POST.get('service')),
            monthly_charges=decimal_value(request.POST.get('monthly_charges')),
            renewal_date=optional_value(request.POST.get('renewal_date')),
            status=request.POST.get('status') or 'active',
            notes=request.POST.get('notes'),
            created_by=request.user
        )

        messages.success(request, 'Client added successfully')

        return redirect('client_list')

    context = {
        'services': services,
        'status_choices': Client.STATUS_CHOICES,
    }

    return render(request, 'crm/clients/add_client.html', context)


@login_required
def client_detail(request, pk):

    client = get_object_or_404(
        Client,
        pk=pk,
        is_deleted=False
    )

    payments = client.payments.filter(
        is_deleted=False
    ).order_by('-created_at')

    files = client.files.filter(
        is_deleted=False
    ).order_by('-created_at')

    context = {
        'client': client,
        'payments': payments,
        'files': files,
    }

    return render(request, 'crm/clients/client_detail.html', context)


@login_required
def edit_client(request, pk):

    client = get_object_or_404(Client, pk=pk, is_deleted=False)
    services = Service.objects.filter(is_deleted=False)

    if request.method == 'POST':

        client.name = request.POST.get('name')
        client.company_name = request.POST.get('company_name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.website = optional_value(request.POST.get('website'))
        client.address = request.POST.get('address')
        client.service_id = optional_value(request.POST.get('service'))
        client.monthly_charges = decimal_value(request.POST.get('monthly_charges'))
        client.renewal_date = optional_value(request.POST.get('renewal_date'))
        client.status = request.POST.get('status') or 'active'
        client.notes = request.POST.get('notes')

        client.save()

        messages.success(request, 'Client updated successfully')

        return redirect('client_detail', pk=client.pk)

    context = {
        'client': client,
        'services': services,
        'status_choices': Client.STATUS_CHOICES,
    }

    return render(request, 'crm/clients/edit_client.html', context)


@login_required
def delete_client(request, pk):

    client = get_object_or_404(Client, pk=pk, is_deleted=False)

    client.is_deleted = True
    client.save()

    messages.success(request, 'Client deleted successfully')

    return redirect('client_list')


# =========================================================
# TASK VIEWS
# =========================================================

@login_required
def task_list(request):

    search = request.GET.get('search')
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    tasks = Task.objects.filter(
        is_deleted=False
    ).order_by('-created_at')

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(related_client__name__icontains=search)
        )

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    paginator = Paginator(tasks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'priority': priority,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }

    return render(request, 'crm/tasks/task_list.html', context)


@login_required
def add_task(request):

    users = User.objects.all()

    clients = Client.objects.filter(
        is_deleted=False
    )

    if request.method == 'POST':

        Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            assigned_to_id=optional_value(request.POST.get('assigned_to')),
            related_client_id=optional_value(request.POST.get('related_client')),
            due_date=optional_value(request.POST.get('due_date')),
            priority=request.POST.get('priority') or 'medium',
            status=request.POST.get('status') or 'pending',
            created_by=request.user
        )

        ActivityLog.objects.create(
            user=request.user,
            action='task_created',
            description='Task created'
        )

        messages.success(request, 'Task added successfully')

        return redirect('task_list')

    context = {
        'users': users,
        'clients': clients,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }

    return render(request, 'crm/tasks/add_task.html', context)


@login_required
def edit_task(request, pk):

    task = get_object_or_404(Task, pk=pk, is_deleted=False)

    users = User.objects.all()
    clients = Client.objects.filter(is_deleted=False)

    if request.method == 'POST':

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.assigned_to_id = optional_value(request.POST.get('assigned_to'))
        task.related_client_id = optional_value(request.POST.get('related_client'))
        task.due_date = optional_value(request.POST.get('due_date'))
        task.priority = request.POST.get('priority') or 'medium'
        task.status = request.POST.get('status') or 'pending'

        task.save()

        messages.success(request, 'Task updated successfully')

        return redirect('task_list')

    context = {
        'task': task,
        'users': users,
        'clients': clients,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }

    return render(request, 'crm/tasks/edit_task.html', context)


@login_required
def delete_task(request, pk):

    task = get_object_or_404(Task, pk=pk, is_deleted=False)

    task.is_deleted = True
    task.save()

    messages.success(request, 'Task deleted successfully')

    return redirect('task_list')


# =========================================================
# PAYMENT VIEWS
# =========================================================

@login_required
def add_payment(request, pk):

    client = get_object_or_404(Client, pk=pk, is_deleted=False)

    if request.method == 'POST':

        Payment.objects.create(
            client=client,
            amount=request.POST.get('amount'),
            payment_date=request.POST.get('payment_date'),
            next_payment_date=optional_value(request.POST.get('next_payment_date')),
            payment_status=request.POST.get('payment_status') or 'pending',
            notes=request.POST.get('notes')
        )

        ActivityLog.objects.create(
            user=request.user,
            action='payment_added',
            description='Payment added'
        )

        messages.success(request, 'Payment added successfully')

        return redirect('client_detail', pk=client.pk)

    context = {
        'client': client,
        'payment_status_choices': Payment.PAYMENT_STATUS,
    }

    return render(request, 'crm/payments/add_payment.html', context)


@login_required
def payment_list(request):

    search = request.GET.get('search')
    status = request.GET.get('status')

    payments = Payment.objects.filter(
        is_deleted=False
    ).select_related('client').order_by('-payment_date', '-created_at')

    if search:
        payments = payments.filter(
            Q(client__name__icontains=search) |
            Q(client__company_name__icontains=search) |
            Q(notes__icontains=search)
        )

    if status:
        payments = payments.filter(payment_status=status)

    paginator = Paginator(payments, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'status_choices': Payment.PAYMENT_STATUS,
    }

    return render(request, 'crm/payments/payment_list.html', context)


@login_required
def delete_payment(request, pk):

    payment = get_object_or_404(Payment, pk=pk, is_deleted=False)

    payment.is_deleted = True
    payment.save()

    messages.success(request, 'Payment deleted successfully')

    return redirect('client_detail', pk=payment.client.pk)


# =========================================================
# FILE UPLOAD VIEWS
# =========================================================

@login_required
def upload_client_file(request, pk):

    client = get_object_or_404(Client, pk=pk, is_deleted=False)

    if request.method == 'POST':

        ClientFile.objects.create(
            client=client,
            title=request.POST.get('title'),
            file=request.FILES.get('file'),
            uploaded_by=request.user
        )

        messages.success(request, 'File uploaded successfully')

        return redirect('client_detail', pk=client.pk)

    context = {
        'client': client
    }

    return render(request, 'crm/clients/upload_file.html', context)


@login_required
def delete_client_file(request, pk):

    file = get_object_or_404(ClientFile, pk=pk, is_deleted=False)

    file.is_deleted = True
    file.save()

    messages.success(request, 'File deleted successfully')

    return redirect('client_detail', pk=file.client.pk)


# =========================================================
# LEAD NOTES VIEWS
# =========================================================

@login_required
def add_lead_note(request, pk):

    lead = get_object_or_404(Lead, pk=pk, is_deleted=False)

    if request.method == 'POST':

        LeadNote.objects.create(
            lead=lead,
            note=request.POST.get('note'),
            created_by=request.user
        )

        messages.success(request, 'Note added successfully')

        return redirect('lead_detail', pk=lead.pk)

    context = {
        'lead': lead
    }

    return render(request, 'crm/leads/add_note.html', context)


# =========================================================
# COMMUNICATION VIEWS
# =========================================================

@login_required
def add_communication(request, pk):

    lead = get_object_or_404(Lead, pk=pk, is_deleted=False)

    if request.method == 'POST':

        Communication.objects.create(
            lead=lead,
            communication_type=request.POST.get('communication_type'),
            message=request.POST.get('message'),
            created_by=request.user
        )

        messages.success(request, 'Communication added successfully')

        return redirect('lead_detail', pk=lead.pk)

    context = {
        'lead': lead
    }

    return render(request, 'crm/communications/add_communication.html', context)


# =========================================================
# SERVICES VIEWS
# =========================================================

@login_required
def service_list(request):

    search = request.GET.get('search')

    services = Service.objects.filter(
        is_deleted=False
    ).order_by('-created_at')

    if search:
        services = services.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'services': services,
        'search': search,
    }

    return render(request, 'crm/services/service_list.html', context)


@login_required
def add_service(request):

    if request.method == 'POST':

        Service.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description')
        )

        messages.success(request, 'Service added successfully')

        return redirect('service_list')

    return render(request, 'crm/services/add_service.html')


# =========================================================
# ACTIVITY LOGS
# =========================================================

@login_required
def activity_logs(request):

    search = request.GET.get('search')

    logs = ActivityLog.objects.filter(
        is_deleted=False
    ).order_by('-created_at')

    if search:
        logs = logs.filter(
            Q(action__icontains=search) |
            Q(description__icontains=search) |
            Q(user__username__icontains=search)
        )

    paginator = Paginator(logs, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
    }

    return render(request, 'crm/activities/activity_logs.html', context)


# =========================================================
# AJAX TASK STATUS UPDATE
# =========================================================

@login_required
@require_POST
def update_task_status(request, pk):

    task = get_object_or_404(Task, pk=pk, is_deleted=False)

    status = request.POST.get('status')

    if status not in dict(Task.STATUS_CHOICES):
        return JsonResponse({
            'success': False,
            'message': 'Invalid task status'
        }, status=400)

    task.status = status
    task.save()

    return JsonResponse({
        'success': True,
        'message': 'Task status updated'
    })
