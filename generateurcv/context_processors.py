from .models import Sitelogo

def logo_context(request):
    config = Sitelogo.objects.first()
    return {'site_config': config}


