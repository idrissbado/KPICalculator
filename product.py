# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 07:15:36 2024

@author: Idriss Olivier BADO
"""

import pandas as pd

class KPICalculator:
    def __init__(self, df):
        self.df = df

    ### 1. Transaction KPIs ###
    
    def total_transaction_volume(self):
        return self.df['transaction_id'].nunique()

    def total_transaction_value(self):
        return self.df['amount'].sum()

    def successful_transactions(self):
        return self.df[self.df['is_successful'] == True]['transaction_id'].nunique()

    def failed_transactions(self):
        return self.df[self.df['is_successful'] == False]['transaction_id'].nunique()

    def average_transaction_value(self):
        return self.df['amount'].mean()

    def transactions_per_user(self):
        return self.df.groupby('user_id')['transaction_id'].count().mean()

    def transaction_growth_rate(self, period='M'):
        # Group by the specified period (M=month, W=week, etc.)
        return self.df.resample(period, on='date')['transaction_id'].nunique().pct_change()

    ### 2. User Engagement KPIs ###
    
    def active_users(self, period='M'):
        return self.df.resample(period, on='date')['user_id'].nunique()

    def new_user_registrations(self):
        return self.df[self.df['is_new_user'] == True]['user_id'].nunique()

    def user_retention_rate(self, period='M'):
        first_time_users = self.df[self.df['is_new_user'] == True]
        returning_users = self.df[~self.df['is_new_user']]
        retention_rate = (returning_users['user_id'].nunique() / first_time_users['user_id'].nunique()) * 100
        return retention_rate

    def churn_rate(self):
        churned_users = self.df.groupby('user_id').apply(lambda x: (x['date'].max() - x['date'].min()).days)
        churned_users = churned_users[churned_users > 30]  # assuming churn is 30 days of inactivity
        return (len(churned_users) / self.df['user_id'].nunique()) * 100

    def transaction_frequency_per_user(self):
        return self.df.groupby('user_id')['transaction_id'].count().mean()

    ### 3. Revenue KPIs ###
    
    def total_revenue(self):
        return self.df['amount'].sum()

    def revenue_per_transaction(self):
        return self.total_revenue() / self.total_transaction_volume()

    def revenue_growth_rate(self, period='M'):
        return self.df.resample(period, on='date')['amount'].sum().pct_change()

    def revenue_per_user(self):
        return self.total_revenue() / self.df['user_id'].nunique()

    ### 4. Operational Efficiency KPIs ###
    
    def transaction_processing_time(self):
        # Assuming you have a 'processing_time' column
        return self.df['processing_time'].mean()

    def error_rate(self):
        return (self.failed_transactions() / self.total_transaction_volume()) * 100

    def cost_per_transaction(self, cost_column='cost'):
        return self.df[cost_column].mean()

    def fraud_rate(self):
        return (self.df[self.df['is_fraud'] == True]['transaction_id'].nunique() / self.total_transaction_volume()) * 100

    def dispute_resolution_time(self):
        return self.df['support_response_time'].mean()

    ### 5. Customer Experience KPIs ###
    
    def net_promoter_score(self, nps_column='nps'):
        promoters = len(self.df[self.df[nps_column] >= 9])
        detractors = len(self.df[self.df[nps_column] <= 6])
        return ((promoters - detractors) / self.df[nps_column].count()) * 100

    def customer_satisfaction_score(self, csat_column='csat'):
        return self.df[csat_column].mean()

    def average_support_response_time(self):
        return self.df['support_response_time'].mean()

    def customer_effort_score(self, ces_column='ces'):
        return self.df[ces_column].mean()

    ### 6. Geographical KPIs ###
    
    def transactions_per_region(self):
        return self.df.groupby('country')['transaction_id'].nunique()

    def user_growth_per_region(self):
        return self.df.groupby('country')['user_id'].nunique()

    def revenue_per_region(self):
        return self.df.groupby('country')['amount'].sum()

    ### 7. Product-Specific KPIs ###
    
    def feature_usage_rate(self, feature_column):
        return self.df.groupby(feature_column)['transaction_id'].nunique()

    def adoption_of_new_features(self, new_feature_column):
        return self.df[self.df[new_feature_column] == True]['user_id'].nunique()

    ### Summary Report ###
    
    def summary_report(self):
        """Generate a summary report of all KPIs."""
        report = {
            "Total Transaction Volume": self.total_transaction_volume(),
            "Total Transaction Value": self.total_transaction_value(),
            "Successful Transactions": self.successful_transactions(),
            "Failed Transactions": self.failed_transactions(),
            "Average Transaction Value": self.average_transaction_value(),
            "Transactions Per User": self.transactions_per_user(),
            "Active Users (Monthly)": self.active_users(),
            "Total Revenue": self.total_revenue(),
            "Revenue Per Transaction": self.revenue_per_transaction(),
            "Error Rate": self.error_rate(),
            "Fraud Rate": self.fraud_rate(),
            "Transactions Per Region": self.transactions_per_region().to_dict(),
            "Revenue Per Region": self.revenue_per_region().to_dict()
        }
        return report

# Usage:
# Assuming you have a dataset (e.g., wave_data.csv) with the relevant columns.
df = pd.read_csv("wave_data.csv")
df['date'] = pd.to_datetime(df['date'])  # Ensure date column is in datetime format

# Initialize the KPI Calculator
kpi_calculator = KPICalculator(df)

# Example of generating a summary report
report = kpi_calculator.summary_report()
print(report)
