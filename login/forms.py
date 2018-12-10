from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    realName = forms.CharField(label='真实姓名', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    phone = forms.CharField(label='手机', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    qq = forms.CharField(label='QQ', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    weChat = forms.CharField(label='微信', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}),required=False)

    # captcha = CaptchaField(label='验证码')
