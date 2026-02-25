from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import OrgMember
from studentorg.forms import OrgMemberForm
from django.urls import reverse_lazy

class HomePageView(ListView) :
    model = OrgMember
    context_object_name = 'home'
    template_name ='OrgMembers_home.html'

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmembers'
    template_name = 'OrgMembers_list.html'
    paginate_by = 5

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'OrgMembers_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'OrgMembers_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'OrgMembers_del.html'
    success_url = reverse_lazy('orgmember-list')
