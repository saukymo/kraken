"""Apschedular config file."""


class Config(object):
    """Schedular config."""

    JOBS = [
        {
            'id': 'cronjob',
            'func': 'app:cron_job',
            'trigger': 'cron',
            'minute': '*/5',
        }
    ]

    SCHEDULER_TIMEZONE = 'UTC'
    SCHEDULER_API_ENABLED = True
