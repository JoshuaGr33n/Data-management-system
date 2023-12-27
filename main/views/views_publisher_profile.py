from ..decorators import authentication_required, admin_privilege, check_month_year, publisher_profile_privilege, restrict_followers
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from ..models import PublisherProfile, User, MonthYear, PublisherReport
from django.shortcuts import render, redirect
# from ..forms import MyForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
import datetime, random, os
from django.conf import settings
from django.utils.crypto import get_random_string
from django.views import View
from django.db.models import Q, F


@authentication_required
@publisher_profile_privilege
def publisher_profile(response, username):
    publisher = response.user
    
    if len(username) == 0:
        return HttpResponseRedirect("/publishers/all-active-publishers")
    try:
        profile = PublisherProfile.objects.get(username=username)
    except (PublisherProfile.DoesNotExist):
        return HttpResponseRedirect("/publishers/all-active-publishers")
    
    if profile.username == profile.parent_id:
        parent_id = "Full Account"
    else:
        parent = PublisherProfile.objects.get(username=profile.parent_id )
        parent_id = f"{parent.first_name} {parent.last_name}"
    
    nav = publisher.first_name
    context = {
        "parent" : parent_id,
        "publisher": publisher, 
        "profile": profile, 
        "nav": nav,
    }    
    return render(response, "main/publisher-profile/publisher-profile.html", context)

@authentication_required
@publisher_profile_privilege
def publisher_profile_settings(request, username):
    publisher = request.user
    
    if len(username) == 0:
        return HttpResponseRedirect("/publishers/all-active-publishers")
    try:
        profile = PublisherProfile.objects.get(username=username)
        if profile.username == profile.parent_id:
            parent_id = "Full Account"
        else:
            parent = PublisherProfile.objects.get(username=profile.parent_id )
            parent_id = f"{parent.first_name} {parent.last_name}"
        
        if profile.gender == 'M':
            gender = 'Male'
        else:
            gender = 'Female'        
        
        if publisher.publisherprofile.privilege == "1":
            disabled = ''
        else:
            disabled = 'disabled' 
               
        nav = publisher.first_name
        context = {
            "parent" : parent_id,
            "publisher": publisher, 
            "profile": profile, 
            "gender": gender,
            "nav": nav,
            "disabled": disabled,
        }    
    except (PublisherProfile.DoesNotExist):
        return HttpResponseRedirect("/publishers/all-active-publishers")
    return render(request, "main/publisher-profile/publisher-profile-settings.html", context)

def is_valid_phone(phone_number):
    # Remove any non-digit characters from the phone number
    digits_only = ''.join(filter(str.isdigit, phone_number))

    # Check if the resulting string has 11 digits
    return len(digits_only) == 11

def is_valid_password(password):
    # Check if the resulting string has at least 6 digits
    return len(password) >= 6

def check_image_exists(image_path):
    image_filename = image_path
    # full_image_path = os.path.join(settings.STATIC_ROOT, image_filename)
    full_image_path = os.path.join(settings.BASE_DIR, 'main', 'static', image_filename)
    image_exists = os.path.isfile(full_image_path)
    return image_exists

def generate_unique_random_string():
    while True:
        unique_random_string = get_random_string(length=8).upper()
        if not User.objects.filter(username=unique_random_string).exists():
            break
    return unique_random_string


@authentication_required
def publisher_profile_settings_update(request):
  
    try: 
        publisher = request.user
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            surname = request.POST.get('surname')
            middle_name = request.POST.get('middlename')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            confirm_phone = request.POST.get('confirm_phone')
            id = request.POST.get('id')
            # name = request.POST.get('first_name')
         

            # Perform manual validation
            errors = {}
            if not first_name:
                errors['first_name'] = ['First Name is required.']
            
            if not surname:
                errors['surname'] = ['Surname is required.']
            
            if not gender:
                errors['gender'] = ['Gender is required.']        
            
            if not phone:
                errors['phone'] = ['Phone number is required.']
            
            if not confirm_phone:
                errors['confirm_phone'] = ['Confirm Phone number']   
                 
            if phone != confirm_phone:
                errors['confirm_phone'] = ['Phone number dont match']
            
            if not is_valid_phone(phone):
            # Do something with the valid phone number
              errors['phone'] = ['Phone number must be 11 digits']
            
            if errors:
                return JsonResponse({'success': False, 'errors': errors})
            
            profile = PublisherProfile.objects.get(id=id)
            
            if publisher.publisherprofile.privilege == "1":
               group = request.POST.get('group')
            else:
               group = profile.groupName
            
            # Update the field for the matching rows
           
        
            user = User.objects.get(id=profile.user_id)
            
        
            
            followers = PublisherProfile.objects.filter(parent_id=profile.username).exclude(username=profile.username)
            for follower in followers:
                if profile.phone == follower.phone:
                    PublisherProfile.objects.filter(id=follower.id).update(phone=phone)
    
            profile.first_name = first_name
            profile.middle_name = middle_name
            profile.last_name = surname
            profile.DOB = dob
            profile.gender = gender
            profile.phone = phone
            profile.email = email
            profile.groupName = group
            profile.save()
            
            user.first_name = first_name
            user.last_name = surname
            user.email = email
            user.phone = phone
            user.save()
            

            # Return a success response
            return JsonResponse({'success': True, 'message': 'Profile updated successfully', 'first_name': f'{user.first_name}', 'last_name': f'{user.last_name}'})
        else:
            # Handle GET requests or other methods as needed
            return JsonResponse({'success': False, 'message': 'Invalid method'})
    except (PublisherProfile.DoesNotExist):
        return HttpResponseRedirect("/publishers/all-active-publishers")
    
