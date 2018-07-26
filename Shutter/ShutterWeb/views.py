from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Topic, Topiccomment, Message, Photo, PhotoComment, UserProfile, News, NewsComment;
from .forms import CommentForm, TopicForm, RegisterForm, photoForm, photocommentForm, messageSendForm, UserInfoForm, NewsCommentForm;
from . import filters
from .forms import CommentForm, TopicForm,photoForm,photocommentForm

# index, index.html will be redirect to album_scenery_new
def index(request):
    return HttpResponseRedirect("album/scenery/new")

def forum(request):
    latest_topic_list=Topic.objects.order_by('-time')
    paginator = Paginator(latest_topic_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        latest_topic = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_topic = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_topic = paginator.page(paginator.num_pages)
    context = {'latest_topic': latest_topic}
    return render(request, 'forum.html', context)

def hot_topic(request):
    latest_topic_list=Topic.objects.order_by('-remarks')
    paginator = Paginator(latest_topic_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        latest_topic = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_topic = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_topic = paginator.page(paginator.num_pages)
    context = {'latest_topic': latest_topic}
    return render(request, 'hot_topic.html', context)

# View topic detail and add comment
def topic(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
        # topic.increase_views()
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")
    if request.method == 'GET':
        form = CommentForm(request.POST)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            clean_data['topic']= topic
            Topiccomment.objects.create(**clean_data)
            topic.increase_remarks()

    context = {
        'topic': topic,
        # 'TopicComments':topic.topiccomment_set.all().order_by('-time'),
        'form': form
    }
    return render(request,'topic.html', context)



def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
                # file is saved
            form.save()
            return redirect('/ShutterWeb/forum')
    else:
        form = TopicForm()
    return render(request, 'add_topic.html', {'form': form})



def news_list(request):
    latest_news_list = News.objects.all()
    # latest_news_list = News.objects.all().order_by("-time")
    paginator = Paginator(latest_news_list, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        latest_news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_news = paginator.page(paginator.num_pages)
    context = {'latest_news': latest_news}
    return render(request, 'news_list.html', context)



def news_content(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise Http404("Topic does not exist")
    if request.method == 'GET':
        NewsCommentForm.author = request.user
        form = NewsCommentForm(request.POST)
    else:
        NewsCommentForm.author = request.user
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            clean_data['topic']= news
            news.author = request.user
            NewsComment.objects.create(**clean_data )
    context = {
        'news':news,
        'NewsComments':news.newscomment_set.all().order_by('-time'),
        'form': form
    }
    return render(request,'news_content.html', context)


class Conversation():
    id = ''
    contact = ''
    content = ''
    time = timezone.now()

def inbox(request):
    context = {}
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserProfile.objects.get(pk=user_id)
        if 'messageSortByDate' in request.POST:
            message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('-time')
        elif 'messageSortByUnread' in request.POST:
            message_list = Message.objects.filter((Q(author=request.user)|Q(receiver=request.user))&Q(readflag='UNREAD'))
            message_list = message_list.order_by('-time')
        elif 'messageSortByFT' in request.POST:
            message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('author')
        # elif 'messageSend' in request.POST:
        elif request.is_ajax():
            print("hi")
            form = messageSendForm(request.POST)
            if form.is_valid():
                try:
                    receiver = UserProfile.objects.get(username=request.POST['receiver'])
                    message = Message()
                    message.author = request.user
                    message.receiver = receiver
                    message.content = request.POST['content']
                    message.save()
                except ObjectDoesNotExist:
                    print('no user admin')
            message_list = Message.objects.filter(Q(author=request.user)|Q(receiver=request.user)).order_by('-time')
        else:
            message_list = Message.objects.filter(Q(author=user)|Q(receiver=user)).order_by('-time')

        conversation = []
        contacts = []
        contact = ''
        for m in message_list:
            if m.author == user:
                contact = str(m.receiver)
            else:
                contact = str(m.author)
            if len(conversation) == 0:
                c = Conversation()
                c.contact = contact
                c.content = m.content
                c.time = m.time
                c.id = m.id
                conversation.append(c)
                contacts.append(contact)
            else:
                for x in conversation:
                    if not contact in contacts:
                        c = Conversation()
                        c.contact = contact
                        c.content = m.content
                        c.time = m.time
                        c.id = m.id
                        conversation.append(c)
                        contacts.append(contact)
                        break
                    else:
                        if x.time < m.time:
                            x.time = m.time
                            x.content = m.content
                            x.id = m.id
                            i = conversation.index(x)
                            conversation.pop(i)
                            conversation.append(x)
                        break

        paginator = Paginator(conversation, 5)  # Show 5 messages per page
        paginator.count = len(list(conversation))

        page = request.GET.get('page', 1)
        print(page)
        try:
            latest_conversation = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            latest_conversation = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            latest_conversation = paginator.page(paginator.num_pages)
        context = {'latest_conversation': latest_conversation}
        # context = {'latest_message': message_list}
    else:
        HttpResponseRedirect("/ShutterWeb/login")
    return render(request, 'inbox.html', context)


@login_required(login_url='/ShutterWeb/login')
def message_detail(request, message_id):
    if 'messageSend' in request.POST:
        form = messageSendForm(request.POST)
        if form.is_valid():
            message = Message.objects.get(pk=message_id)
            newMessage = Message()
            if str(message.receiver) == str(request.user):
                newMessage.receiver = message.author
            else:
                newMessage.receiver = message.receiver
            newMessage.content = form.cleaned_data['content']
            newMessage.author = request.user
            newMessage.save()
    try:
        print(request)
        message = Message.objects.get(pk=message_id)
        author = message.author
        receiver = message.receiver
        if str(message.receiver) == str(request.user):
            message = Message.objects.filter(Q(author=message.author)|Q(receiver=message.author)).order_by('-time')
            context = {'message': message, 'talker': author, 'me': request.user}
        elif str(message.author) == str(request.user):
            message = Message.objects.filter(Q(author=message.receiver) | Q(receiver=message.receiver)).order_by('-time')
            context = {'message': message, 'talker': receiver, 'me': request.user}
        else:
            raise Http404("Not your message!")
    except ObjectDoesNotExist:
        raise Http404("Message does not exist")
    return render(request, 'message_detail.html', context)


# album
def album_scenery_new(request):
    # filter out all scenery photos (category = 1) and order by time
    newest_scenery_photos_list = Photo.objects.filter(category=1).order_by('-time')
    # 9 photos per page
    paginator = Paginator(newest_scenery_photos_list, 9)
    page = request.GET.get('page')
    try:
        newest_scenery_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        newest_scenery_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        newest_scenery_photos = paginator.page(paginator.num_pages)
    photos_list = newest_scenery_photos
    context = {'newest_scenery_photos': newest_scenery_photos, 'photos_list': photos_list}
    #return render(request, 'album_scenery_new.html', context)
    return render(request, 'album.html', context)


def album_scenery_hot(request):
    # filter out all scenery photos (category = 1) and order by time
    hottest_scenery_photos_list = Photo.objects.filter(category=1).order_by('-thumbs_up_number')
    # 9 photos per page
    paginator = Paginator(hottest_scenery_photos_list, 9)
    page = request.GET.get('page')
    try:
        hottest_scenery_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hottest_scenery_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hottest_scenery_photos = paginator.page(paginator.num_pages)
    photos_list = hottest_scenery_photos
    context = {'hottest_scenery_photos': hottest_scenery_photos, 'photos_list': photos_list}
    #return render(request, 'album_scenery_hot.html', context)
    return render(request, 'album.html', context)


def album_people_new(request):
    # filter out all scenery photos (category = 1) and order by time
    newest_people_photos_list = Photo.objects.filter(category=2).order_by('-time')
    # 9 photos per page
    paginator = Paginator(newest_people_photos_list, 9)
    page = request.GET.get('page')
    try:
        newest_people_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        newest_people_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        newest_people_photos = paginator.page(paginator.num_pages)
    photos_list = newest_people_photos
    context = {'newest_people_photos': newest_people_photos, 'photos_list': photos_list}
    #return render(request, 'album_people_new.html', context)
    return render(request, 'album.html', context)


def album_people_hot(request):
    # filter out all scenery photos (category = 1) and order by time
    hottest_people_photos_list = Photo.objects.filter(category=2).order_by('-thumbs_up_number')
    # 9 photos per page
    paginator = Paginator(hottest_people_photos_list, 9)
    page = request.GET.get('page')
    try:
        hottest_people_photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hottest_people_photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hottest_people_photos = paginator.page(paginator.num_pages)
    photos_list = hottest_people_photos
    context = {'hottest_people_photos': hottest_people_photos, 'photos_list': photos_list}
    #return render(request, 'album_people_hot.html', context)
    return render(request, 'album.html', context)

@login_required(login_url='/ShutterWeb/login')
def album_photo(request, photo_id):
    photo=Photo.objects.filter(id=int(photo_id))
    this_photo=photo[0]
    image_path = this_photo.image.url
    photo_name = this_photo.photo_name
    photographer_name = this_photo.photographer_name
    photographer_remark = this_photo.photographer_remark
    category = this_photo.category
    thumbs_up_number = this_photo.thumbs_up_number
    photocomment_set=PhotoComment.objects.filter(photo_id=photo_id)

    # comment form
    if request.method == 'POST':
        form = photocommentForm(request.POST)
        #return HttpResponse('successful!')
        if form.is_valid():
            content=form.cleaned_data['content']
            s=PhotoComment()
            s.content=content
            s.author = request.user
            s.photo_id = photo_id
            s.save()
            #return HttpResponse('successful!')
        else:
            return HttpResponse('fail!')
    else:
        form = photocommentForm()
    context = {
        'photo_id': photo_id,
        'PhotoComment': photocomment_set.all().order_by('-time'),
        'form': form,
        'image_path': image_path,
        'thumbs_up_number': thumbs_up_number,
        'photo_name': photo_name,
        'photographer_name': photographer_name,
        'photographer_remark': photographer_remark,
        'category': category,
    }
    return render(request, 'album_photo.html', context)


# upload photo
@login_required(login_url='/ShutterWeb/login')
def album_upload_image(request):
    if request.method == 'POST':
        form = photoForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            if 'image' in request.FILES:
                image = request.FILES["image"]
                image.name = str(timezone.now()) + '.jpg'
                category = form.cleaned_data['category']
                photo_name = form.cleaned_data['photo_name']
                photographer_remark = form.cleaned_data['photographer_remark']
                s = Photo(image=image, thumbs_up_number=0)
                s.category = category
                s.photo_name = photo_name
                s.photographer_name = request.user
                s.photographer_remark = photographer_remark
                s.save()
                #return HttpResponse('successful!')
                return redirect('/ShutterWeb/album/photo/'+ str(s.id))
            else:
                return HttpResponse('fail 123')
        else:
            image_path = None
            return HttpResponse('fail')
    else:
        form = photoForm()
        return render(request, 'album_upload_image.html', {'form': form})


def delete_photo(request, photo_id):
    this_photo=Photo.objects.get(id = photo_id)
    this_photo.delete()
    return render(request,'album_delete_photo.html',{})

def delete_comment(request, comment_id):
    this_photocomment=PhotoComment.objects.get(id = comment_id)
    photo_id = this_photocomment.photo_id
    this_photocomment.delete()
    context = {'photo_id': photo_id
    }
    return render(request,'album_delete_comment.html', context)



def thumbs_up(request, photo_id):
    photo = Photo.objects.filter(id=photo_id)
    this_photo = photo[0]
    this_photo.increase_thumbs_up()
    return redirect('/ShutterWeb/album/photo/' + str(this_photo.id))

def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password","")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return render(request, "forum.html")
        else:
            context = {'login_err': 'Username or Password is wrong!'}
            return render(request, "login.html", context)
    elif request.method == "GET":
        return render(request, "login.html",{})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/ShutterWeb")


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            my_register(request, username, password)
            return HttpResponseRedirect("/ShutterWeb")
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={'form': form})


def my_register(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        request.session['user_id'] = user.id


def Userinfo(request):
    return  render(request, 'user_profile.html',{})

def editprofile(request):
    user_info_form = UserInfoForm(request.POST, instance=request.user)
    if user_info_form.is_valid():
        user_info_form.save()
        return HttpResponseRedirect("/ShutterWeb/info")
    else:
        user_info_form = UserInfoForm()
    return render(request, 'edit_profile.html', context={'user_info_form': user_info_form})
