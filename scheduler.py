from datetime import timedelta
from collections import defaultdict
import random


class Scheduler:
    def __init__(self, indoor, outdoor, avoid_map):
        self.indoor = indoor
        self.outdoor = outdoor
        self.avoid = avoid_map

        self.icount = defaultdict(int)
        self.ocount = defaultdict(int)

    def can_use(self, name, date):
        key1 = f"{date.month}/{date.day}"
        key2 = f"{date.month:02d}/{date.day:02d}"

        return not (
            name in self.avoid and
            (key1 in self.avoid[name] or key2 in self.avoid[name])
        )

    def pick(self, people, date, count):
        c = [p for p in people if self.can_use(p, date)]

        if not c:
            return "無人"

        c.sort(key=lambda x: (count[x], random.random()))
        p = c[0]
        count[p] += 1
        return p

    def generate(self, start, days):
        dates = [start + timedelta(days=i) for i in range(days)]

        data = {
            "dates": dates,
            "mo": [], "so": [], "ao": [],
            "mi": [], "ni": [], "ai": []
        }

        last_day = dates[-1]

        for d in dates:
            # 外勤
            data["mo"].append(self.pick(self.outdoor, d, self.ocount))
            data["so"].append(self.pick(self.outdoor, d, self.ocount))
            data["ao"].append(self.pick(self.outdoor, d, self.ocount))

            # 升旗：只排星期一
            if d == dates[0]:
                data["mi"].append(self.pick(self.indoor, d, self.icount))
            else:
                data["mi"].append("")

            # 中午：每天排
            data["ni"].append(self.pick(self.indoor, d, self.icount))

            # 降旗：星期五，或排班區間最後一天
            if d.weekday() == 4 or d == last_day:
                data["ai"].append(self.pick(self.indoor, d, self.icount))
            else:
                data["ai"].append("")

        return data