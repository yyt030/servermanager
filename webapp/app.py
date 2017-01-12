#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, current_app
from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import SelectField, SelectMultipleField, SubmitField

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='your_secret_key',
    CSRF_ENABLED=True,
))


class Select2MultipleField(SelectMultipleField):
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class DemoForm(Form):
    single_select = SelectField(u"单选", [DataRequired()],
                                choices=[("py", "python"), ("rb", "ruby"), ("js", "javascript")],
                                description=u"有限选项。无效化。",
                                render_kw={"disabled": "true"})
    single_dynamic_select = SelectField(u"单选", [DataRequired()],
                                        choices=[("0", "")],
                                        description=u"动态加载选项。",
                                        render_kw={})
    multi_select = Select2MultipleField(u"选择框", [],
                                        choices=[("py", "python"), ("rb", "ruby"), ("js", "javascript")],
                                        description=u"多选。有限选项。",
                                        render_kw={"multiple": "multiple"})
    tags = Select2MultipleField(u'标签', [],
                                choices=[("py", "python"), ("rb", "ruby"), ("js", "javascript")],
                                description=u"多选。无限选项。",
                                render_kw={"multiple": "multiple", "data-tags": "1"})
    submit = SubmitField()


@app.route("/demo", methods=["GET", "POST"])
def demo():
    form = DemoForm(request.form)

    if form.validate_on_submit():
        current_app.logger.debug(form.data)

    return render_template("demo.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