@authentication_required
def publisher_profile_settings_update_password(request):
  
    try: 
        if request.method == 'POST':
            if request.POST.get("update-password-process-id"):
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                id = request.POST.get('update-password-process-id')
            
                errors = {}
                if not password:
                    errors['password'] = ['Required.']
                
                if not confirm_password:
                    errors['confirm_password'] = ['Required.']
                    
                if password != confirm_password:
                    errors['confirm_password'] = ['Password dont match']
                
                if not is_valid_password(password):
                    errors['password'] = ['Password must be at least 6 characters']
                
                if errors:
                    return JsonResponse({'success': False, 'errors': errors})
                
                profile = PublisherProfile.objects.get(id=id)
                user = User.objects.get(id=profile.user_id)
                
                user.password = make_password(password)
                user.save()
                update_session_auth_hash(request, request.user)
                profile.updated_at = datetime.datetime.now()
                profile.save()
                

                # Return a success response
                return JsonResponse({'success': True, 'message': 'Password updated successfully'})
            else:
                password = str(random.randint(10000000, 99999999))
                id = request.POST.get('id')
        
                profile = PublisherProfile.objects.get(id=id)
                user = User.objects.get(id=profile.user_id)
                
                user.password = make_password(password)
                user.save()
                update_session_auth_hash(request, request.user)
                profile.updated_at = datetime.datetime.now()
                profile.save()
                

                # Return a success response
                return JsonResponse({'success': True, 'message': f'The new password is {password}'})
                
        else:
            # Handle GET requests or other methods as needed
            return JsonResponse({'success': False, 'message': 'Invalid method'})
    except (PublisherProfile.DoesNotExist):
        return HttpResponseRedirect("/publishers/all-active-publishers")  

@authentication_required
@publisher_profile_privilege
@restrict_followers
def publisher_followers(response, username):
    publisher = response.user
    
    if len(username) == 0:
        return HttpResponseRedirect("/publishers/all-active-publishers")
    try:
        profile = PublisherProfile.objects.get(username=username)
    except (PublisherProfile.DoesNotExist):
        return HttpResponseRedirect("/publishers/all-active-publishers")
    
    followers = PublisherProfile.objects.filter(parent_id=profile.username).exclude(username=profile.username).order_by('-id')
    
    image_path = 'main/profilePics/profile-picture-1n.jpg'
    image_exists = check_image_exists(image_path)
    
    nav = 'followers'
    context = {
        "no_of_followers": followers.count(),
        "image_path": image_path,
        "image_exists": image_exists,
        "followers" : followers,
        "publisher": publisher, 
        "profile": profile, 
        "nav": nav,
    }    
    return render(response, "main/publisher-profile/publisher-followers.html", context)

