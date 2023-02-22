from .Cloud_utils import*

from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['06:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = take_snapshot_instance()    # a unique code

    def do(self):
        print('ho')

class cronjob_second(CronJobBase):
    RUN_AT_TIMES = ['06:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = get_snapshots()    # a unique code

    def do(self):
        print('ho')