from django.shortcuts import render
import json
# Create your views here.
from django.views.generic import ListView, FormView, TemplateView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth import authenticate, login
from .models import UserProfile, ClientMaster, Candidate, DrvingLicence
from .forms import *
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# nibinsha
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date


def handle_uploaded_file(f):
    with open('app/media/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class UserLogin(FormView):
    template_name = 'login.html'
    form_class = userprofileForm
    success_url = 'home'

    def post(self, request, *args, **kwargs):
        cd = self.get_form().data
        username = cd.get('username')
        print(username)
        password = cd.get('password')
        print(password)
        try:
            user = UserProfile.objects.get(email=username)
        except:
            user = None
        if user:
            if user.check_password(password):
                user = user
        else:
            messages.info(request, 'Please check the Email and Password!')
            return HttpResponseRedirect(reverse('login'))
        # user = authenticate(username = username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))


class Home(ListView, LoginRequiredMixin):
    template_name = 'app/home.html'
    # form_class = ClientMaster
    success_url = 'home'
    model = Candidate


class ClientList(ListView, LoginRequiredMixin):
    template_name = 'app/client_form.html'
    # form_class = ClientMaster
    success_url = 'client_master'
    model = ClientMaster

    def get_context_data(self, **kwargs):
        context = super(ClientList, self).get_context_data(**kwargs)
        clientFormSet = formset_factory(ClientMasterForm)
        formset = clientFormSet()
        context['formset'] = formset
        # import pdb; pdb.set_trace()
        return context

    # def get_queryset(self):
    #     import pdb; pdb.set_trace()


# class clientSave(CreateView):
#     form_class = ClientMaster
#     model = ClientMaster
#     template_name = 'app/client_form.html'

#     def get_success_url(self):
#         return reverse('candidate_list')


class CandidateList(ListView, LoginRequiredMixin):
    # template_name = 'app/candidate.html'
    template_name = 'app/candidate_list.html'
    # form_class = ClientMaster
    success_url = 'candidate_master'
    model = Candidate
    # form_class = CandidateForm

    # def get_context_data(self, **kwargs):
    #     context = super(CandidateList, self).get_context_data( **kwargs)
    #     # import pdb; pdb.set_trace()
    #     # extra_count =context['object_list'].count()+1
    #     # clientFormSet = formset_factory(CandidateForm, extra = 5)
    #     # formset = CandidateFormset()
    #     # context['formset']= formset
    #     import pdb; pdb.set_trace()
    #     return context

    # def get_initial(self):
    #     # import pdb; pdb.set_trace()
    #     initial = self.model.objects.values()
    #     return initial

    # def post(self, request, *args, **kwargs):
    #     # cd = self.get_form().data
    #     # import pdb; pdb.set_trace()

    #     formset = CandidateFormset(request.POST)
    #     if formset.is_valid():
    #         for form in formset:
    #                 # only save if name is present
    #                 # if form.cleaned_data.get('name'):
    #             form.save()
    #     else:
    #         import pdb; pdb.set_trace()
    # return redirect('candidate_list')

class Report(ListView, LoginRequiredMixin):
    template_name = 'app/report.html'
    success_url = 'candidate_master'
    model = Candidate

class CandidateAdd(CreateView):
    form_class = CandidateForm
    model = Candidate
    template_name = 'app/candidate_save.html'

    def get_success_url(self):
        return reverse('candidate_list')

    # def post(self, request, *args, **kwargs):
    #     cd = self.get_form().data
    #     import pdb; pdb.set_trace()
    # username = cd.get('username')
    # password = cd.get('password')
    # user = authenticate(username = username, password=password)
    # if user:
    #     if user.is_superuser:
    #         login(request, user)
    #         return HttpResponseRedirect(reverse('dashboard'))
    #     if user.is_active:
    #         login(request, user)
    #         return HttpResponseRedirect(reverse('home'))
    # else:
    #     return HttpResponseRedirect(reverse('register'))


class CandidateEditView(UpdateView):
    template_name = 'app/candidate_save.html'
    model = Candidate
    form_class = CandidateForm
    pk_url_kwarg = 'candidate_id'

    def get_context_data(self, *args, **kwargs):
        context = super(CandidateEditView, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        return reverse('candidate_list')

    def get_initial(self):
        initial = super(CandidateEditView, self).get_initial()
        initial["company"] = self.object.interview.company.company_name
        initial["scheduled_on"] = self.object.interview.scheduled_on
        initial["duration_in_min"] = self.object.interview.duration_in_min
        try:
            dr_licence = self.object.driving_license.all()[0]
            initial["licence_id"] = dr_licence.licence_id
            initial["country"] = dr_licence.country
            initial["valid_up_to"] = dr_licence.valid_up_to
        except IndexError:
            pass

        # initial["matches"] = Candidate.objects.get(interview = self.kwargs.get('pk'))
        return initial

    def post(self, request, *args, **kwargs):
        cd = self.request.POST

        # try:
        candidate_id = kwargs.get('candidate_id')

        if not cd.get('interview'):
            inter = Interview.objects.create()
        else:
            inter = Interview.objects.get(id=cd.get('interview'))

        inter.company_id = cd.get('intervew_company')
        inter.scheduled_on = cd.get('scheduled_on') if cd.get('scheduled_on') else None
        inter.duration_in_min = cd.get('duration_in_min') if cd.get('duration_in_min') else 0
        inter.save()
        licence_id = cd.get('licence_id')
        # try:
        #     dr_licence = DrvingLicence.objects.get(licence_id= licence_id)
        #     if cd.get('country') == dr_licence.country:
        #         dr_licence.valid_up_to = cd.get('valid_up_to')

        # except DrvingLicence.DoesNotExist:
        #     # dr_licence = DrvingLicence.objects.create()
        #     dr_licence = DrvingLicence()
        #     dr_licence.country = cd.get('country')
        #     dr_licence.valid_up_to = cd.get('valid_up_to') if cd.get('valid_up_to') else None
        #     dr_licence.licence_id = cd.get('licence_id')
        #     dr_licence.save()

        # dr_licence.save()

        # can = Candidate.objects.get_or_create(id = candidate_id)
        # if candidate_id :
        can = Candidate.objects.get(id=candidate_id)
        try:
            dr_licence = can.driving_license.all()[0]
        except IndexError:
            dr_licence = DrvingLicence()

        dr_licence.country = cd.get('country')
        dr_licence.valid_up_to = cd.get('valid_up_to') if cd.get('valid_up_to') else None
        dr_licence.licence_id = cd.get('licence_id')
        dr_licence.save()

        can.driving_license.add(dr_licence)
        # else:
        #     can = Candidate()
        # import pdb; pdb.set_trace()
        can.first_name = cd.get('first_name')
        can.last_name = cd.get('last_name')
        can.primary_mob_no = cd.get('primary_mob_no')
        can.secondary_mob_no = cd.get('secondary_mob_no')
        can.age = cd.get('age')
        can.dob = cd.get('dob')
        can.passport_no = cd.get('passport_no')
        can.passport_expery_date = cd.get('passport_expery_date') if cd.get('passport_expery_date') else None
        can.driving_license.add(dr_licence)
        can.job_category = cd.get('job_category')
        can.total_experence = cd.get('total_experence')
        can.abroad_experence = cd.get('abroad_experence')
        # can.document_files = cd.get('document_files')
        if self.request.FILES.get('document_files'):
            can.document_files = self.request.FILES.get('document_files')
        can.interview = inter
        can.interview_status = cd.get('interview_status')
        can.visa_approval_status = True if cd.get('visa_approval_status') else False
        can.salary_details = cd.get('salary_details')
        can.passport_status = cd.get('passport_status')
        can.departure_date = cd.get('departure_date') if cd.get('departure_date') else None
        can.save()
        return HttpResponseRedirect(reverse('candidate_list'))


# class CandidateDeleteView(RedirectView):
#     # template_name = 'app/candidate_confirm_delete.html'
#     model = Candidate
#     form_class = CandidateForm
#     pk_url_kwarg = 'candidate_id'


#     def get_context_data(self,*args, **kwargs):
#         context = super(CandidateDeleteView, self).get_context_data( *args, **kwargs)
#         return context

#     def get_success_url(self):
#         return reverse('candidate_list')


class CandidateDeleteView(RedirectView):
    # template_name = "admin/admin_departments.html"
    pattern_name = 'candidate_id'

    # url = 'app/data-table.html'

    # def get_redirect_url(self, *args, **kwargs):
    #     import ipdb; ipdb.set_trace()

    def get(self, request, *args, **kwargs):
        self.candidate_id = kwargs.get("candidate_id")
        tt = Candidate.objects.filter(id=self.candidate_id)
        tt.delete()
        # return super(CandidateDeleteView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('candidate_list'))


# nibinsha
# subuser details

class SubuserList(ListView):
    template_name = 'app/subuser_list.html'
    success_url = 'subuser_list'
    model = UserProfile


class SubuserSave(CreateView):
    form_class = SubuserForm
    model = UserProfile
    template_name = 'app/subuser_form.html'

    def get_success_url(self):
        return reverse('subuser_list')


class SubuserEditView(UpdateView):
    template_name = 'app/subuser_form.html'
    model = UserProfile
    form_class = SubuserForm
    pk_url_kwarg = 'subuser_id'

    def get_context_data(self, *args, **kwargs):
        context = super(SubuserEditView, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        return reverse('subuser_list')


class SubuserDelete(RedirectView):
    pattern_name = 'subuser_id'

    def get(self, request, *args, **kwargs):
        self.subuser_id = kwargs.get("subuser_id")
        tt = UserProfile.objects.filter(id=self.subuser_id)
        tt.delete()
        return HttpResponseRedirect(reverse('subuser_list'))


# company details

class CompanyList(ListView):
    # template_name = 'app/candidate.html'
    template_name = 'app/company_list.html'
    # form_class = ClientMaster
    success_url = 'candidate_master'
    model = ClientMaster


class CompanyAdd(CreateView):
    form_class = ClientMasterForm
    model = ClientMaster
    template_name = 'app/company_form.html'

    def get_success_url(self):
        return reverse('company_list')


class CompanyEditView(UpdateView):
    template_name = 'app/company_form.html'
    model = ClientMaster
    form_class = ClientMasterForm
    pk_url_kwarg = 'company_id'

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyEditView, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        return reverse('company_list')


class CompanyDelete(RedirectView):
    pattern_name = 'company_id'

    def get(self, request, *args, **kwargs):
        self.subuser_id = kwargs.get("company_id")
        tt = ClientMaster.objects.filter(id=self.subuser_id)
        tt.delete()
        return HttpResponseRedirect(reverse('company_list'))


# logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


# mail functinality


class MailingView(View):
    pattern_name = 'intervew_company'

    def get(self, request, *args, **kwargs):
        self.intervew_company = kwargs.get("intervew_company")
        print(self.intervew_company)
        # tt = ClientMaster.objects.filter(id=self.company_name)
        # tt.delete()
        # return HttpResponseRedirect(reverse('company_list'))

class ReportCandidate(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReportCandidate, self).dispatch(*args, **kwargs)

    def post(self, request):
        data_list=[]
        start_date = str(datetime.strptime(str(request.POST['from']),'%m/%d/%Y').strftime('%Y-%m-%d'))
        end_date = str(datetime.strptime(str(request.POST['to']),'%m/%d/%Y').strftime('%Y-%m-%d'))
        candidate_obj = Candidate.objects.filter(added_date__range=(start_date,end_date))
        for li in candidate_obj:
            data=[li.id,li.first_name,li.last_name,li.primary_mob_no,li.age,str(li.passport_expery_date),li.job_category,str(li.added_date),li.interview_status]
            data_list.append(data)
        return HttpResponse(json.dumps(data_list))