import json

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from core.forms import ShortURLForm
from core.models import ShortURL


@csrf_exempt
def create_url(request):
    if request.method != "POST":
        return JsonResponse({}, status=405)
    try:
        form = ShortURLForm(json.loads(request.body))
    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "request is not readable"}, status=422)

    if form.is_valid():
        # usually I would encapsulate the following in the method save of the form
        try:
            short_url = ShortURL.id_generator()
            ShortURL.objects.create(url=form.cleaned_data.get("url"), short_url=short_url)
            return JsonResponse({"url": f"http://localhost:8000/s/{short_url}"}, status=201)
        except ValueError:
            return JsonResponse({"error": "an error occured while generating the short url"}, status=400)

    return JsonResponse(form.errors.as_json(), status=422, safe=False)


def get_url(request, slug):
    try:
        short_url = ShortURL.objects.get(short_url=slug)
        short_url.counter = F("counter") + 1  # F-expression helps in that case to avoid race condition
        # more in the docs :
        # https://docs.djangoproject.com/en/3.2/ref/models/expressions/#avoiding-race-conditions-using-f
        short_url.save()
    except ShortURL.DoesNotExist:
        return JsonResponse({}, status=404)

    return redirect(short_url.url)
