# AWS Cost Explorer Dashboard

This repository contains the code for a Streamlit-based dashboard that provides visualizations for AWS spending over time. It includes features such as viewing the costs by service in a bar chart, estimated current month's bill, last month's billed cost, and a pie chart breakdown of service utilization for the current year.

## Preliminary Setup

Before using this dashboard, several setup steps are necessary on AWS and in your local environment.

### AWS Configuration

#### 1. Create a New Policy for Cost Explorer Access

To access the AWS Cost Explorer API, you need appropriate permissions. You can either use an existing policy or create a new one.

- **To create a new policy:**
  - Navigate to the IAM (Identity and Access Management) console in your AWS account.
  - Go to Policies and choose Create policy.
  - Select the JSON tab and paste the following policy, which grants access to the necessary Cost Explorer actions:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ce:GetCostAndUsage"
          ],
          "Resource": "*"
        }
      ]
    }
    ```

  - Click on 'Review policy', give it a name, and create the policy.

#### 2. Add a New IAM User and Assign the Policy

- Navigate to the IAM dashboard and select Users.
- Click on Add user and enter a user name.
- Enable Programmatic access and click Next.
- Attach the policy you created by selecting Attach existing policies directly and searching for your newly created policy.
- Review and create the user.
- On the final screen, download the .csv file containing the Access Key ID and Secret Access Key. Keep this file secure, as it will be needed to configure your application.

### Local Environment Setup

#### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone [repository_url]
cd [repository_directory]
```

#### 2. Install Dependencies

The `requirements.txt` file lists all Python libraries that the project depends on. Install them using pip:

`pip install -r requirements.txt`

#### 3. Configure AWS Credentials Locally

For development, you can use the AWS CLI to configure your credentials:

`aws configure`

Enter you Access Key ID, Secret Access Key, and default region when prompted.

### Running the Application

To run the Streamlit application, navigate to the project directory and execute:

`streamlit run app.py`

## Usage

The dashboard allows you to select a date range for displaying AWS costs and provides interactive charts to analyze the data. Ensure your AWS account has Cost Explorer activated and that the dates selected fall within the range of available data.

## Files and Directories

`aws_cost_manager.py`: Contains the logic for fetching data from AWS Cost Explorer.
`app.py`: The main Streamlit application.
`requirements.txt`: Lists the Python dependencies.
`credentials/`: (If applicable) Contains the Python module for AWS credential management for development purposes.