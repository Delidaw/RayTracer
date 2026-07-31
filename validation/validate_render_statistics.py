import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time

from rendering.render_statistics import RenderStatistics

stats = RenderStatistics()

stats.start()

stats.record_capture()
stats.record_capture()

stats.record_disk_hit()

stats.record_background()
stats.record_background()
stats.record_background()

time.sleep(1)

stats.stop()

stats.summary(
    30,
    30
)