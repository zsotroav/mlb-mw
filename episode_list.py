from apscheduler.schedulers.blocking import BlockingScheduler
from episode_updater import episode_update
import datetime


# Moved stuff out to diferentiate the script and the episode list

SPOILER = "Miraculous Ladybug Wiki:Spoiler Doctrine"
sched = BlockingScheduler()

sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 8, 14, 00, 00), args=['Evolution',
                                                                                       'Evolution',
                                                                                       Mode.ENG])
sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 22, 14, 00, 00), args=['Evolution',
                                                                                       'Evolution',
                                                                                       Mode.FULL])

sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 15, 14, 00, 00), args=['Multiplication',
                                                                                       'Multiplication',
                                                                                       Mode.ENG])
#sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 29, 14, 00, 00), args=['Multiplication',
#                                                                                       'Multiplication',
#                                                                                       Mode.ENG])

sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 22, 14, 00, 00), args=['Destruction',
                                                                                       'Destruction',
                                                                                       Mode.ENG])
#sched.add_job(episode_update, 'date', run_date=datetime(2022, 11, 5, 14, 00, 00), args=['Destruction',
#                                                                                       'Destruction',
#                                                                                       Mode.ENG])

#sched.add_job(episode_update, 'date', run_date=datetime(2022, 10, 29, 14, 00, 00), args=['Jubilation',
#                                                                                       'Jubilation',
#                                                                                       Mode.ENG])                                                                                       
#sched.add_job(episode_update, 'date', run_date=datetime(2022, 11, 12, 14, 00, 00), args=['Jubilation',
#                                                                                       'Jubilation',
#                                                                                       Mode.ENG])

sched.start()