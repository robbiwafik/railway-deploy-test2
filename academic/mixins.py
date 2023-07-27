from django.contrib.admin.utils import flatten_fieldsets

class UserDosenAdminMixin:
    def get_form(self, request, obj=None, **kwargs):
        """ By passing 'fields', we prevent ModelAdmin.get_form from looking 
    		up the fields itself by calling self.get_fieldsets()

        	If you do not do this you will get an error from
        	modelform_factory complaining about non-existent fields.
        """

        if not self.fieldsets:
            # Simple validation in case fieldsets don't exists 
            # in the admin declaration
            all_fields = self.form().fields.keys()
            user_fields = self.form().user_fields.keys()
            model_fields = list(
                filter(
                    lambda field: field not in user_fields, 
                    all_fields
    	        )
            )
            self.fieldsets = [(None, {'fields': model_fields})]
        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        return super().get_form(request, obj, **kwargs)        
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # convert to list just in case, its a tuple
        new_fieldsets = list(fieldsets)
        user_fields = [f for f in self.form().user_fields]
        new_fieldsets.append(
            ('USER', {'classes': ('collapse',), 'fields': user_fields})
        )
        return new_fieldsets