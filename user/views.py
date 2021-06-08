from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from .forms import UserCreateForm, ReplyForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib import messages #import messages
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout

from verify_email.email_handler import send_verification_email
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

from django.urls import reverse
from .models import Profile, PostToUser, CommentToPost, Follow, Activity, Notification, UserSeenNotifycation
from user.models import *
# add date time and time ago - humaize
import datetime
import humanize

#add os to display image
import os
from django.views.decorators.csrf import csrf_exempt
# add random
import operator
import random
from django.core.mail import send_mail

# UserModel = get_user_model()

# Create your views here.


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(username=user_name, password=pass_word)
        print('None', user)
        if user is not None and user.is_active:
            print("User Login:  Username:" + user_name + '    Password:' + pass_word)
            print(request.POST)
            login(request, user)
            return redirect('/')
        else:
            return redirect('/')
    else:
        return render(request, '404.html')

@csrf_exempt
def send_login(request):
    if request.method == 'POST':
        if request.is_ajax():
            print('nguyen minh dan')
            type = request.POST.get('type')
            password = request.POST.get('password')
            username = request.POST.get('username')
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            print('None', user)
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse({'mess':'oke'})
            else:
                return JsonResponse({'mess':'error'})


@csrf_exempt
@login_required
def change_password(request):
    if request.method =='POST':
        if request.is_ajax():
            print('nguyen minh dan')
            type = request.POST.get('type')
            password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')

            if type == 'change-password':
                username = request.user.username
                print(password)
                print(new_password)
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({'mess': 'ok', 'type':'change-password'})
                else:
                    print('here')
                    return JsonResponse({'mess': 'error', 'type':'change-password'})
    return JsonResponse({'mess': 'error', 'type':'change-password'})

@csrf_exempt
def connect_social(request):
    if request.method =='POST':
        if request.is_ajax():
            facebook = request.POST.get('facebook')
            linked = request.POST.get('linked')
            google = request.POST.get('google')
            instagram = request.POST.get('instagram')
            twitter = request.POST.get('twitter')
            print(facebook)
            
            profile = Profile.objects.filter(user= request.user)[0]
            profile.facebook_link = facebook
            profile.linkedln_link = linked
            profile.google_link = google
            profile.instagram = instagram
            profile.twitter_link = twitter
            profile.save()
            return JsonResponse({'mess':'ok'})
    return JsonResponse({'mess':'error'})
    
        





@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('/')

#complete register page
@csrf_protect
def user_register(request):
    if request.method=="POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your  account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            # context = {
            #     'user' : user,
            #     'domain' : current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),}

            # html_message = render_to_string('acc_active_email.html', context = context)
            # send_mail(
            #     subject='Activate your  account',
            #     html_message= html_message,
            #     recipient_list=[to_email],
            #     message = 'Email from Imovie Team',
            #      html_message= html_message,
            #     from_email=[to_email],
            # )
            return render(request, template_name="confirm_email.html")
    else:
        form = UserCreateForm()
    return render(request, template_name="register.html", context={"register_form": form})


