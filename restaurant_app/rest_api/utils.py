from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.conf import settings
import traceback

RED = "\033[31m"
RESET = "\033[0m"


def custom_exception_handler(exc, context):
    if settings.DEBUG == True:
        print(f"{RED}####### WARNING! CRITICAL ERROR! ######{RESET}\n")
        print(f"{RED}Context:{RESET} {context}\n{RED}Error:{RESET} {exc}\n")
        print(f"{RED}Traceback (most recent call last):{RESET}")
        print(traceback.format_exc())
        print(f"{RED}#######################################{RESET}\n")

    response = exception_handler(exc, context)
    if response is None:
        return Response({"error": "An unexpected error occurred"}, status=500)
    return response