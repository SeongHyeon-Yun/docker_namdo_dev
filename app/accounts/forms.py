from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "id": "pw1",
                "class": "form-control",
                "placeholder": "비밀번호 입력",
            }
        ),
    )

    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                "id": "pw2",
                "class": "form-control",
                "placeholder": "비밀번호 확인",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "boss_name",
            "email",
            "phone",
            "company_name",
            "company_num",
            "manager_name",
            "company_img",
            "sms_marketing_agree",
            "email_marketing_agree",
            "bank_name",
            "bank_num",
            "addree_1",
            "addree_2",
            "addree_3",
            "addree_4",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={"id": "id", "class": "form-control", "placeholder": "아이디"}
            ),
            "boss_name": forms.TextInput(
                attrs={
                    "id": "boss_name",
                    "class": "form-control",
                    "placeholder": "대표자 이름",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "id": "email",
                    "class": "form-control",
                    "placeholder": "name@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "id": "phone",
                    "class": "form-control",
                    "placeholder": "전화번호 - 빼고 입력",
                    "type": "tel",
                }
            ),
            "company_name": forms.TextInput(
                attrs={
                    "id": "company_name",
                    "class": "form-control",
                    "placeholder": "사업자 명",
                }
            ),
            "company_num": forms.TextInput(
                attrs={
                    "id": "company_num",
                    "class": "form-control",
                    "placeholder": "사업자 번호 - 빼고 입력",
                }
            ),
            "manager_name": forms.TextInput(
                attrs={
                    "id": "manager_name",
                    "class": "form-control",
                    "placeholder": "담당자 명",
                }
            ),
            "company_img": forms.FileInput(
                attrs={
                    "id": "company_img",
                    "class": "form-control",
                }
            ),
            "sms_marketing_agree": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "sms_marketing_agree",
                }
            ),
            "email_marketing_agree": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "email_marketing_agree",
                }
            ),
            "bank_name": forms.TextInput(
                attrs={
                    "id": "bank_name",
                    "class": "form-control",
                    "placeholder": "은행 명",
                }
            ),
            "bank_num": forms.TextInput(
                attrs={
                    "id": "bank_num",
                    "class": "form-control",
                    "placeholder": "계좌번호 - 빼고 입력",
                }
            ),
            "addree_1": forms.TextInput(
                attrs={
                    "id": "addree_1",
                    "class": "form-control",
                    "placeholder": "우편번호",
                    "readonly": "readonly",
                }
            ),
            "addree_2": forms.TextInput(
                attrs={
                    "id": "addree_2",
                    "class": "form-control",
                    "placeholder": "주소",
                    "readonly": "readonly",
                }
            ),
            "addree_3": forms.TextInput(
                attrs={
                    "id": "addree_3",
                    "class": "form-control",
                    "placeholder": "상세주소",
                }
            ),
            "addree_4": forms.TextInput(
                attrs={
                    "id": "addree_4",
                    "class": "form-control",
                    "placeholder": "참고항목",
                    "readonly": "readonly",
                }
            ),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        try:
            validate_password(password1)
        except ValidationError:
            raise forms.ValidationError("비밀번호를 다시 확인해주세요.")

        return password1

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if "-" in phone:
            raise forms.ValidationError("전화번호에 - 를 빼주세요.")

        return phone

    def clean_bank_num(self):
        bank_num = self.cleaned_data.get("bank_num")

        if "-" in bank_num:
            raise forms.ValidationError("계좌번호에 - 를 빼주세요.")

        return bank_num

    def clean_company_num(self):
        company_num = self.cleaned_data.get("company_num")

        if "-" in company_num:
            raise forms.ValidationError("사업자번호에 - 를 빼주세요.")

        return company_num

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 사용중인 아이디 입니다.")

        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "비밀번호가 일치하지 않습니다.")

        return cleaned_data
