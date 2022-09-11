from django.views.generic import TemplateView

message = ""


def set_message(input_message):
    global message
    message = input_message


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        global message
        context = super().get_context_data(**kwargs)
        context["message"] = message
        message = ""
        return context
