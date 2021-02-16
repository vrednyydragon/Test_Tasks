"""Alias web application."""
from django.http import HttpResponse
from .models import Alias
from django.utils import timezone
import datetime
from datetime import datetime

max_system_date: str = '9999-12-31 00:00:00.000001+00:00'


def index(request):
    """Start page."""
    return HttpResponse("Hello, Alias!")


# def create(request, obj_alias, obj_target):
def create(request, obj_alias: str, obj_target: str) -> HttpResponse:
    """Create an Alias object with start time from now to the end time None."""
    obj_start_time = timezone.now()
    message = save_with_check(obj_alias, obj_target, obj_start_time)
    return HttpResponse(message)


# def get(request, obj_alias):
def get(request, obj_alias: str) -> HttpResponse:
    """Get aliases target."""
    return get_on_date(request, obj_alias, str(timezone.now()))


def get_on_date(request, obj_alias: str, on_date: str) -> HttpResponse:
    """
    Get aliases target in current time.

    on_date - date when alias must be active.
    """
    cur_on_date = check_date(on_date)
    if isinstance(cur_on_date, datetime):
        alias_obj = Alias.objects.filter(alias=obj_alias, start__lte=on_date, end__gte=on_date)
        if alias_obj.exists():
            return HttpResponse(alias_obj.first().target)
        else:
            return HttpResponse("alias not found")
    else:
        return HttpResponse(cur_on_date)


def aliases(request, alias_target: str, from_datetime: str, to_datetime: str) -> HttpResponse:
    """
    Get aliases by target and period.

    from_datetime, to_datetime - period of alias activity.
    """
    cur_from_datetime = check_date(from_datetime)
    if to_datetime == "None":
        to_datetime = max_system_date
    cur_to_datetime = check_date(to_datetime)
    if isinstance(cur_from_datetime, datetime) and isinstance(cur_to_datetime, datetime):
        alias_obj = Alias.objects.filter(target=alias_target, start=from_datetime, end=to_datetime)
        if alias_obj.exists():
            return HttpResponse(alias_obj.first().alias)
        else:
            return HttpResponse("alias not found")
    else:
        return HttpResponse('check a date format')


def replace(request, existing_alias: str, alias_start: str, new_alias_value: str) -> HttpResponse:
    """
    Replacing an existing alias with a new one at a specific time point.

    alias_start - date when the active alias started. new_alias_value - name of new alias.
    """
    replace_at = timezone.now()
    alias_obj = Alias.objects.filter(alias=existing_alias, start=alias_start)
    alias_obj.update(end=replace_at)
    alias_obj_1 = Alias.objects.filter(alias=existing_alias, start=alias_start)
    message = save_with_check(new_alias_value, alias_obj_1[0].target, alias_obj_1[0].end)
    return HttpResponse(message)


def alias_save(obj_alias: str, obj_target: str, obj_start_time: str, obj_end_time: str):
    """The function that save alias object."""
    alias_obj = Alias.objects.create(alias=obj_alias, target=obj_target,
                                     start=obj_start_time, end=obj_end_time)
    alias_obj.save()


def save_with_check(obj_alias: str, obj_target: str, obj_start_time: str, obj_end_time=max_system_date) -> str:
    """Save alias with checking date overlapping."""
    check2_alias = Alias.objects.filter(alias=obj_alias, end__gte=obj_start_time)
    check1_alias = Alias.objects.filter(alias=obj_alias, start__lte=obj_end_time)
    if (obj_end_time is None and (not check2_alias.exists())) or (
            obj_end_time is not None and (not check1_alias.exists() or not check2_alias.exists())):
        alias_save(obj_alias, obj_target, obj_start_time, obj_end_time)
        return 'alias created'
    else:
        return 'date of new alias overlapping with existing'


def check_date(on_date):
    """Check date format."""
    on_date = on_date.replace("+00:00", "")
    try:
        on_date = datetime.strptime(on_date, '%Y-%m-%d %H:%M:%S.%f')
    except:
        return f'{on_date} is not a date format'
    return on_date
