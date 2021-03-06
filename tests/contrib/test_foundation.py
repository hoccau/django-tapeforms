from django import forms

from tapeforms.contrib.foundation import FoundationTapeformMixin


class DummyForm(FoundationTapeformMixin, forms.Form):
    my_field1 = forms.CharField()
    my_field2 = forms.BooleanField()
    my_field3 = forms.MultipleChoiceField(
        choices=(('foo', 'foo'), ('bar', 'bar')), widget=forms.RadioSelect)


class DummyFormWithProperties(DummyForm):
    field_label_css_class = 'custom-label'
    widget_css_class = 'some-widget-cssclass'
    field_template = 'form-wide-field-template.html'


class TestFoundationTapeformMixin:

    def test_field_template_default(self):
        form = DummyForm()
        assert form.get_field_template(
            form['my_field1']) == 'tapeforms/fields/foundation.html'

    def test_field_template_fieldset(self):
        form = DummyForm()
        assert form.get_field_template(
            form['my_field3']) == 'tapeforms/fields/foundation_fieldset.html'
        form = DummyFormWithProperties()
        assert form.get_field_template(
            form['my_field3']) == 'tapeforms/fields/foundation_fieldset.html'

    def test_field_template_fieldset_override(self):
        form = DummyForm()
        assert form.get_field_template(
            form['my_field3'], 'field-template.html') == 'field-template.html'

    def test_field_label_css_class_invalid(self):
        form = DummyForm({})
        assert form.get_field_label_css_class(
            form['my_field1']) == 'is-invalid-label'

    def test_apply_widget_invalid_options(self):
        form = DummyForm({})
        assert 'my_field1' in form.errors
        widget = form.fields['my_field1'].widget
        assert widget.attrs['class'] == 'is-invalid-input'
