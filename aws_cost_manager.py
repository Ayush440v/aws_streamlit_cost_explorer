import boto3
import pandas as pd
from datetime import datetime, timedelta

class AWSCostExplorer:
    def __init__(self):
        self.client = boto3.client('ce')  # Create a Boto3 client for AWS Cost Explorer

    def get_cost_and_usage(self, start_date, end_date, granularity='MONTHLY', metrics=['UnblendedCost'], group_by=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]):
        return self.client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},  # Specify the time period for cost and usage data
            Granularity=granularity,  # Specify the granularity of the data (MONTHLY by default)
            Metrics=metrics,  # Specify the metrics to retrieve (UnblendedCost by default)
            GroupBy=group_by  # Specify the grouping criteria for the data (SERVICE dimension by default)
        )

class CostData:
    def __init__(self, cost_explorer):
        self.cost_explorer = cost_explorer  # Store an instance of AWSCostExplorer

    def fetch_monthly_costs(self, start_date, end_date, months=6):
        response = self.cost_explorer.get_cost_and_usage(
            start_date=start_date.strftime('%Y-%m-%d'),  # Convert start_date to string in 'YYYY-MM-DD' format
            end_date=end_date.strftime('%Y-%m-%d')  # Convert end_date to string in 'YYYY-MM-DD' format
        )
        data = []
        for item in response['ResultsByTime']:  # Iterate over the results for each time period
            for group in item['Groups']:  # Iterate over the groups within each time period
                amount = float(group['Metrics']['UnblendedCost']['Amount'])  # Extract the cost amount
                service = group['Keys'][0]  # Extract the service name
                month = item['TimePeriod']['Start']  # Extract the month of the time period
                if start_date <= datetime.strptime(month, '%Y-%m-%d') <= end_date:  # Check if the month is within the specified range
                    data.append({'Service': service, 'Month': month, 'Cost': amount})  # Add the data to the list
        return pd.DataFrame(data)  # Convert the list of data to a pandas DataFrame

    def get_estimated_current_month_bill(self):
        today = datetime.now()  # Get the current date and time
        start_date = datetime(today.year, today.month, 1)  # Set the start date to the first day of the current month
        end_date = today  # Set the end date to the current date and time
        response = self.cost_explorer.get_cost_and_usage(
            start_date=start_date.strftime('%Y-%m-%d'),  # Convert start_date to string in 'YYYY-MM-DD' format
            end_date=end_date.strftime('%Y-%m-%d'),  # Convert end_date to string in 'YYYY-MM-DD' format
            granularity='DAILY'  # Set the granularity to DAILY
        )
        total_cost = 0
        for item in response.get('ResultsByTime', []):  # Iterate over the results for each time period
            for group in item.get('Groups', []):  # Iterate over the groups within each time period
                total_cost += float(group['Metrics']['UnblendedCost']['Amount'])  # Add the cost amount to the total
        return total_cost  # Return the total cost

    def get_last_month_cost(self):
        today = datetime.now()  # Get the current date and time
        start_date = datetime(today.year, today.month - 1, 1)  # Set the start date to the first day of the previous month
        end_date = datetime(today.year, today.month, 1) - timedelta(days=1)  # Set the end date to the last day of the previous month
        response = self.cost_explorer.get_cost_and_usage(
            start_date=start_date.strftime('%Y-%m-%d'),  # Convert start_date to string in 'YYYY-MM-DD' format
            end_date=end_date.strftime('%Y-%m-%d')  # Convert end_date to string in 'YYYY-MM-DD' format
        )
        total_cost = 0
        for item in response.get('ResultsByTime', []):  # Iterate over the results for each time period
            for group in item.get('Groups', []):  # Iterate over the groups within each time period
                total_cost += float(group['Metrics']['UnblendedCost']['Amount'])  # Add the cost amount to the total
        return total_cost  # Return the total cost

    def get_total_cost_selected_months(self, start_date, end_date):
        selected_months = self.fetch_monthly_costs(start_date, end_date)  # Fetch the monthly costs within the specified range
        total_cost = selected_months['Cost'].sum()  # Calculate the total cost by summing the 'Cost' column
        return total_cost  # Return the total cost
