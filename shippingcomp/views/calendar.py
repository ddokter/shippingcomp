from datetime import datetime, date, timedelta
import calendar


class Calendar:

    """ Mixin for calendar function, like 'month' """

    @property
    def year(self):

        """ Return all months """

        today = datetime.now()

        if self.request.GET.get('go', None):

            year = self.request.GET['go']

            now = date(int(year), 1, 1)
        else:
            now = today

        all_days = []
        months = []

        cal = calendar.Calendar()
        
        for mon in range(1, 13):

            days = list(cal.itermonthdates(now.year, mon))
            weeks = []
            week = []

            for idx, val in enumerate(days):
                week.append(val)

                if (idx + 1) % 7 == 0:
                    weeks.append(week)
                    week = []

            months.append({'weeks': weeks, 'title': calendar.month_abbr[mon]})
            all_days.append(days)
            
        return {
            'title': now.strftime("%Y"),
            'days': all_days,
            'today': today,
            'next': now.year + 1,
            'prev': now.year - 1,
            'months': months,
            'year': now.year
            }


    @property
    def month(self):

        """Return current month data, for displaying of the month
        calendar

        """

        today = datetime.now()

        if self.request.GET.get('go', None):

            year, month = self.request.GET['go'].split('-')

            now = date(int(year), int(month), 1)
        else:
            now = today

        if now.month == 12:
            _next = date(now.year + 1, 1, 1)
        else:
            _next = date(now.year, now.month + 1, 1)

        if now.month == 1:
            _prev = date(now.year - 1, 12, 1)
        else:
            _prev = date(now.year, now.month - 1, 1)

        cal = calendar.Calendar()

        days = list(cal.itermonthdates(now.year, now.month))

        weeks = []
        week = []

        for idx, val in enumerate(days):
            week.append(val)

            if (idx + 1) % 7 == 0:
                weeks.append(week)
                week = []

        return {
            'title': now.strftime("%B %Y"),
            'days': days,
            'today': today,
            'weeks': weeks,
            'next': _next.strftime("%Y-%m"),
            'prev': _prev.strftime("%Y-%m"),
            'month': now.month,
            'year': now.year
            }

    @property
    def week(self):

        """ Get the current week """

        now = date.today()
        dates = [now + timedelta(days=i)
                 for i in range(0 - now.weekday(), 7 - now.weekday())]

        return {
            'title': now.isocalendar()[1],
            'days': dates,
            'today': now,
            'month': now.month,
            'year': now.year
            }
