from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, FormView, TemplateView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth import authenticate, login
from .models import UserProfile, ClientMaster, Candidate
from .forms import *
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
#nibinsha
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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

@method_decorator(login_required, name='dispatch')
class Home(ListView):
    template_name = 'app/home.html'
    # form_class = ClientMaster
    success_url = 'home'
    model = Candidate


class ClientList(ListView):
    template_name = 'app/client_form.html'
    # form_class = ClientMaster
    success_url = 'client_master'
    model = ClientMaster


    def get_context_data(self, **kwargs):
        context = super(ClientList, self).get_context_data( **kwargs)
        clientFormSet = formset_factory(ClientMasterForm)
        formset = clientFormSet()
        context['formset']= formset
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



class CandidateList(ListView):
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

    def get_context_data(self,*args, **kwargs):
        context = super(CandidateEditView, self).get_context_data( *args, **kwargs)
        return context

    def get_success_url(self):
        return reverse('candidate_list')


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





#nibinsha
#subuser details

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

    def get_context_data(self,*args, **kwargs):
        context = super(SubuserEditView, self).get_context_data( *args, **kwargs)
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


#company details

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

    def get_context_data(self,*args, **kwargs):
        context = super(CompanyEditView, self).get_context_data( *args, **kwargs)
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




#logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


#mail functinality


class MailingView(View):
    pattern_name = 'intervew_company'

    def get(self, request, *args, **kwargs):
        self.intervew_company = kwargs.get("intervew_company")
        print(self.intervew_company)
        # tt = ClientMaster.objects.filter(id=self.company_name)
        # tt.delete()
        # return HttpResponseRedirect(reverse('company_list'))
