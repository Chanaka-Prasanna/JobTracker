from datetime import datetime
from collections import Counter

class StatsManager:
    def __init__(self, jobs_data, settings_manager):
        self.jobs_data = jobs_data
        self.settings_manager = settings_manager

    def get_basic_stats(self):
        if not self.jobs_data:
            return {
                'total_applications': 0,
                'unique_companies': 0,
                'applications_by_role': {},
                'daily_rate': 0.0,
                'total_days': 0,
            }

        total_applications = len(self.jobs_data)
        unique_companies = len({j.get('company', '').strip() for j in self.jobs_data if j.get('company')})

        roles = [j.get('role', 'Not Specified') or 'Not Specified' for j in self.jobs_data]
        applications_by_role = dict(Counter(roles))

        # Parse dates and compute daily rate
        dates = []
        for j in self.jobs_data:
            d = j.get('applied_date')
            if not d:
                continue
            try:
                # Accept ISO format or YYYY-MM-DD
                dt = datetime.fromisoformat(d) if 'T' in d else datetime.strptime(d, '%Y-%m-%d')
                dates.append(dt.date())
            except Exception:
                continue

        if dates:
            days = (max(dates) - min(dates)).days + 1
            total_days = max(days, 1)
            daily_rate = round(total_applications / total_days, 2)
        else:
            total_days = 0
            daily_rate = 0.0

        return {
            'total_applications': total_applications,
            'unique_companies': unique_companies,
            'applications_by_role': applications_by_role,
            'daily_rate': daily_rate,
            'total_days': total_days,
        }
