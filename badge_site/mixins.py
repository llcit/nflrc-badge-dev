# mixins.py

class ClassNameMixin(object):
	def get_context_data(self, **kwargs):
		context = super(ClassNameMixin, self).get_context_data(**kwargs)
		context['object_type'] = self.object_name
		return context