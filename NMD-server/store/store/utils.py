class DataMixin:
    title = None
    header = None
    form_label = None
    def get_context_data(self,**kwargs):
        context = super(DataMixin,self).get_context_data(**kwargs)
        context['title'] = self.title
        context['header'] = self.header
        context['form_label'] = self.form_label
        return context