import asyncio

from celery import shared_task

from utils.parser import main
from fuel import models


@shared_task()
def update_data(date):
    print('Start task update data')
    try:
        asyncio.get_event_loop().run_until_complete(main())
        status = models.UpdateDatabase.objects.filter(run_date=date).first()
        status.status = 'Done'
        status.save()
    except Exception as error:
        print(error)
    print('End task')
    return True
