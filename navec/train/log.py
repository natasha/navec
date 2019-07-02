
from __future__ import print_function

import sys
from datetime import datetime


def log_info(format, *args):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, format % args, file=sys.stderr)
