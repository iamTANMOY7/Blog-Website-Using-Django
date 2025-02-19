from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
from .models import PasswordResetToken
from django.core.mail import send_mail
from .models import Comment,Post


# Create your views here.
def index(request):
    # If user is authenticated, show their own active posts
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(user_id=request.user.id, status='active').order_by("id").reverse()
    else:
        user_posts = []
    
    # Calculate comment counts and last post dates per category
    category_comment_counts = {}
    category_last_post_dates = {}
    categories = ['Programming', 'Travel', 'Education', 'Technology', 'ArtificialIntelligence']
    
    for category in categories:
        category_comment_counts[category] = Comment.objects.filter(
            post__category=category, 
            post__status='active'
        ).count()
        
        # Get the last post date for each category
        last_post = Post.objects.filter(
            category=category, 
            status='active'
        ).order_by('-id').first()
        
        category_last_post_dates[category] = last_post.time if last_post else 'No recent posts'
    
    return render(request,"index.html",{
        'posts': user_posts,
        'top_posts': Post.objects.filter(status='active').order_by("-likes"),
        'recent_posts': Post.objects.filter(status='active').order_by("-id"),
        'user': request.user,
        'media_url': settings.MEDIA_URL,
        'category_comment_counts': category_comment_counts,
        'category_last_post_dates': category_last_post_dates
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already Exists")
                return redirect('signup')
            else:
                # Create user with the provided details
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('signin')
        else:
            messages.info(request, "Password should match")
            return redirect('signup')
            
    return render(request, "signup.html")

def signin(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == 'POST':
        # Check if it's a Google sign-in request
        if 'google_signin' in request.POST:
            # Redirect to Google sign-in
            return redirect('/accounts/google/login/')

        # Traditional username/password login
        elif 'traditional_signin' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            
            if not username or not password:
                messages.info(request, 'Username and Password are required')
                return redirect("signin")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("index")
            else:
                messages.info(request, 'Username or Password is incorrect')
                return redirect("signin")
    return render(request, "signin.html")

def logout(request):
    auth.logout(request)
    return redirect('index')

def blog(request):
    # Filter posts that are active and optionally filter by the current user if logged in
    if request.user.is_authenticated:
        posts = Post.objects.filter(status='active', user_id=request.user.id).order_by("id").reverse()
    else:
        posts = Post.objects.filter(status='active').order_by("id").reverse()
    
    return render(request,"blog.html",{
        'posts': posts,
        'top_posts': Post.objects.filter(status='active').order_by("-likes"),
        'recent_posts': Post.objects.filter(status='active').order_by("-id"),
        'user': request.user,
        'media_url': settings.MEDIA_URL
    })
@login_required(login_url='signin')    
def create(request):
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES['image']
            Post(postname=postname,content=content,category=category,image=image,user=request.user).save()
        except:
            print("Error")
        return redirect('index')
    else:
        return render(request,"create.html")
    
@login_required
def profile(request):
    active_posts = Post.objects.filter(user=request.user, status='active')
    inactive_posts = Post.objects.filter(user=request.user, status='inactive')
    return render(request, 'profile.html', {
        'user': request.user,
        'active_posts': active_posts,
        'inactive_posts': inactive_posts,
        'media_url': settings.MEDIA_URL,
    })

@login_required
def toggle_post_status(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        # Toggle post status
        if post.status == 'active':
            post.status = 'inactive'
        else:
            post.status = 'active'
        post.save()
    return redirect('profile')

@login_required
def profileedit(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
    
        user = request.user
        user.first_name = firstname
        user.email = email
        user.last_name = lastname
        user.save()
        return redirect('profile')
    return render(request, "profileedit.html", {
        'user': request.user,
    })
    
@login_required(login_url='signin')
def increaselikes(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.likes += 1
        post.save()
    # Redirect to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def post(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Restrict access to inactive posts
    if post.status != 'active':
        messages.error(request, " ")
        return redirect('index')
    
    return render(request, "post-details.html", {
        "user": request.user,
        'post': post,
        'recent_posts': Post.objects.filter(status='active').order_by("-id"),
        'media_url': settings.MEDIA_URL,
        'comments': Comment.objects.filter(post_id=post.id),
        'total_comments': Comment.objects.filter(post_id=post.id).count()
    })

def savecomment(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect("post",id=id)
    
def deletecomment(request,id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user == request.user:
        postid = comment.post.id
        comment.delete()
        return redirect('post', id=postid)
    else: 
        return HttpResponseForbidden("You are not allowed to delete this comment.")
@login_required(login_url='signin')    
def editpost(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Restrict editing inactive posts
    if post.status != 'active':
        messages.error(request, "")
        return redirect('index')
    
    # Check if the logged-in user is the owner of the post
    if post.user != request.user:
        return redirect('index')
    
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            
            post.postname = postname
            post.content = content
            post.category = category
            post.save()
        except Exception as e:
            print("Error:", e)
        return redirect('profile')
    
    return render(request, "postedit.html", {'post': post})

@login_required(login_url='signin')    
def deletepost(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Restrict deletion of inactive posts if necessary
    if post.status != 'active':
        messages.error(request, " ")
        return redirect('index')
    
    if post.user == request.user:
        post.delete()
        return redirect('profile')
    else:
        return redirect('index')

def contact_us(request):
    context={}
    if request.method == 'POST':
        name=request.POST.get('name')    
        email=request.POST.get('email')  
        subject=request.POST.get('subject')  
        message=request.POST.get('message')  

        obj = Contact(name=name,email=email,subject=subject,message=message)
        obj.save()
        context['message']=f"Dear {name}, Thanks for your time!"

    return render(request,"contact.html",context)

def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Create a new reset token
            reset_token = PasswordResetToken.create_token_for_user(user)
            
            # Construct reset link
            reset_link = f"{request.scheme}://{request.get_host()}/resetpassword/{reset_token.token}"
            
            # Send email
            send_mail(
                'Password Reset Request',
                f'Hello {user.username},\n\nYou requested a password reset. Click the link below to reset your password. This link will expire in 24 hours:\n\n{reset_link}\n\nIf you did not request this, please ignore this email.\n\nThank you,\nYour Website Team',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'A password reset link has been sent to your email.')
            return redirect('signin')
        
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
        
    return render(request, "forget.html")

def resetpassword(request, token):
    try:
        # Find the token, ensuring it's not used
        reset_token = PasswordResetToken.objects.get(
            token=token, 
            is_used=False
        )
        
        # Check token expiration
        if reset_token.is_expired():
            reset_token.delete()
            messages.error(request, 'Password reset link has expired.')
            return redirect('forget')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate passwords
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, "resetpassword.html", {'token': token})
            
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, "resetpassword.html", {'token': token})
            
            # Update user password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('signin')
        
        return render(request, "reset.html", {'token': token})
    
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid or expired password reset token.')
        return redirect('forget')
    
def category(request, category_name):
    # Filter posts by the specified category and ensure they are active
    category_posts = Post.objects.filter(category__iexact=category_name, status='active').order_by('-id')
    
    return render(request, "category.html", {
        'category': category_name,
        'posts': category_posts,
        'top_posts': Post.objects.filter(status='active').order_by("-likes"),
        'recent_posts': Post.objects.filter(status='active').order_by("-id"),
        'media_url': settings.MEDIA_URL
    })