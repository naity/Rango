from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.contrib.auth.models import User
from rango.category_search import get_category_list

# Create your views here.
def index(request):
    #request.session.set_test_cookie()

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by("-views")[0:5]
    context = {"categories": category_list, "pages": page_list}

    visits = request.session.get("visits")

    if not visits:
        visits = 1

    reset_last_visit = False

    last_visit = request.session.get("last_visit")

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[0:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit = True
    
    else:
        reset_last_visit= True

    if reset_last_visit:
        request.session["last_visit"] = str(datetime.now())
        request.session["visits"] = visits

    context["visits"] = visits
    
    return render(request, "rango/index.html", context)

def category(request, category_name_slug):
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context["category_name"] = category.name

        pages = Page.objects.filter(category=category).order_by("-views")

        context["pages"] = pages
        context["category"] = category

    except Category.DoesNotExist:
        pass

    result_list = []
    query = None

    if request.method == "POST":
        query = request.POST["query"].strip()
        if query:
            result_list = run_query(query)
    
    context["result_list"] = result_list
    if not query:
        query = category.name
    context["query"] = query

    return render(request, "rango/category.html", context)

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse("rango:index"))

    else:
        form = CategoryForm()

    return render(request, "rango/add_category.html", {"form":form})

@login_required
def add_page(request, category_name_slug):
    context = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        context["category"] = category
    except Category.DoesNotExist:
        category = False

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse("rango:category", args=(category_name_slug,)))

    else:
        if category:
            form = PageForm(initial={"category": category})
            context["form"] = form

    return render(request, "rango/add_page.html", context)

def track_url(request):
    context = {}
    page = None

    if request.method == "GET":
        if  "page_id" in request.GET:
            page_id = request.GET["page_id"]
            try:
                page = Page.objects.get(id=page_id)
            except Page.DoesNotExist:
                page = None

            if page:
                page.views += 1
                page.save()

    context["page"] = page
    return render(request, 'rango/page_views_display.html', context)

@login_required
def register_profile(request):
    profile_registered = False

    if request.method == "POST":
        profile_form = UserProfileForm(data=request.POST)

        if profile_form.is_valid():
            if request.user.is_authenticated():
                user = request.user
                if user.is_active:
                    profile = profile_form.save(commit=False)
                    profile.user = user

                    # handle profile picture
                    if "picture" in request.FILES:
                        profile.picture = request.FILES["picture"]

                    profile_registered = True
                    profile.save()

    else:
        profile_form = UserProfileForm()

    context = {"profile_form": profile_form, "profile_registered": profile_registered}

    return render(request, "rango/profile_registration.html", context)

@login_required
def profile(request):
    context = {}

    if request.method == "GET":
        if "user_id" in request.GET:
            user_id = request.GET["user_id"]
            user = get_object_or_404(User, pk=user_id)
            user_profile = UserProfile.objects.get(pk=user)

            if user.id != request.user.id:
                context["own"] = False
            else:
                context["own"] = True

            context["user_profile"] = user_profile

            return render(request, "rango/profile.html", context)
       
        else:
            return HttpResponseRedirect(reverse("rango:index", ))

    elif request.method == "POST":
        user = request.user
        user_profile = UserProfile.objects.get(pk=user)

        if request.POST["username"]:
            user.username = request.POST["username"]

        if request.POST["email"]:
            user.email = request.POST["email"]

        if request.POST["first_name"]:
            user.first_name = request.POST["first_name"]

        if request.POST["last_name"]:
            user.last_name = request.POST["last_name"]

        if request.POST["website"]:
            user_profile.website = request.POST["website"]

        if "picture" in request.FILES:
            user_profile.picture = request.FILES["picture"]
        
        user.save()
        user_profile.save()

        context = {"user_profile": user_profile, "own": True}
        return render(request, "rango/profile.html", context)

@login_required
def users(request):
    context = {"users": None}
    if request.user.is_authenticated():
        user = request.user
        if user.is_active:
            users = User.objects.all()
            context["users"] = users

    return render(request, "rango/users.html", context)

@login_required
def like_category(request):
    if request.method == "GET":
        if  "category_id" in request.GET:
            category_id = request.GET["category_id"]
            try:
                category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                category = None

            if category:
                category.likes += 1
                category.save()
                return HttpResponse(category.likes)

    return HttpResponse(0)

def suggest_category(request):
    context = {}
    categories = []
    if request.method == "GET":
        if "suggestion" in request.GET:
            starts_with = request.GET["suggestion"]

            categories = get_category_list(8, starts_with)

    context["cats"] = categories
    return render(request, 'rango/cats.html', context)

@login_required
def search_add_page(request):
    context = {}
    pages = None

    if request.method == "GET":
        if  "category_id" in request.GET:
            category_id = request.GET["category_id"]
            try:
                category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                category = None

        if category:
            if "page_link" and "page_title" in request.GET:
                page_link = request.GET["page_link"]
                page_title = request.GET["page_title"]
                new_page = Page.objects.get_or_create(category=category, title=page_title, url=page_link, views=0)[0]

            pages = Page.objects.filter(category=category).order_by("-views")

    context["pages"] = pages
    return render(request, "rango/search_add_page.html", context)

def about(request):
    visits = request.session.get("visits")
    if not visits:
        visits = 1
    return render(request, "rango/about.html", {"visits": visits})

# def register(request):
#     #if request.session.test_cookie_worked():
#         #print("TEST COOKIE WORKED!")
#         #request.session.delete_test_cookie()

#     registered = False

#     if request.method == "POST":
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             # hash password
#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             # handle profile picture
#             if "picture" in request.FILES:
#                 profile.picture = request.FILES["picture"]

#             profile.save()

#             registered = True

#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     context = {"user_form": user_form, "profile_form": profile_form, "registered": registered}

#     return render(request, "rango/register.html", context)

# def user_login(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("rango:index"))
#             else:
#                 return HttpResponse("Your Rango account is disabled.")

#         else:
#             return HttpResponse("Invalid username or password.")

#     else:
#         return render(request, "rango/login.html", {})

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("rango:index"))

