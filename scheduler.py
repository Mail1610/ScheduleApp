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
            "mo": [],
            "so": [],
            "ao1": [],
            "ao2": [],
            "mi": [],
            "ni1": [],
            "ni2": [],
            "ai": []
        }

        last_day = dates[-1]

        for d in dates:
            used_today = set()

            def pick_once(people, count):
                candidates = [
                    p for p in people
                    if self.can_use(p, d) and p not in used_today
                ]

                if not candidates:
                    candidates = [p for p in people if self.can_use(p, d)]

                if not candidates:
                    return "無人"

                candidates.sort(key=lambda x: (count[x], random.random()))
                p = candidates[0]
                count[p] += 1
                used_today.add(p)
                return p

            data["mo"].append(pick_once(self.outdoor, self.ocount))
            data["so"].append(pick_once(self.outdoor, self.ocount))
            data["ao1"].append(pick_once(self.outdoor, self.ocount))
            data["ao2"].append(pick_once(self.outdoor, self.ocount))

            data["ni1"].append(pick_once(self.indoor, self.icount))
            data["ni2"].append(pick_once(self.indoor, self.icount))

            if d == dates[0]:
                data["mi"].append(pick_once(self.indoor, self.icount))
            else:
                data["mi"].append("")

            if d.weekday() == 4 or d == last_day:
                data["ai"].append(pick_once(self.indoor, self.icount))
            else:
                data["ai"].append("")

        return data