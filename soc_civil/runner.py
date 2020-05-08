import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))


        # [
        #     'scrapy',
        #     'crawl',
        #     'clutch_developers',
        #     '-o',
        #     'out.json',
        #     '-L',
        #     'INFO'
        # ]

try:
    execute(
        [
            'scrapy',
            'crawl',
            'organizaciones',
            '-o',
            'org.csv'
        ]
    )
except SystemExit:
    pass