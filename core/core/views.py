from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import ProcessFormView
from django.http.response import HttpResponseRedirect, HttpResponseForbidden


class MultiFormMixin(ContextMixin):
    
    form_classes = {} 
    instances = {}
    querysets = {}
    prefixes = {}
    success_urls = {}
    
    grouped_forms = {}
    
    initial = {}
    prefix = None
    instance = None
    queryset = None
    success_url = None
    
     
    def get_form_classes(self):
        return self.form_classes
     
    def get_forms(self, form_classes, form_names=None, bind_all=False):
        return dict([(key, self._create_form(key, klass, (form_names and key in form_names) or bind_all)) \
            for key, klass in form_classes.items()])
    
    def get_form_kwargs(self, form_name, bind_form=False):
        kwargs = {}
        kwargs.update({'initial':self.get_initial(form_name)})
        kwargs.update({'prefix':self.get_prefix(form_name)})
        kwargs.update({'instance': self.get_instance(form_name)})   # JVR
        kwargs.update({'queryset': self.get_form_queryset(form_name)})   # JVR
        for attribute in ['instance', 'queryset']:
            if kwargs[attribute] == None:
                kwargs.pop(attribute)
        if bind_form:
            kwargs.update(self._bind_form_data())

        return kwargs
    
    def forms_valid(self, forms, form_name=None):
        form_valid_method = '%s_form_valid' % form_name
        if hasattr(self, form_valid_method):
            return getattr(self, form_valid_method)(forms[form_name])
        else:
            return HttpResponseRedirect(self.get_success_url(form_name))
     
    def forms_invalid(self, forms, form_name=None):
        for name, form in forms.items():
            print(name, form.errors)
        print(forms)
        return self.render_to_response(self.get_context_data(forms=forms))
    
    def get_initial(self, form_name):
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return self.initial.copy()
        
    def get_instance(self, form_name):
        instance_method = 'get_%s_instance' % form_name
        if hasattr(self, instance_method):
            return getattr(self, instance_method)()
        else:
            return self.instances.get(form_name, self.instance)
    
    def get_form_queryset(self, form_name):
        queryset_method = 'get_%s_queryset' % form_name
        if hasattr(self, queryset_method):
            return getattr(self, queryset_method)()
        else:
            return self.querysets.get(form_name, self.queryset)

    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)
        
    def get_success_url(self, form_name=None):
        return self.success_urls.get(form_name, self.success_url)
    
    def _create_form(self, form_name, klass, bind_form):
        form_kwargs = self.get_form_kwargs(form_name, bind_form)
        form_create_method = 'create_%s_form' % form_name
        if hasattr(self, form_create_method):
            form = getattr(self, form_create_method)(**form_kwargs)
        else:
            form = klass(**form_kwargs)
        return form
           
    def _bind_form_data(self):
        if self.request.method in ('POST', 'PUT'):
            return{'data': self.request.POST,
                   'files': self.request.FILES,}
        return {}


class ProcessMultipleFormsView(ProcessFormView):
    
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))
     
    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        form_name = request.POST.get('action')
        if self._individual_exists(form_name):
            return self._process_individual_form(form_name, form_classes)
        elif self._group_exists(form_name):
            return self._process_grouped_forms(form_name, form_classes)
        else:
            return self._process_all_forms(form_classes)
        
    def _individual_exists(self, form_name):
        return form_name in self.form_classes
    
    def _group_exists(self, group_name):
        return group_name in self.grouped_forms
              
    def _process_individual_form(self, form_name, form_classes, silent=False):
        forms = self.get_forms(form_classes, (form_name,))
        form = forms.get(form_name)
        if silent:
            if form.is_valid():
                form.save()
            else:
                print(f"Errors in '{form_name}':{form.errors}")
        else:
            if not form:
                return HttpResponseForbidden()
            elif form.is_valid():
                
                return self.forms_valid(forms, form_name)
            else:
                return self.forms_invalid(forms, form_name)
        
    def _process_grouped_forms(self, group_name, form_classes):
        form_names = self.grouped_forms[group_name]
        forms = self.get_forms(form_classes, tuple(form_names.keys()))
        group_forms = {form_name: forms.get(form_name) for form_name in form_names.values()}

        if all([form.is_valid() for form in group_forms.values()]):
            return self.forms_valid({group_name:group_forms}, group_name)
        else:
            return self.forms_invalid(forms, group_name)
        
    def _process_all_forms(self, form_classes):
        forms = self.get_forms(form_classes, None, True)
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)
 
 
class BaseMultipleFormsView(MultiFormMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """
 
class MultiFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaying several forms, and rendering a template response.
    """