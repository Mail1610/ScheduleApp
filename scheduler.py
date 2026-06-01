from datetime import timedelta
from collections import defaultdict
import random


class Scheduler:
    def __init__(self, indoor, outdoor, avoid_map, no_flag=None, no_morning_outdoor=None,
                 half_days=None, no_flag_down=None, no_afternoon_outdoor=None):
        self.indoor = indoor
        self.outdoor = outdoor
        self.avoid = avoid_map

        self.no_flag = set(no_flag or [])
        self.no_morning_outdoor = set(no_morning_outdoor or [])
        self.no_flag_down = set(no_flag_down or [])
        self.no_afternoon_outdoor = set(no_afternoon_outdoor or [])
        self.half_days = set(half_days or [])

        self.icount = defaultdict(int)
        self.ocount = defaultdict(int)

    def can_use(self, name, date, slot=None):
        if name not in self.avoid:
            return True

        key = f"{date.month:02d}/{date.day:02d}"
        excluded = self.avoid[name].get(key, set())

        if not excluded:
            return True
        if slot is None:
            return False
        return slot not in excluded

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

        for idx, d in enumerate(dates):
            used_today = set()
            is_half_day = idx in self.half_days

            def pick_once(people, count, exclude_names=None, allow_repeat=False, slot=None):
                exclude_names = exclude_names or set()

                candidates = [
                    p for p in people
                    if self.can_use(p, d, slot)
                       and p not in exclude_names
                       and (allow_repeat or p not in used_today)
                ]

                if not candidates:
                    candidates = [
                        p for p in people
                        if self.can_use(p, d, slot)
                           and p not in exclude_names
                    ]

                if not candidates:
                    return "無人"

                candidates.sort(key=lambda x: (count[x], random.random()))
                p = candidates[0]
                count[p] += 1

                if not allow_repeat:
                    used_today.add(p)

                return p

            data["mo"].append(
                pick_once(self.outdoor, self.ocount, self.no_morning_outdoor, slot="mo")
            )

            if is_half_day:
                data["so"].append("半天")
            else:
                data["so"].append(
                    pick_once(self.outdoor, self.ocount, slot="so")
                )

            data["ao1"].append(
                pick_once(self.outdoor, self.ocount, self.no_afternoon_outdoor, slot="ao1")
            )
            data["ao2"].append(
                pick_once(self.outdoor, self.ocount, self.no_afternoon_outdoor, slot="ao2")
            )

            if d == dates[0]:
                data["mi"].append(
                    pick_once(self.indoor, self.icount, self.no_flag, slot="mi")
                )
            else:
                data["mi"].append("")

            data["ni1"].append(
                pick_once(self.indoor, self.icount, slot="ni1")
            )
            data["ni2"].append(
                pick_once(self.indoor, self.icount, slot="ni2")
            )

            if d.weekday() == 4 or d == last_day:
                data["ai"].append(
                    pick_once(self.indoor, self.icount, self.no_flag_down, slot="ai")
                )
            else:
                data["ai"].append("")

        return data