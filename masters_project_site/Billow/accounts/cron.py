from .Cloud_utils import*

from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['06:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = take_snapshot_instance()    # a unique code

    def do(self):
        print('test3')

class cronjob_second(CronJobBase):
    RUN_AT_TIMES = ['06:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = get_snapshots()    # a unique code

    def do(self):
        print('test2')


class cronjob_third(CronJobBase):
    RUN_AT_TIMES = ['06:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = sync_aws_cloud()    # a unique code

    def do(self):
        print('test1')

class cronjob_fourth(CronJobBase):
    RUN_AT_TIMES = ['06:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = synch_op_cloud()    # a unique code

    def do(self):
        print('test4')