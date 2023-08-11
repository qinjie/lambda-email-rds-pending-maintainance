# Lambda Email RDS Maintaince Actions Alerts

This lambda function pulls the RDS maintainance actions and send emails according to settings in the `.env` file. 

### Pre-requites

1. Sender email address must be verified in the AWS SES.

### Setup
1. Download required libraries in `requirements.txt` into `python` folder
    ```
    pip install -r requirements.txt --target python
    ```
2. Zip the folder content for deployment in Lambda function.
3. Create lambda function using the zip file.
4. Setup necessary environment variables according to `.env` file.
5. Grant lambda execution role with permissions to access RDS and SES.
6. Use Eventbridge to schedule the lambda function to run daily.
