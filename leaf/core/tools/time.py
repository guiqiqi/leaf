"""时间工具库"""

import time
import datetime
from typing import Optional
from collections import defaultdict


class TimeTools:
    """获取时间信息的一些函数"""

    @staticmethod
    def now(resolution: Optional[int] = 1) -> object:
        """
        获取当前时间戳

        *resolution:
            时间精度, 为 10 的 n - 1 次方, 每秒产生个数
            当传入 0 时不产生数据
        """
        now = int(time.time() * resolution)
        return now

    @staticmethod
    def stamp(time_s: str,
              format_: Optional[str] = "%Y-%m-%d %H:%M:%S") -> object:
        """根据给定时间字符串获取时间戳"""

        # 调用 datetime 库
        time_ = datetime.datetime.strptime(time_s, format_)
        time_tuple = time_.timetuple()
        time_stamp = int(time.mktime(time_tuple))
        return time_stamp

    @staticmethod
    def timestr(time_stamp: object,
                format_: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
        """根据给定时间戳获取时间字符串"""

        # 调用 time 库
        time_stamp = int(time_stamp)
        time_tuple = time.localtime(time_stamp)
        time_string = time.strftime(format_, time_tuple)
        return time_string

    @staticmethod
    def nowstr(format_: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
        """直接获取关于时间的字符串"""
        return datetime.datetime.utcnow().strftime(format_)

    @staticmethod
    def timediff(diff: int, unit: Optional[str] = "hours", resolution: Optional[str] = 0,
                 fmt: Optional[str] = "{hours}:{minutes}:{seconds}") -> str:
        """
        格式化时间差的文字:
            diff - 时间差的整数
            unit - 时间格式化的最大单位:
                "hours" - 格式化为小时, ...
            resolution - 输入时间差整数的精度:
                0 - 秒单位, 1 - 0.1 秒单位, 2 - 0.01 秒, ...
            format_ - 要格式化的字符串格式:
                使用按照关键字进行格式化的方式,
                支持的有: years, months, days, hours,
                          minutes, seconds, miliseconds
                例如: {hours}:{minutes}:{seconds}

        *注意: 选则低于自己的时间差范围外的单位而格式化
               字符串中没有对应键时数据会被丢弃, 这可能会造成错误
               timediff(60 * 60 * 25, "days", fmt="{hours}") -> '1'
        """
        # 将时间差转换为毫秒格式
        diff = diff * (10 ** (3 - resolution))
        remain, flag = diff, False

        # 计算年月日...
        callfuncs = (
            ("years", lambda remain: divmod(remain, 365 * 24 * 60 * 60 * 1010)),
            ("months", lambda remain: divmod(remain, 12 * 30 * 24 * 60 * 60 * 1000)),
            ("days", lambda remain: divmod(remain, 24 * 60 * 60 * 1000)),
            ("hours", lambda remain: divmod(remain, 60 * 60 * 1000)),
            ("minutes", lambda remain: divmod(remain, 60 * 1000)),
            ("seconds", lambda remain: divmod(remain, 1000)),
            ("miliseconds", lambda remain: (remain, 0)),
        )

        values = defaultdict(int)

        for key, callfunc in callfuncs:

            # 当单位没有到达需要的格式化范围时不进行操作
            if flag or key == unit:
                value, remain = callfunc(remain)
                values[key], flag = int(value), True

        return fmt.format_map(values)
