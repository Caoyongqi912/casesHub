if __name__ == '__main__':
    import os
    os.system(" celery -A celery_task.tasks:celery  worker -l info -P eventlet")
