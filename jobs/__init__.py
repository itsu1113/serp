from flask.cli import AppGroup
from jobs.task1 import task1_run
from jobs.task2 import task2_run
from jobs.task_rakuten import task_rakuten_run
from jobs.task_rakuten_spapi import task_rakuten_spapi_run
from jobs.task_yahoo import task_yahoo_run
from jobs.task_au import task_au_run
from jobs.task_edion import task_edion_run
from jobs.task_check_exhibit import task_check_exhibit_run
from jobs.task_get_arari import task_get_arari_run
from jobs.task_rakuten_keyword import task_rakuten_keyword_run
from jobs.task_ipo import task_ipo_run
from jobs.task_tracking import task_tracking_run
from jobs.task_orenor import task_orenor_run
from jobs.task_make_delivery import task_make_delivery_run
from jobs.task_hikari import task_hikari_run
from jobs.task_registration import task_registration_run
from jobs.task_au_1 import task_au_1_run
from jobs.task_kataban_profit import task_kataban_profit_run

# グループを作成
job = AppGroup('job')

# jobsディレクトリ配下にtaskを追加し、以下にも追加する
job.add_command(task1_run)
job.add_command(task2_run)
job.add_command(task_rakuten_run)
job.add_command(task_rakuten_spapi_run)
job.add_command(task_yahoo_run)
job.add_command(task_au_run)
job.add_command(task_edion_run)
job.add_command(task_check_exhibit_run)
job.add_command(task_get_arari_run)
job.add_command(task_rakuten_keyword_run)
job.add_command(task_ipo_run)
job.add_command(task_tracking_run)
job.add_command(task_orenor_run)
job.add_command(task_make_delivery_run)
job.add_command(task_hikari_run)
job.add_command(task_registration_run)
job.add_command(task_au_1_run)
job.add_command(task_kataban_profit_run)
