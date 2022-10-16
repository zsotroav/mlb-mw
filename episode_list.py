from apscheduler.schedulers.blocking import BlockingScheduler
from episode_updater import episode_update, Mode
import datetime


# Moved stuff out to diferentiate the script and the episode list

SPOILER = "Miraculous Ladybug Wiki:Spoiler Doctrine"
sched = BlockingScheduler()

sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 18, 00, 30, 00), args=['Destruction',
                                                                                       'Destruction',
                                                                                       Mode.WW])
sched.start()