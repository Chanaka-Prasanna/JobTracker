import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter
import io

class StatsManager:
    def __init__(self, jobs_data, settings_manager):
        self.jobs_data = jobs_data
        self.settings_manager = settings_manager
        
    def get_basic_stats(self):
        """Get basic statistics about applications"""
        if not self.jobs_data:
            return {
                'total_applications': 0,
                'unique_companies': 0,
                'applications_by_role': {},
                'daily_rate': 0,
                'total_days': 0
            }
            
        df = pd.DataFrame(self.jobs_data)
        
        # Handle missing dates and roles
        if 'applied_date' not in df.columns:
            df['applied_date'] = datetime.now().strftime('%Y-%m-%d')
        if 'role' not in df.columns:
            df['role'] = 'Not Specified'
            
        # Convert date strings to datetime
        df['applied_date'] = pd.to_datetime(df['applied_date'])
        
        # Calculate statistics
        total_applications = len(df)
        unique_companies = len(df['company'].unique())
        applications_by_role = dict(Counter(df['role']))
        
        # Calculate daily rate
        if len(df) > 0:
            date_range = (df['applied_date'].max() - df['applied_date'].min()).days + 1
            daily_rate = total_applications / max(date_range, 1)
        else:
            daily_rate = 0
        
        return {
            'total_applications': total_applications,
            'unique_companies': unique_companies,
            'applications_by_role': applications_by_role,
            'daily_rate': round(daily_rate, 2),
            'total_days': date_range
        }
    
    def generate_daily_applications_plot(self):
        """Generate a plot of daily applications"""
        if not self.jobs_data:
            return None
            
        df = pd.DataFrame(self.jobs_data)
        df['applied_date'] = pd.to_datetime(df['applied_date'])
        
        # Create date range from first to last application
        date_range = pd.date_range(
            start=df['applied_date'].min(),
            end=df['applied_date'].max(),
            freq='D'
        )
        
        # Count applications per day
        daily_counts = df.groupby('applied_date').size().reindex(date_range, fill_value=0)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(daily_counts.index, daily_counts.values, marker='o')
        plt.title('Daily Job Applications')
        plt.xlabel('Date')
        plt.ylabel('Number of Applications')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
    
    def generate_roles_pie_chart(self):
        """Generate a pie chart of applications by role"""
        if not self.jobs_data:
            return None
            
        df = pd.DataFrame(self.jobs_data)
        role_counts = df['role'].value_counts()
        
        plt.figure(figsize=(10, 8))
        plt.pie(role_counts.values, labels=role_counts.index, autopct='%1.1f%%')
        plt.title('Applications by Role')
        plt.axis('equal')
        
        # Save plot to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf
    
    def get_weekly_stats(self):
        """Get weekly application statistics"""
        if not self.jobs_data:
            return []
            
        df = pd.DataFrame(self.jobs_data)
        df['applied_date'] = pd.to_datetime(df['applied_date'])
        
        # Group by week and count
        weekly_stats = df.groupby(pd.Grouper(key='applied_date', freq='W')).size()
        
        return [
            {
                'week': week.strftime('%Y-%m-%d'),
                'count': int(count)
            }
            for week, count in weekly_stats.items()
        ]
    
    def get_company_stats(self):
        """Get statistics about companies applied to"""
        if not self.jobs_data:
            return []
            
        df = pd.DataFrame(self.jobs_data)
        company_stats = df.groupby('company').agg({
            'role': 'count',
            'applied_date': 'max'
        }).reset_index()
        
        company_stats.columns = ['company', 'applications', 'last_application']
        company_stats = company_stats.sort_values('applications', ascending=False)
        
        return company_stats.to_dict('records')
