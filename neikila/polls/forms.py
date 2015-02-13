class QuestionForm(forms.From):
    
    def __init__ (self, *argc, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuestionForm, self).__init__(*args, *kwargs)

    def save(self, commit=True):
        obj = super(QuestionForm, self).save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Question
        exclude ('user', )
