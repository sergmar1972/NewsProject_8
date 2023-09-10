class MyMixin(object):
    mixin_group=''

    def get_proup(self):
        return self.mixin_group.upper()

    def get_upper(self,s):
        # If isinstance(s, str):
            return s.upper()
        # else:
        #     return s.title.upper()