@authentication_required
def add_follower(request):
  
    try: 
        if request.method == 'POST':
            if request.POST.get("add-follower-publisher-id"):
                first_name = request.POST.get('first_name')
                middle_name = request.POST.get('middle_name')
                surname = request.POST.get('surname')
                gender = request.POST.get('gender')
                secondary_phone = request.POST.get('secondary_phone')
                id = request.POST.get('add-follower-publisher-id')
                
                
                profile = PublisherProfile.objects.get(id=id)
                user = User.objects.get(id=profile.user_id)
                
                check_phone = PublisherProfile.objects.filter(phone=secondary_phone).exclude(
                         parent_id=profile.username).count()
            
                errors = {}
                if not first_name:
                    errors['first_name'] = ['Required']
                
                if not surname:
                    errors['surname'] = ['Required']
                    
                if not gender:
                    errors['gender'] = ['Required']
                    
                if len(secondary_phone) == 0:
                    secondary_phone = user.phone
                else:    
                    if len(secondary_phone) != 11:
                        errors['secondary_phone'] = ['Phone number must be 11 digits']       
                
                if check_phone > 0:
                    errors['secondary_phone'] = ['Phone number already registered by a publisher outside this zone']    
                    
                    
                if errors:
                    return JsonResponse({'success': False, 'errors': errors})
                
               
                unique_random_string = generate_unique_random_string()
                
                username = first_name+unique_random_string    
                    
                user = User(
                    first_name = first_name,
                    last_name = surname,
                    phone = secondary_phone,
                    username = unique_random_string)
                user.save()
                
                
                user.refresh_from_db()
                user.publisherprofile.first_name = first_name
                user.publisherprofile.middle_name = middle_name
                user.publisherprofile.last_name = surname
                user.publisherprofile.username = username
                user.publisherprofile.gender = gender
                user.publisherprofile.phone = secondary_phone
                user.publisherprofile.pioneer = 0
                user.publisherprofile.appointment = 0
                user.publisherprofile.privilege = 0
                user.publisherprofile.parent_id = profile.username
                user.publisherprofile.status = 'Pending'
                user.publisherprofile.created_at = datetime.datetime.now()
                user.save()
                

                # Return a success response
                return JsonResponse({'success': True, 'message': 'Follower added successfully'})
            
            elif request.POST.get("create-full-account-follower-id"):
                phone = request.POST.get('create_full_account_phone')
                confirm_phone = request.POST.get('create_full_account_confirm_phone')
                password = request.POST.get('create_full_account_password')
                confirm_password = request.POST.get('create_full_account_confirm_password')
                id = request.POST.get('create-full-account-follower-id')
                
                
                profile = PublisherProfile.objects.get(user_id=id)
                user = User.objects.get(id=profile.user_id)
                
                check_phone = PublisherProfile.objects.filter(phone=phone).exclude(
                         username=profile.username).count()
            
                errors = {}
                if not phone:
                    errors['create_full_account_phone'] = ['Required']
                
                if len(phone) != 11:
                    errors['create_full_account_phone'] = ['Phone number must be 11 digits']    
                
                if not confirm_phone:
                    errors['create_full_account_confirm_phone'] = ['Required']
                else:
                    if phone != confirm_phone:
                        errors['create_full_account_confirm_phone'] = ['Phone number dont match']
                        
                if not password:
                    errors['create_full_account_password'] = ['Required']
                
                if len(password) < 6:
                    errors['create_full_account_password'] = ['Password must not be less than 6 digits']    
                    
                if not confirm_password:
                    errors['create_full_account_confirm_password'] = ['Required']
                else:    
                    if password != confirm_password:
                        errors['create_full_account_confirm_password'] = ['Password dont match']        
                    
                if check_phone > 0:
                    errors['create_full_account_phone'] = ['Phone number already taken']  
                    errors['create_full_account_confirm_phone'] = ['Phone number already taken']
                    
                    
                if errors:
                    return JsonResponse({'success': False, 'errors': errors})
                   
                user.phone = phone
                user.password = make_password(password)
                
                profile.phone = phone
                profile.parent_id = profile.username
                
                user.save()
                profile.save()
                 

                # Return a success response
                return JsonResponse({'success': True, 'message': f'Full Account for {user.first_name} {user.last_name} created successfully'})
            elif request.POST.get("currentParent_username"):
                newParent_username = request.POST.get('newParent_username')
                follower_id = request.POST.getlist('follower_id[]')
                
                followers = PublisherProfile.objects.filter(user_id__in=follower_id)
                errors = {}
                if followers.count() == 0:
                    errors['newParent_username'] = ['No follower is selected']
                
                if not newParent_username:
                    errors['newParent_username'] = ['Search and select a publisher']    
                    
                if errors:
                    return JsonResponse({'success': False, 'errors': errors})
                   
                for follower in followers:
                    followerProfile = PublisherProfile.objects.get(user_id=follower.user_id)
                    check_phone = PublisherProfile.objects.filter(phone=followerProfile.phone).count()
                    followerProfile.parent_id = newParent_username
                    if check_phone > 0:
                        newParent = PublisherProfile.objects.get(username=newParent_username)
                        followerProfile.phone = newParent.phone
                    followerProfile.save()
               
                return JsonResponse({'success': True, 'message': 'The selected followers(s) transfered successfully'})
    except (PublisherProfile.DoesNotExist):
        return HttpResponseRedirect("/publishers/all-active-publishers")  

class SearchView(View):
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        username = self.kwargs.get('username')


        results = PublisherProfile.objects.filter(
            (Q(first_name__icontains=query) | Q(last_name__icontains=query)) & Q(status='Active') & Q(username=F('parent_id'))
        ).exclude(username=username)[:5]


        data = [{'id': obj.id, 'user_id': obj.user_id, 'name': f'{obj.first_name} {obj.last_name}', 'username': obj.username, 'parent_id': obj.parent_id} for obj in results]

        return JsonResponse({'results': data})