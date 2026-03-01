from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import College, OrgMember, Organization, Program, Student
from studentorg.forms import (
    CollegeForm,
    OrgMemberForm,
    OrganizationForm,
    ProgramForm,
    StudentForm,
)
from django.urls import reverse_lazy
from django.db.models import Q 
from django.utils import timezone

class SearchableListView(ListView):
    search_param = "q"
    search_fields = ()

    def get_search_query(self):
        return self.request.GET.get(self.search_param, "").strip()

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.get_search_query()

        if query and self.search_fields:
            search_filter = Q()
            for field in self.search_fields:
                search_filter |= Q(**{f"{field}__icontains": query})
            qs = qs.filter(search_filter).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.get_search_query()

        params = self.request.GET.copy()
        params.pop("page", None)
        context["query_params"] = params.urlencode()
        return context


class HomePageView(SearchableListView) :
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"
    search_fields = ("name", "description", "college__college_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()

        today = timezone.now().date()
        count = (
            OrgMember.objects.filter(
                date_joined__year=today.year
            )
            .values("student")
            .distinct()
            .count()
        )

        context["students_joined_this_year"] = count
        return context

class OrganizationList(SearchableListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5
    ordering = ["college__college_name","name"]
    search_fields = ("name", "description", "college__college_name")

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')


class CollegeList(SearchableListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    paginate_by = 5
    search_fields = ("college_name",)


class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_form.html'
    success_url = reverse_lazy('college-list')


class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_form.html'
    success_url = reverse_lazy('college-list')


class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')


class ProgramList(SearchableListView):
    model = Program
    context_object_name = 'programs'
    template_name = 'program_list.html'
    paginate_by = 5
    search_fields = ("prog_name", "college__college_name")

    def get_ordering(self):
        allowed = ("prog_name", "college__college_name")
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "prog_name"


class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program-list')


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program-list')


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')


class StudentList(SearchableListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student_list.html'
    paginate_by = 5
    search_fields = (
        "student_id",
        "lastname",
        "firstname",
        "middlename",
        "program__prog_name",
        "program__college__college_name",
    )


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')


class OrgMemberList(SearchableListView):
    model = OrgMember
    context_object_name = 'orgmembers'
    template_name = 'OrgMembers_list.html'
    paginate_by = 5
    search_fields = (
        "student__student_id",
        "student__lastname",
        "student__firstname",
        "student__middlename",
        "organization__name",
        "organization__college__college_name",
    )


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
