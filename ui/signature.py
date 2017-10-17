from sigauth.utils import RequestSigner

from django.conf import settings


api_signer = RequestSigner(settings.API_SIGNATURE_SECRET)
