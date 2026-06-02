from django import forms
from django.utils import timezone
from django.utils.text import slugify

from .models import Category, FAQ, InternalLink, MediaFile, OutboundLink, Post, Tag


class PostForm(forms.ModelForm):
    publish_action = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = (
            "title",
            "slug",
            "focus_keyphrase",
            "meta_title",
            "meta_description",
            "excerpt",
            "content",
            "featured_image",
            "featured_image_alt",
            "category",
            "tags",
            "service",
            "city",
            "state",
            "status",
            "published_at",
            "scheduled_at",
            "canonical_url",
            "robots_index",
            "robots_follow",
            "og_title",
            "og_description",
            "og_image",
            "twitter_title",
            "twitter_description",
            "twitter_image",
            "schema_type",
            "internal_links",
            "outbound_links",
        )
        widgets = {
            "content": forms.Textarea(attrs={"class": "rich-editor", "rows": 18}),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "meta_description": forms.Textarea(attrs={"rows": 3, "maxlength": 160}),
            "og_description": forms.Textarea(attrs={"rows": 2}),
            "twitter_description": forms.Textarea(attrs={"rows": 2}),
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "tags": forms.CheckboxSelectMultiple,
            "internal_links": forms.CheckboxSelectMultiple,
            "outbound_links": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} dashboard-input".strip()
        self.fields["internal_links"].queryset = InternalLink.objects.all()
        self.fields["outbound_links"].queryset = OutboundLink.objects.all()

    def clean_slug(self):
        slug = slugify(self.cleaned_data["slug"] or self.cleaned_data.get("title", ""))
        if not slug:
            raise forms.ValidationError("Slug is required.")
        queryset = Post.objects.filter(slug=slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("This slug already exists.")
        return slug

    def clean(self):
        cleaned = super().clean()
        action = self.data.get("action") or cleaned.get("publish_action")
        status = cleaned.get("status")
        if action == "publish":
            cleaned["status"] = Post.STATUS_PUBLISHED
            self._validate_publish_ready(cleaned)
        elif action == "schedule":
            cleaned["status"] = Post.STATUS_SCHEDULED
            if not cleaned.get("scheduled_at"):
                self.add_error("scheduled_at", "Scheduled posts need a scheduled date.")
            self._validate_publish_ready(cleaned)
        elif action == "draft":
            cleaned["status"] = Post.STATUS_DRAFT
        elif status == Post.STATUS_PUBLISHED:
            self._validate_publish_ready(cleaned)
        return cleaned

    def _validate_publish_ready(self, cleaned):
        required_fields = [
            "title",
            "slug",
            "focus_keyphrase",
            "meta_title",
            "meta_description",
            "content",
            "featured_image",
            "featured_image_alt",
            "canonical_url",
            "category",
        ]
        for field in required_fields:
            if not cleaned.get(field):
                self.add_error(field, "Required before publishing.")
        if len(cleaned.get("meta_title") or "") not in range(50, 61):
            self.add_error("meta_title", "SEO title must be 50-60 characters.")
        if len(cleaned.get("meta_description") or "") not in range(140, 161):
            self.add_error("meta_description", "Meta description must be 140-160 characters.")
        if len(self.data.getlist("internal_links")) < 4:
            self.add_error("internal_links", "Select at least 4 internal links.")
        if len(self.data.getlist("outbound_links")) < 4:
            self.add_error("outbound_links", "Select at least 4 outbound links.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.status == Post.STATUS_PUBLISHED and not instance.published_at:
            instance.published_at = timezone.now()
        if instance.status == Post.STATUS_SCHEDULED:
            instance.published_at = instance.scheduled_at
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "description", "is_indexable")


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", "slug", "is_indexable")


class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ("title", "file", "alt_text")


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ("question", "answer", "sort_order")
