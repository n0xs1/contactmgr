import datetime
import os.path

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from json import dumps

from django.contrib.auth.decorators import login_required
from django.conf import settings

from manage_contacts.models import Contact, Product, Entitlement, Organization
from .models import License
from .forms import ChoiceForm, SearchForm, NewLicenseForm, SearchChoiceForm
from .services import *

base_dir = str(settings.BASE_DIR)

# Create your views here.

@login_required
def manage_licenses(request):
    """ Render manage-licenses html page """
    #Get current user info
    current_user = request.user
    user_email = current_user.email

    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    user_role = contact_data.role

    user_org = contact_data.organization
    org_id = user_org.id
    org_name = user_org.org_name

    #Get entitlement data for current contact organization
    product_entitlements = Entitlement.objects.filter(organization=org_id)

    #Get product data for current contact organization
    product_licenses = License.objects.filter(org_id=org_id)

    #Create a search form
    # search_form = SearchForm()
    license_header = get_license_header()

    license_choice_list = get_choice_list(license_header)

    # choice_list = []
    # for key in license_header:
    #     # for key in product_license:
    #     choice_list.append((key, license_header[key]))


    license_search_form =  SearchChoiceForm(auto_id='license_search_form_%s', choice_list=license_choice_list)

    entitlement_header = get_entitlement_header()
    entitlement_choice_list = get_choice_list(entitlement_header)
    entitlement_search_form =  SearchChoiceForm(auto_id='entitlement_search_form_%s', choice_list=entitlement_choice_list)

    
    #Clear search filter on response from clear search button
    # if request.GET.get("clear_search"):
    #     return HttpResponseRedirect(request.path_info)

    #Create product choices from entitlements
    product_choices = []
    for entitlement in product_entitlements:
        product_choices.append((entitlement.product.product_name, entitlement.product.product_name))

    #Create a form for license generation
    new_license_form = NewLicenseForm(product_choices=product_choices)

    #Generate license on response from form
    if request.method == "POST":
        user_query = request.POST
        product_choice = user_query.get('product_choice')

        #Get entitlement data
        entitlement_product = Product.objects.filter(product_name=product_choice).get()
        product_id = entitlement_product.id
        entitlement_data = product_entitlements.filter(product=product_id).get()

        #Create license if entitlements exist
        if entitlement_data.check_allocated_licenses():
            new_license = create_license(current_user, user_query)
            new_license.save()
                                
            #Reduce license allocations after successful generation
            entitlement_data.total_licenses -= 1
            entitlement_data.save()

            messages.add_message(request, messages.INFO, 'New license created')
            return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request, messages.INFO, 'Not enough product entitlements')
            return HttpResponseRedirect(request.path_info)

    
    #Check for input from delete license
    if request.GET.get('delete_license_button'):

        user_selection = request.GET.getlist("check-box")
        print(user_selection)


        delete_license(current_user, user_selection)
        messages.add_message(request, messages.INFO, 'Selection Deleted')
        return HttpResponseRedirect(request.path_info)

    #Check for input to generate license
    if request.GET.get("generate_license_selection"):
        user_selection = request.GET.getlist("check-box")
        # print(user_selection)
        license_array = generate_license_array(current_user, user_selection)
        messages.add_message(request, messages.INFO, license_array["Message"])
        return HttpResponseRedirect(request.path_info)
    
    #Render variables in html
    context = {'user_email': user_email,
                'user_role': user_role,
                'user_org':org_name,
                'org_id': org_id,
                'product_licenses': product_licenses,
                'user_products': product_entitlements,
                # 'product_form':product_form,
                # 'entitlement_list':entitlement_list,
                'license_search_form':license_search_form,
                'new_license_form':new_license_form,
                'entitlement_search_form':entitlement_search_form,
                }

    return render(request, "manage_licenses/manage-licenses.html", context)


def download_license(request):
    """ Download a generated license """
    license_file = base_dir + "/bin/Product-License.lic"
    if os.path.isfile(license_file):
        f = open(license_file, "r")
        license_data = f.read()
        os.remove(license_file)
        license_data = license_data.replace("\n", "\r\n")
        response = HttpResponse(license_data, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="product-license.lic"'
        return response

    else:
        response = HttpResponse("No file exists", content_type="text/plain")
        return response


def get_entitlement_data(request):
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    entitlement_data = Entitlement.objects.filter(organization=org_id)

    table_header = get_entitlement_header()
    # table_header = {'product_name':'Product Name', 'product_version':'Product Version', 'num_allocated':'Allocated'}
    table_data = get_table_data(table_header, entitlement_data)
    return JsonResponse(table_data)


def get_license_data(request):
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user=user_id).get()
    org_id = contact_data.organization.id
    license_data = License.objects.filter(org_id=org_id)
    table_header = get_license_header()
    table_data = get_table_data(table_header, license_data)
    return JsonResponse(table_data)