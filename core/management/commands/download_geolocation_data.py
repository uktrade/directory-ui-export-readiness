from io import BytesIO
import os
import tarfile

import requests

from django.core.management import BaseCommand
from django.conf import settings


class GeolocationArchive(BytesIO):

    @classmethod
    def from_url(cls, url):
        response = requests.get(url)
        response.raise_for_status()

        file_like_object = cls()
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                file_like_object.write(chunk)
        file_like_object.seek(0)
        return file_like_object

    def decompress(self, file_name, destination):
        tar = tarfile.open(mode="r:gz", fileobj=self)
        for member in tar.getmembers():
            if member.name.endswith(file_name):
                member.name = file_name
                tar.extract(member, path=destination)
                break
        else:
            raise ValueError(file_name + ' not found in geolocation archive')


class Command(BaseCommand):

    help = 'Download the latest geolocation data'

    def handle(self, *args, **options):

        if not os.path.exists(settings.GEOIP_PATH):
            os.makedirs(settings.GEOIP_PATH)

        compressed_database = GeolocationArchive.from_url(
            settings.GEOLOCATION_MAXMIND_DATABASE_FILE_URL
        )
        compressed_database.decompress(
            file_name=settings.GEOIP_COUNTRY,
            destination=settings.GEOIP_PATH
        )
