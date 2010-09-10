from django.conf import settings


def project_settings(request):
    return {"MIMESIS_USE_FLASH_UPLOAD": settings.MIMESIS_USE_FLASH_UPLOAD}