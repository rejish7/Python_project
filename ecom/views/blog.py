
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from ecom.models import BlogPost, Comment
from ecom.forms import CommentForm
from django.contrib import messages

def blog_list(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(blog_posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/blog/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    related_posts = BlogPost.objects.filter(category=blog_post.category).exclude(id=post_id)[:4]
    previous_post = BlogPost.objects.filter(created_at__lt=blog_post.created_at).order_by('-created_at').first()
    next_post = BlogPost.objects.filter(created_at__gt=blog_post.created_at).order_by('created_at').first()
    
    context = {
        'blog_post': blog_post,
        'related_posts': related_posts,
        'previous_post': previous_post,
        'next_post': next_post,
    }
    return render(request, 'pages/blog/blog.html', context)

def add_comment(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog_post
            comment.author = request.user if request.user.is_authenticated else None
            comment.save()
            messages.success(request, 'Your comment has been added successfully.')
            return redirect('blog_detail', post_id=post_id)
    return redirect('blog_detail', post_id=post_id)
