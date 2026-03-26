from django.forms import DateInput

class XDSoftDateTimePickerInput(DateInput):
    template_name = "widgets/datepicker/XDSoftDateTime_datepicker.html"

    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/jquery-datetimepicker/2.5.20/jquery.datetimepicker.min.css",
            )
        }
        js = (
            # "https://code.jquery.com/jquery-3.3.1.slim.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery-datetimepicker/2.5.20/jquery.datetimepicker.full.min.js",
        )
