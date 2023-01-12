from django.core.management.base import CommandError, BaseCommand
from django.db import models
from ...tools import convert_data_process

class Command(BaseCommand):
    help = '每日凌晨对当天数据库进行更新'  # command功能作用简介

    def add_arguments(self, parser):  # 用来接收可选参数的( 如果没有参数该方法可以不写 )
        # parser.add_argument('offset', type=int, help='天数转移量')
        parser.add_argument(
            '--convert_data',
            action='store_true',
            dest='convert_data',
            default=False,
            help='convert data'
        )
    
    def handle(self, *args, **options):  # 主处理程序
        convert_data = options['convert_data']
        if convert_data:
            convert_data_process.convert_data_process()