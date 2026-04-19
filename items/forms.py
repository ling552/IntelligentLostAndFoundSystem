from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Item
        fields = [
            "type",
            "title",
            "category",
            "description",
            "location",
            "time",
            "contact",
            "image",
        ]
        widgets = {
            "type": forms.Select(),
            "title": forms.TextInput(
                attrs={"placeholder": "例如：学生证、AirPods、保温杯"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 5, "placeholder": "补充颜色、品牌、编号、明显特征等关键信息"}
            ),
            "location": forms.TextInput(
                attrs={"placeholder": "例如：图书馆二楼、教学楼 A-203、操场看台"}
            ),
            "contact": forms.TextInput(
                attrs={"placeholder": "电话、微信或 QQ，建议做适度脱敏"}
            ),
            "image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def clean_title(self):
        value = (self.cleaned_data.get("title") or "").strip()
        if not value:
            raise forms.ValidationError("请输入物品名称。")
        return value

    def clean_location(self):
        return (self.cleaned_data.get("location") or "").strip()

    def clean_contact(self):
        return (self.cleaned_data.get("contact") or "").strip()

    def clean_description(self):
        return (self.cleaned_data.get("description") or "").strip()