def activate(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        user.backend = 'django.contrib.auth.backends.ModelBackend' 
        # print('In ra o day nhe ')
        user.is_active = True
        user.save()
        # print(user.is_active)
        # print(user)
        return render(request,template_name="active_sucess.html" )
        
    else:
        return render(request,template_name="active_sucess.html")


#complete Facebook
def facebook(request):
    print('Process here ...')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
    else:
        # Create new account with default password
        user = User.objects.create_user(username=username, password='facebook')
        user.save()
        user = authenticate(username=username, password='facebook')
        login(request, user)
    return HttpResponse()

@csrf_exempt
@login_required
def upload_image(request):
    
    if request.method == "POST":
        if request.is_ajax():
            print('oke')
            profile_picture = request.FILES.get('avatar-image')
            print('image',profile_picture)

            return JsonResponse({'profile_picture': profile_picture})
    return JsonResponse({'profile_picture': 'profile_picture'})



@csrf_exempt
@login_required
def user_detail_edit_profile(request):
    response_data = {}
    if request.method == "POST":
        print('1')
        if request.is_ajax():
            print('2')
            type = request.POST.get('type')
            if type == 'general':
                print('3')
                location = request.POST.get('country')
                gender = request.POST.get('gender')
                print('gender', gender)
                birthday =  request.POST.get('birthday')
                bio = request.POST.get('bio')
                profile_picture = request.FILES.get('profile_picture')
                full_name = request.POST.get('full_name')
                if len(Profile.objects.filter(user=request.user).order_by('-id'))==1:
                    print('here')
                    user_profile = Profile.objects.filter(user=request.user).order_by('-id')[0]
                    if len(location)>1:
                        user_profile.location = location
                    if gender is not None:
                        print('here',gender)
                        user_profile.gender = gender
                    if len(birthday) >=1:
                        user_profile.birthday = birthday
                    if len(bio) >=1:
                        user_profile.bio = bio
                    if profile_picture is None:
                        user_profile.profile_picture = request.user.profile.profile_picture
                    if profile_picture is not None:
                        user_profile.profile_picture = profile_picture
                    if len(full_name) >1:
                        user_profile.full_name = full_name
                    user_profile.save()

                # return data
                response_data['location'] = location
                response_data['gender'] = gender
                response_data['birthday'] = birthday
                response_data['full_name'] = full_name
                response_data['bio'] = bio
                response_data['profile_picture'] = user_profile.profile_picture.url
                return JsonResponse({'mess':'success', 'data': response_data})

                # return JsonResponse(response_data)
            
            
            return JsonResponse({'mess': 'error'})

                    
    if request.user.profile.birthday is not None:
        birthday = str(request.user.profile.birthday.year)+'-' +'{:02d}'.format(request.user.profile.birthday.month) +'-' + '{:02d}'.format(request.user.profile.birthday.day)
        return render(request, 'edit_detail_profile.html', {'user': request.user, 'birthday':birthday})
    return render(request, 'edit_detail_profile.html', {'user': request.user, 'birthday':''})
    

def check_follow(user1, user2):
    if len(Follow.objects.filter(user1 = user1, user2 = user2)) >0:
        return True
    return False

@login_required
def comunity(request):
    # show activity for user follow 
    activitys = []
    for acti in Activity.objects.all():
        if check_follow(request.user, acti.user):
            if acti.type == 3:
                if acti.review.review is not None:
                    activitys.append(acti)
            else:
                activitys.append(acti)

    # add activity by request.user
    for acti in Activity.objects.filter(user= request.user):
        if acti.type == 3:
                if acti.review.review is not None:
                    activitys.append(acti)
        else:
            activitys.append(acti)
    #done
    activitys = sorted(activitys, key = lambda x : x.date_posted)
    activitys.reverse()
    # add notification to show user...
    data = {}
    notifications = Notification.objects.filter(user = request.user).order_by('-date_posted')[:10]
    count_noti = UserSeenNotifycation.objects.filter(user = request.user, is_seen = False).count()
    data['activitys'] = activitys
    data['notifications'] = notifications
    data['count_noti'] = count_noti
    # recommend friend here 
    recommend_follow = []
    recommend2 = []
    for u1 in User.objects.all():
        if check_follow(request.user, u1) is False:
            if check_follow(u1, request.user) is True:
                recommend_follow.append(u1)
    all_users = User.objects.all()
    all_users = [all_users[i] for i in random.sample(range(len(all_users)), 8)]
    for u3 in all_users:
        if u3 not in recommend_follow:
            if check_follow(request.user, u3) is False and u3.id != request.user.id:
                recommend2.append(u3)
    
    data['recommend_random'] = recommend2[:6]
    data['recommend_follow'] = recommend_follow[:5]
    # print(recommend2)
    # print(recommend_follow)

    
    return render(request, 'comunity.html',  data)

# get profile by id ...


@csrf_exempt
def follow_now(request):
    if request.method == 'POST':
        if request.is_ajax():
            user2_Id =  request.POST.get('userID')
            user1 = request.user
            user2 = User.objects.get(id = user2_Id)
            record = Follow.objects.filter(user1 = user1, user2 = user2)
            if len(record) >=1:
                record[0].delete()
                print('unfollow')
                return JsonResponse({'mess':'oke'})
            else:
                new_record = Follow(user1 = user1, user2 = user2)
                new_record.save()
                print('follow')
                return JsonResponse({'mess':'oke'})
        
    return JsonResponse({'mess':'error'})
        


            



@csrf_exempt
@login_required
def detail_user(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    post_comments = PostToUser.objects.filter(to_user=profile.user).order_by('-date_posted')
    notifications = Notification.objects.filter(user = request.user).order_by('-date_posted')[:5]
    count_noti = UserSeenNotifycation.objects.filter(user = request.user, is_seen = False).count()
    print('vao day 1')
    # check request user , profile's user
    follow_flag = -1
    if request.user.profile.id == profile_id:
        profile_flag = 1
    else:
        profile_flag = 0
        # check follow , user follow profile's user
        record = Follow.objects.filter(user1=request.user, user2 = profile.user)
        print(record)
        if len(record) >= 1:
            follow_flag = 1
        else:
            follow_flag = 0
    # count followers , following 
    following = Follow.objects.filter(user1 = profile.user).count()
    followers = Follow.objects.filter(user2 = profile.user).count()
    list_followers = Follow.objects.filter(user2 = profile.user)
    print(list_followers)
    if request.method == 'POST':
        print('vao day 2')

        if request.is_ajax():
            print('vao day 3')

            type = request.POST.get('type')
            print('o day type la gi ', type)
            if type == 'comment':
                print('vao day 4')
                content = request.POST.get('content')
                date_posted = datetime.datetime.now()
                print(content)

                new_post = PostToUser(content = content, author = request.user, to_user = profile.user, date_posted = date_posted)
                new_post.save()


                data = {
                    'send_user': request.user.username,
                    'to_user': profile.user.username,
                    'content': content,
                    'date_posted': 'just now',
                    'send_user_url': request.user.profile.get_absolute_url(),
                    'send_user_avatar': request.user.profile.profile_picture.url,
                    'post_id': new_post.id,
                }

                return JsonResponse(data)
            else:
                if type == 'reply':
                    print('vao day 5')
                    print('ban da vao day : reply .....')
                    content = request.POST.get('content')
                    date_posted = datetime.datetime.now()
                    postID = request.POST.get('postID')
                    post = get_object_or_404(PostToUser, pk=int(postID))

                    print(content)
                    print(postID)

                    reply =  CommentToPost(post = post, author = request.user, date_posted = date_posted, content = content)
                    reply.save()


                    data = {
                        'send_user': request.user.username,
                        'to_post': postID,
                        'content': content,
                        'date_posted': 'just now',
                        'send_user_url': request.user.profile.get_absolute_url(),
                        # bug ig you not have image avatar => bug here to ajax
                        'send_user_avatar': request.user.profile.profile_picture.url,
                        'count_comments': post.total_comments(),
                    }

                    return JsonResponse(data)
    return render(request, 'user_profile.html', {'notifications':notifications,'list_followers':list_followers ,'count_noti':count_noti,'user':request.user, 'profile':profile, 'posts': post_comments, 'profile_flag' : profile_flag, 'follow_flag': follow_flag, 'followers': followers, 'following': following})

#profile request user
def user_detail(request, format=None):
    profile_id = request.user.profile.id
    return  detail_user(request, profile_id)


@csrf_exempt
@login_required
def like_post(request):
    if request.method == 'POST':
        print('1')
        if request.is_ajax():
            print('2')
            postID = request.POST.get('postID')
            type = request.POST.get('type')
            if type == 'like':
                post = get_object_or_404(PostToUser, pk=int(postID))
                request_user = request.user

                if request_user in post.likes.all():
                    #dislike
                    post.likes.remove(request_user)
                    count_likes = post.likes.count()
                    return JsonResponse({'count_likes': count_likes, 'type':'dislike'})
                else:
                    post.likes.add(request.user)
                    # add notification
                    if request.user.id != post.author.id:
                        Notification.objects.create(user=post.author, user2= request.user, post = post, type = 7)
                    count_likes = post.likes.count()
                    return JsonResponse({'count_likes': count_likes, 'type':'like'})
    return JsonResponse({'count_likes': 0, 'type': -1})

@csrf_exempt
@login_required
def report_post(request):
    if request.method == 'POST':
        if request.is_ajax():
            postID = request.POST.get('postID')
            print(postID)
            type = request.POST.get('type')
            if type == 'report':
                post = get_object_or_404(PostToUser, pk=int(postID))
                request_user = request.user
                if request_user in post.reports.all():
                    #dislike
                    post.reports.remove(request_user)
                    return JsonResponse({'type':'unreport'})
                else:
                    post.reports.add(request.user)
                    return JsonResponse({ 'type':'report'})

    return JsonResponse({'type': -1})

@csrf_exempt
@login_required
def seen_noti(request):
    if request.method == 'POST':
        if request.is_ajax():
            all_noti = UserSeenNotifycation.objects.filter(user = request.user)
            for noti in all_noti:
                noti.is_seen = True
                noti.save()            

            return JsonResponse({'mess': 'sucess'})
    return JsonResponse({'mess': 'error'})



@csrf_exempt
@login_required
def follow(request):
    if request.method == 'POST':
        if request.is_ajax():
            user2_Id =  request.POST.get('user2')
            user1 = request.user
            user2 = User.objects.get(id = user2_Id)
            record = Follow.objects.filter(user1 = user1, user2 = user2)
            if len(record) >=1:
                record[0].delete()
                return JsonResponse({'mess': 'unfollow'})
            else:
                new_record = Follow(user1 = user1, user2 = user2)
                new_record.save()
                return JsonResponse({'mess': 'follow'})
    return JsonResponse({'mess':'error'})


@csrf_exempt
@login_required
def get_data_chart1(request):
    if request.is_ajax():
        type = request.GET.get('type')
        if type == 'chart1':
            register_list = []
            register_list.append(User.objects.filter(date_joined__month = 1).count())
            register_list.append(User.objects.filter(date_joined__month = 2).count())
            register_list.append(User.objects.filter(date_joined__month = 3).count())
            register_list.append(User.objects.filter(date_joined__month = 4).count())
            register_list.append(User.objects.filter(date_joined__month = 5).count())
            register_list.append(User.objects.filter(date_joined__month = 6).count())
            register_list.append(User.objects.filter(date_joined__month = 7).count())
            register_list.append(User.objects.filter(date_joined__month = 8).count())
            register_list.append(User.objects.filter(date_joined__month = 9).count())
            register_list.append(User.objects.filter(date_joined__month = 10).count())
            register_list.append(User.objects.filter(date_joined__month = 11).count())
            register_list.append(User.objects.filter(date_joined__month = 12).count())
            return JsonResponse({'data': register_list, 'mess': 'sucess', 'label':'Total User Register'})
        if type == 'chart2':
            register_list = []
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 1).count())     
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 2).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 3).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 4).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 5).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 6).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 7).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 8).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 9).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 10).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 11).count())
            register_list.append(Activity.objects.filter(type=3, date_posted__month = 12).count())
            return JsonResponse({'data': register_list, 'mess': 'sucess','label':'Total Reviews'})
        if type == 'chart3':
            register_list = []
            register_list.append(PostToUser.objects.filter(date_posted__month = 1).count())     
            register_list.append(PostToUser.objects.filter(date_posted__month = 2).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 3).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 4).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 5).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 6).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 7).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 8).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 9).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 10).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 11).count())
            register_list.append(PostToUser.objects.filter(date_posted__month = 12).count())
            return JsonResponse({'data': register_list, 'mess': 'sucess', 'label':'Total Posts'})
        
    return JsonResponse({'mess':'error'})

