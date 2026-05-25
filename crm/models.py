from django.db import models
from django.contrib.auth.models import User
import uuid


# =========================================================
# BASE MODEL
# =========================================================

class BaseModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# =========================================================
# USER PROFILE
# =========================================================

class UserProfile(BaseModel):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


# =========================================================
# SERVICE MODEL
# =========================================================

class Service(BaseModel):

    name = models.CharField(max_length=150)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# =========================================================
# CLIENT MODEL
# =========================================================

class Client(BaseModel):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=150)

    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)

    website = models.URLField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    monthly_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    renewal_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients_created'
    )

    def __str__(self):
        return self.name


# =========================================================
# LEAD MODEL
# =========================================================

class Lead(BaseModel):

    LEAD_SOURCE_CHOICES = (
        ('facebook', 'Facebook'),
        ('google', 'Google'),
        ('instagram', 'Instagram'),
        ('website', 'Website'),
        ('whatsapp', 'WhatsApp'),
        ('reference', 'Reference'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('follow_up', 'Follow Up'),
        ('converted', 'Converted'),
        ('not_interested', 'Not Interested'),
    )

    PIPELINE_CHOICES = (
        ('new_lead', 'New Lead'),
        ('discussion', 'Discussion'),
        ('proposal_sent', 'Proposal Sent'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    )

    name = models.CharField(max_length=150)

    company_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)

    website = models.URLField(
        blank=True,
        null=True
    )

    lead_source = models.CharField(
        max_length=50,
        choices=LEAD_SOURCE_CHOICES,
        default='website'
    )

    interested_service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new'
    )

    pipeline_stage = models.CharField(
        max_length=50,
        choices=PIPELINE_CHOICES,
        default='new_lead'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_leads'
    )

    def __str__(self):
        return self.name


# =========================================================
# FOLLOW UP MODEL
# =========================================================

class FollowUp(BaseModel):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='followups'
    )

    followup_date = models.DateTimeField()

    note = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.lead.name} - {self.followup_date}"


# =========================================================
# TASK MODEL
# =========================================================

class Task(BaseModel):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    title = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )

    related_client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    due_date = models.DateField(
        blank=True,
        null=True
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks'
    )

    def __str__(self):
        return self.title


# =========================================================
# PAYMENT MODEL
# =========================================================

class Payment(BaseModel):

    PAYMENT_STATUS = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField()

    next_payment_date = models.DateField(
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.client.name} - {self.amount}"


# =========================================================
# LEAD NOTES MODEL
# =========================================================

class LeadNote(BaseModel):

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='lead_notes'
    )

    note = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.lead.name


# =========================================================
# CLIENT FILES MODEL
# =========================================================

class ClientFile(BaseModel):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='files'
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to='client_files/'
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.title


# =========================================================
# COMMUNICATION MODEL
# =========================================================

class Communication(BaseModel):

    TYPE_CHOICES = (
        ('call', 'Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='communications'
    )

    communication_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    message = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.communication_type


# =========================================================
# ACTIVITY LOG MODEL
# =========================================================

class ActivityLog(BaseModel):

    ACTION_CHOICES = (
        ('lead_created', 'Lead Created'),
        ('lead_updated', 'Lead Updated'),
        ('client_created', 'Client Created'),
        ('task_created', 'Task Created'),
        ('followup_added', 'Follow Up Added'),
        ('payment_added', 'Payment Added'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.action}"