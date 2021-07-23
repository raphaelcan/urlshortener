import random
import string

from django.db import models


class ShortURL(models.Model):
    short_url = models.CharField(max_length=7, unique=True, db_index=True)  # ensure uniqueness on the database level + indexed as it will be often accessed
    url = models.URLField( max_length=300)  # I do not know the max length of the url, in a first approach I set 300 chars.
    counter = models.IntegerField(default=0)

    @classmethod
    def id_generator(cls, size=7, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase, retry=3):
        """
        It could be implemented using a while, but a loop with a retry of 3 should be enough to avoid collision even for a
        large database. the retry parameter can be increased based on the requirements. In case of a collision after 3 trials
        I would consider the event as suspicious and log it. In our case I raise a simple exception ValueError

        :param size:
        :param chars:
        :param retry:
        :return:
        """
        slug = None
        for _ in range(retry):
            slug = ''.join(random.choice(chars) for _ in range(size))
            if not cls.objects.filter(short_url=slug).exists():
                break
        if slug is None:
            raise ValueError
        return slug
