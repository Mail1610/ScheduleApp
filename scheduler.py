from datetime import timedelta
from collections import defaultdict
import random


class Scheduler:
    def __init__(self, indoor, outdoor, avoid_map, no_flag=None, no_morning_outdoor=None, half_days=None):
        self.indoor = indoor
        self.outdoor = outdoor
        self.avoid = avoid_map

        self.no_flag = set(no_flag or [])
        self.no_morning_outdoor = set(no_morning_outdoor or [])
        self.half_days = set(half_days or [])

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

        for idx, d in enumerate(dates):
            used_today = set()
            flag_person_today = None
            is_half_day = idx in self.half_days

            def pick_once(people, count, exclude_names=None, allow_repeat=False):
                exclude_names = exclude_names or set()

                candidates = [
                    p for p in people
                    if self.can_use(p, d)
                       and p not in exclude_names
                       and (allow_repeat or p not in used_today)
                ]

                if not candidates:
                    candidates = [
                        p for p in people
                        if self.can_use(p, d)
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

            # 上午外勤：排除「早上不能站外勤」的人
            data["mo"].append(
                pick_once(self.outdoor, self.ocount, self.no_morning_outdoor)
            )

            # 第七節外勤（半天不排）
            if is_half_day:
                data["so"].append("半天")
            else:
                data["so"].append(
                    pick_once(self.outdoor, self.ocount)
                )

            # 下午外勤兩格
            data["ao1"].append(
                pick_once(self.outdoor, self.ocount)
            )
            data["ao2"].append(
                pick_once(self.outdoor, self.ocount)
            )

            # 升旗：每次排班第一天，排除「不能升旗的人」
            if d == dates[0]:
                flag_person_today = pick_once(self.indoor, self.icount, self.no_flag)
                data["mi"].append(flag_person_today)
            else:
                data["mi"].append("")

            # 發資料、寫白板
            # 如果是升旗那個人，允許跟發資料/寫白板重複
            data["ni1"].append(
                pick_once(self.indoor, self.icount, allow_repeat=False)
            )

            data["ni2"].append(
                pick_once(self.indoor, self.icount, allow_repeat=False)
            )

            # 降旗：星期五或最後一天
            if d.weekday() == 4 or d == last_day:
                data["ai"].append(
                    pick_once(self.indoor, self.icount)
                )
            else:
                data["ai"].append("")

        return data