from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm

def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('blog:contact_us')
    else:
        form = ContactMessageForm()
    return render(request, 'blog/contact_us.html', {'form': form})


def about(request):
    return render(request, 'blog/about.html')


def help(request):
    return render(request, 'blog/help.html')