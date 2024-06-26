import streamlit as st  # Importing the Streamlit library for building web applications
from aws_cost_manager import AWSCostExplorer, CostData  # Importing custom modules for AWS cost management
import plotly.express as px  # Importing Plotly Express for data visualization
from credentials import initialize_aws_session  # Importing a function to initialize AWS session
from datetime import datetime, timedelta  # Importing datetime module for date manipulation

# Initialize cost management
initialize_aws_session()  # Calling the function to initialize AWS session
cost_explorer = AWSCostExplorer()  # Creating an instance of the AWSCostExplorer class
cost_data = CostData(cost_explorer)  # Creating an instance of the CostData class with the cost_explorer instance

st.title('AWS Cloud Services Cost Dashboard')  # Setting the title of the web application

# Sidebar for date range selection
st.sidebar.title("Date Range Selector")  # Setting the title of the sidebar
start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=180))  # Creating a date input widget for selecting the start date
end_date = st.sidebar.date_input("End Date", value=datetime.now())  # Creating a date input widget for selecting the end date

# Convert date_input (date) to datetime at the start of the day for comparison
start_date_datetime = datetime.combine(start_date, datetime.min.time())  # Converting the start date to a datetime object with the time set to the start of the day
end_date_datetime = datetime.combine(end_date, datetime.min.time())  # Converting the end date to a datetime object with the time set to the start of the day

if start_date >= end_date:
    st.sidebar.error("Start date must be before end date.")  # Displaying an error message if the start date is greater than or equal to the end date

# Display Cost Cards
# Display streamlit metrics in a single row
colCard1, colCard2, colCard3 = st.columns(3)  # Creating three columns for displaying cost metrics
colCard1.metric("Current Month Estimated Bill", f"${cost_data.get_estimated_current_month_bill():,.2f}")  # Displaying the current month's estimated bill
colCard2.metric("Last Month Billed Cost", f"${cost_data.get_last_month_cost():,.2f}")  # Displaying the last month's billed cost
colCard3.metric("Total Cost of Selected Months", f"${cost_data.get_total_cost_selected_months(start_date_datetime, end_date_datetime):,.2f}")  # Displaying the total cost of the selected months

# Display Monthly Cost Data
monthly_data = cost_data.fetch_monthly_costs(start_date=start_date_datetime, end_date=end_date_datetime)  # Fetching the monthly cost data for the selected date range
fig = px.bar(monthly_data, x='Month', y='Cost', color='Service', title='Cost Breakdown by Service Over the Selected Date Range')  # Creating a bar chart using Plotly Express
st.plotly_chart(fig, use_container_width=True)  # Displaying the bar chart in the web application

# Display Pie charts in a single row
colPie1, colPie2 = st.columns(2)  # Creating two columns for displaying pie charts
current_month_data = cost_data.fetch_monthly_costs(start_date=start_date_datetime, end_date=end_date_datetime, months=1)  # Fetching the monthly cost data for the current month
fig_pie = px.pie(current_month_data, values='Cost', names='Service', title='Service Cost Distribution This Month')  # Creating a pie chart for the current month
colPie1.plotly_chart(fig_pie, use_container_width=True)  # Displaying the pie chart in the first column

# Pie chart for the current year
current_year_data = cost_data.fetch_monthly_costs(start_date=start_date_datetime, end_date=end_date_datetime, months=12)  # Fetching the monthly cost data for the current year
fig_pie = px.pie(current_year_data, values='Cost', names='Service', title='Service Cost Distribution This Year')  # Creating a pie chart for the current year
colPie2.plotly_chart(fig_pie, use_container_width=True)  # Displaying the pie chart in the second column
