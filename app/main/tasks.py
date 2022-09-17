from celery import shared_task


@shared_task
def clean_data_base():
    """
    method for cleaning database from outdated events
    :return: None
    """
    pass


@shared_task
def parse_new_events():
    """
    method for parsing sites
    :return:
    """
    pass
