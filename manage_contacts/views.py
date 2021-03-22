import datetime

from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Contact, Organization, Product, Entitlement
from .forms import ContactCreationForm, SearchChoiceForm, OrgCreationForm, ProductCreationForm, EntitlementCreationForm, ChoiceForm

from .services import *


#Manage Contacts Views#
@login_required
def manage_contacts(request):
    """ Render manage-contacts html page """
    #Get current user info
    current_user = request.user
    user_id = current_user.id
    user_email = current_user.email
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name
    org_id = user_data.organization.id

    # contact_objects = Contact.objects.filter(organization=org_id)
    
    contact_header = get_contact_header()
    contact_choice_list = get_choice_list(contact_header)

    contact_search_form = SearchChoiceForm(auto_id='contact_search_form_%s', choice_list=contact_choice_list)

    # if request.GET.get("filter_contactchoice"):
    #     user_query = request.GET
    #     filter_choice = user_query.get("filter_choice")
    #     search_field = user_query.get("search_field")
    #     contact_list = filter_contacts(contact_list=contact_list, filter_choice=filter_choice, search_field=search_field)

    #Clear search filter on response from clear search button
    # elif request.GET.get("clear_search"):
    #     contact_list = []
    #     for contact in contact_objects:
    #         user_dict = contact.get_table_dictionary()
    #         contact_list.append(user_dict)

    #Check for input from delete contacts
    # if request.GET.get('delete_contact_button'):
    #     user_selection = request.GET.getlist("check-box")
    #     message = delete_contacts(user_selection)
    #     messages.add_message(request, messages.INFO, message)
    #     return HttpResponseRedirect(request.path_info)

    #Render variables in html
    context = {'user_email':user_email,
               'user_role':user_role,
               'org_id':org_id,
               'user_org':user_org,
               'contact_search_form':contact_search_form,
            }

    return render(request, "manage_contacts/manage-contacts.html", context)

@login_required
def add_contact(request):
    """ Render add-contact html page """
    #Get current contact role to check for admin access
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role

    #Get current contact organization
    contact_data = Contact.objects.filter(user_id=user_id).get()
    new_contact_org = contact_data.organization

    org_objects = Organization.objects.all()
    choice_list = []
    for org_object in org_objects:
        choice_list.append(org_object.org_name)

    #Check for user submission
    if request.method == 'POST':
        contact_form = ContactCreationForm(request.POST)

        if contact_form.is_valid():
            user_query = request.POST
            if request.POST.get('select_org'):
                org_selection = request.POST.get('select_org')
                print(org_selection)
                new_contact_org = Organization.objects.filter(org_name=org_selection).get()

            add_new_contact(user_query=user_query, contact_organization=new_contact_org)
            messages.add_message(request, messages.INFO, 'New contact created')
            return HttpResponseRedirect(request.path_info)


    else:
        #Create a contact form if no data has been posted
        contact_form = ContactCreationForm()


    #Render variables in html
    context = {'user_role':user_role, 'contact_org':new_contact_org, 'contact_form':contact_form, 'choice_list':choice_list}
    return render(request, "manage_contacts/add-contact.html", context)


def delete_contact_selection(request, contact_id):

        # user_selection = request.GET.getlist("check-box")
        response = delete_contact(contact_id)
        

        return get_contact_data(request)
        
        # messages.add_message(request, messages.INFO, message)


        # return HttpResponseRedirect(request.path_info)


def get_contact_data(request):
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    org_id = user_data.organization.id
    contact_data = Contact.objects.filter(organization=org_id)
    table_header = get_contact_header()
    table_data = get_table_data(table_header, contact_data)
    return JsonResponse(table_data)



##Automai admin views
@login_required
def admin_dash(request):
    """ Render admin dash """
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name
    org_objects = Organization.objects.all()
    product_objects = Product.objects.all()
    entitlement_objects = Entitlement.objects.all()

    #Check for input to delete orgs
    if request.GET.get('delete_organization_selection'):
        user_selection = request.GET.getlist("org_selection")
        delete_object_selection(data_objects=Organization, user_selection=user_selection)
        messages.add_message(request, messages.INFO, 'Selection Deleted')
        return HttpResponseRedirect(request.path_info)

     #Check for input to delete products
    if request.GET.get('delete_product_selection'):
        user_selection = request.GET.getlist("product_selection")
        delete_object_selection(data_objects=Product, user_selection=user_selection)
        messages.add_message(request, messages.INFO, 'Selection Deleted')
        return HttpResponseRedirect(request.path_info)

     #Check for input from delete entitlements
    if request.GET.get('delete_entitlement_selection'):
        user_selection = request.GET.getlist("entitlement_selection")
        delete_object_selection(data_objects=Entitlement, user_selection=user_selection)
        messages.add_message(request, messages.INFO, 'Selection Deleted')
        return HttpResponseRedirect(request.path_info)

    context = {'user_role':user_role,
               'user_org':user_org,
               'org_objects':org_objects,
               'product_objects':product_objects,
               'entitlement_objects':entitlement_objects}

    return render(request, "manage_contacts/admin-dash.html", context)

@login_required
def add_organization(request):
    """ Render add organization page"""
    org_form = OrgCreationForm()
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    if request.method == 'POST':
        org_form = OrgCreationForm(request.POST)
        if org_form.is_valid():
            user_query = request.POST     
            success_message = add_new_organization(user_query)            
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, "Invalid submission")
            return HttpResponseRedirect(request.path_info)

    context = {'user_role':user_role, 'user_org':user_org, 'org_form':org_form}
    return render(request, "manage_contacts/add-organization.html", context)
    

def get_org_data(request):
    # current_user = request.user
    # user_id = current_user.id
    # user_data = Contact.objects.get()
    # org_id = user_data.organization.id
    # org_data = Contact.objects.filter(organization=org_id)
    org_data = Organization.objects.all()

    table_header = get_org_header()
    table_data = get_table_data(table_header, org_data)

    return JsonResponse(table_data)


@login_required
def add_product(request):
    """ Render add product page """
    product_form = ProductCreationForm()
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    if request.method == 'POST':
        product_form = ProductCreationForm(request.POST)
        if product_form.is_valid():
            user_query = request.POST
            success_message = add_new_product(user_query)

            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, "Invalid submission")
            return HttpResponseRedirect(request.path_info)


    context = {'user_role':user_role, 'user_org':user_org, 'product_form':product_form}
    return render(request, "manage_contacts/add-product.html", context)
    
@login_required
def add_entitlement(request):
    """ Render add entitlement page """
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    org_data = Organization.objects.all()
    org_list = []
    for organization in org_data:
        org_list.append((organization.org_name, organization.org_name))

    product_data = Product.objects.all()
    product_list = []
    for product in product_data:
        product_list.append((product.product_name, product.product_name))
        
    entitlement_form = EntitlementCreationForm(org_list=org_list, product_list=product_list)

    if request.method == 'POST':
        entitlement_form = EntitlementCreationForm(request.POST, product_list=product_list, org_list=org_list)
        if entitlement_form.is_valid():
            user_query = request.POST
            success_message = add_new_entitlement(user_query)
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, "Invalid submission")
            return HttpResponseRedirect(request.path_info)

    context = {'user_role':user_role, 'user_org':user_org, 'entitlement_form':entitlement_form}
    return render(request, "manage_contacts/add-entitlement.html", context)





def check_return(request, pk):
    # username = request.GET.get('username', None)
    data = {
        'check':pk
    }
    return JsonResponse(data)
    