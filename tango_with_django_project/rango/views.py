from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
    response = render(request, "rango/index.html", context)
    
    return response

def category(request, category_name_slug):
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context["category_name"] = category.name

        pages = Page.objects.filter(category=category)

        context["pages"] = pages
        context["category"] = category

    except Category.DoesNotExist:
        pass

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

def register(request):
    #if request.session.test_cookie_worked():
        #print("TEST COOKIE WORKED!")
        #request.session.delete_test_cookie()

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # hash password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # handle profile picture
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            registered = True

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {"user_form": user_form, "profile_form": profile_form, "registered": registered}

    return render(request, "rango/register.html", context)

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("rango:index"))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            return HttpResponse("Invalid username or password.")

    else:
        return render(request, "rango/login.html", {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("rango:index"))

def about(request):
    visits = request.session.get("visits")
    if not visits:
        visits = 1
    return render(request, "rango/about.html", {"visits": visits})