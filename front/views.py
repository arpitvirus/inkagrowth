from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import *


# HOME PAGE
def index(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        mobile = request.POST['mobile']

        front_contact = contact.objects.create(
            name=name,
            email=email,
            message=message,
            mobile=mobile
        )

        front_contact.save()

        messages.success(
            request,
            "Your message has been submitted successfully!"
        )
        return redirect('/')

    return render(
        request,
        'index.html'
    )


# DYNAMIC SEO PAGE
def dynamic_page(request, slug):

    page = get_object_or_404(
        SEOPage,
        slug=slug
    )

    # CONTACT FORM
    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        mobile = request.POST['mobile']

        front_contact = contact.objects.create(
            name=name,
            email=email,
            message=message,
            mobile=mobile
        )

        front_contact.save()

        messages.success(
            request,
            "Your message has been submitted successfully!"
        )
        return redirect('/')

    # DYNAMIC IMAGES
    if page.service == "SEO Services":

        image_url = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=700&h=500&fit=crop&auto=format"

    elif page.service == "Website Development":

        image_url = "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=700&h=500&fit=crop&auto=format"

    else:

        image_url = "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=700&h=500&fit=crop&auto=format"

    state = "Uttar Pradesh"

    context = {

        'service': page.service,

        'city': page.city,

        'image_url': image_url,

        'state': state,

        'meta_title': page.meta_title,

        'meta_description': page.meta_description,

        'content': page.content,
    }

    return render(
        request,
        'seo_page.html',
        context
    )