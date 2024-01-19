import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog

from mailing.forms import MailingForm, MessageForm, ClientForm, MailingModeratorForm, MailingUpdateForm
from mailing.models import Message, Mailing, Client, Logs
from mailing.services import get_cache_mailing_active, get_cache_mailing_count


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        new_mailing = form.save(commit=False)
        new_mailing.owner = self.request.user
        new_mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        if self.request.user == self.get_object():
            return MailingForm
        elif self.request.user.has_perm('mailing.set_is_activated'):
            return MailingModeratorForm


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.has_perm('mailing.can_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class HomeView(ListView):
    model = Mailing
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings_count'] = get_cache_mailing_count()
        context_data['active_mailings_count'] = get_cache_mailing_active()
        context_data['clients_count'] = len(Client.objects.all())
        blog_list = list(Blog.objects.all())
        if len(blog_list) > 3:
            random.shuffle(blog_list)
            context_data['blog_list'] = blog_list[:3]
        else:
            context_data['blog_list'] = []

        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = list(self.object.mail_to.all())
        context_data['logs'] = list(Logs.objects.filter(mailing=self.object))
        return context_data


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        _user = self.request.user
        if _user == self.get_object().owner or _user.has_perms(['mailing.can_delete', ]):
            return True
        return self.handle_no_permission()


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    extra_context = {
        'title': 'Создание сообщения'
    }

    def form_valid(self, form):
        new_message = form.save()
        new_message.owner = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Список сообщений'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.has_perm('mailing.can_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return self.handle_no_permission()


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.has_perm('mailing.can_view'):
            return queryset
        return queryset.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Добавить клиента'
    }

    def form_valid(self, form):
        new_client = form.save()
        new_client.owner = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        return self.request.user == Client.objects.get(pk=self.kwargs['pk']).owner


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        permissions = ('mailing.client_delete',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permissions):
            return True
        return self.handle_no_permission()


class LogsListView(ListView):
    model = Logs
    template_name = 'mailing/logs_list.html'
