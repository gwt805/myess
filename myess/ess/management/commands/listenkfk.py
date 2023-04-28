from django.core.management.base import BaseCommand
from ...tools import real_time_listen_kfk

class Command(BaseCommand):
    help = '每日凌晨对当天数据库进行更新'  # command功能作用简介

    def add_arguments(self, parser):  # 用来接收可选参数的( 如果没有参数该方法可以不写 )
        # parser.add_argument('offset', type=int, help='天数转移量')
        parser.add_argument(
            '--start_listen_kafka',
            action='store_true',
            dest='listen_kafka',
            default=False,
            help='ess real_time listen kafka'
        )
    
    def handle(self, *args, **options):  # 主处理程序
        convert_data = options['listen_kafka']
        if convert_data:
            real_time_listen_kfk.listen_kafka()