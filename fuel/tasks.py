from pathlib import Path

from django.utils import timezone

from celery import shared_task
from subprocess import call
from fuel import models


@shared_task()
def update_data(date):
    print('Start task update data')
    file_dir = str(Path(__file__).resolve().parent.parent) + '/utils/parser.py'
    try:
        call(["python3", file_dir])
        status = models.UpdateDatabase.objects.filter(run_date=date).first()
        status.status = 'Done'
        status.save()
    except Exception as error:
        print(error)
    print('End task')
    return True


@shared_task()
def update_data_auto():
    print('Start task update data auto')
    now_date = timezone.now().date()
    get_run_date = models.UpdateDatabase.objects.order_by('-run_date').first()
    if not get_run_date or now_date > get_run_date.run_date:
        try:
            id_task = update_data.delay(str(now_date))
            task = models.UpdateDatabase(
                id_task=id_task,
                run_date=now_date,
                status='Auto start update'
            )
            task.save()
            print('Send to the celery')
        except Exception as msg:
            print(f'Error! {msg}')
    else:
        print('Already update')