@csrf_exempt
def post_now(request):
    if request.method == "POST":
        if request.is_ajax():
            content = request.POST.get('content')
            user = request.user
            PostToUser.objects.create(author = user, to_user = user, content = content)

            data = {}
            data['content']  = content
            data['date_posted'] = 'just now'
            data['mess'] = 'oke'

            return JsonResponse(data)
    return JsonResponse({'mess':'error'})
    





@csrf_exempt
@login_required
def get_data_chart2(request):
    if request.is_ajax():
        # get top 6 user hoat dong nhieu nhat 
        all_user = User.objects.all()
        lables = []
        data = []
        for user in all_user:
            lables.append(user.username)
            data.append(check_activity(user))
        total_acivitys = Activity.objects.all().count()
        return JsonResponse({'mess':'success', 'labels':lables, 'data':data, 'total': total_acivitys})
    return JsonResponse({'mess':'error'})

def check_activity(user):
    return Activity.objects.filter(user=user).count()

@csrf_exempt
@login_required
def get_chart_post(request):
    if request.is_ajax():
        # Top cac bai post nhieu report nhat 
        total_likes =0 
        total_comments =0
        total_reports = 0
        data = []
        for post in PostToUser.objects.all():
            total_likes += post.total_likes()
            total_comments +=  post.total_comments()
            total_reports += post.total_reports()
        data = [total_likes, total_comments, total_reports]
        total_post = PostToUser.objects.all().count()
        print(data)
        return JsonResponse({'mess':'success', 'data' : data, 'total': total_post})
    return JsonResponse({'mess':'error'})
