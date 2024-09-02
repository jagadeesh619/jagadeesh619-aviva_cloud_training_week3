import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
import logging

# Set up logging to a file
logging.basicConfig(filename='ec2.log' , level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try :
        client = boto3.client('ec2')

        # Taking input from user
        user_input=input(" Enter the state of instance 'start' or 'stop' : ").strip().lower()

        # checking user provided correct input or not
        if user_input not in ["start","stop"]:

            logger.error("ERROR : invalid input state of instance either 'start' or 'stop' ")
            print("ERROR : invalid input state of instance either 'start' or 'stop'")

            return
        # describing the instance 
        response = client.describe_instances()

        instance_ids=[]
        # Getting all instance from account
        for i in response["Reservations"]:
            for j in i["Instances"]:
                instance_ids.append(j["InstanceId"])

        logger.info(f"Instance-ids : {instance_ids}")
        print(f"Instance-ids : {instance_ids}")

        # starting the instances
        if user_input=="start":
            response_start = client.start_instances(
                InstanceIds=instance_ids
            )


            # waiting instance to get started
            waiter = client.get_waiter('instance_running')
            waiter.wait(InstanceIds=instance_ids)
            print("starting above instance successfully")

            logger.info("starting above instance successfully")

        # stoping the instances 
        elif user_input=="stop":
            response_stop = client.stop_instances(
                InstanceIds=instance_ids
            )
            # waiting instance to get stopped
            waiter = client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=instance_ids)
            logger.info("stopping above instance successfully")
            print("stoppping above instance successfully")

    except ClientError as e:
        # Handle known errors related to AWS services
        print(f"An error occurred: {e.response['Error']['Message']}")
        logger.error(f"An error occurred: {e.response['Error']['Message']}")

    except NoCredentialsError:
        # Handle case where credentials are missing
        print("ERROR: Credentials are missing or not configured properly.")
        logger.error("ERROR: Credentials are missing or not configured properly.")

    except PartialCredentialsError:
        # Handle case where incomplete credentials are provided
        print("ERROR: Incomplete credentials provided. Please check your AWS credentials configuration.")
        logger.error("ERROR: Incomplete credentials provided. Please check your AWS credentials configuration.")

    except Exception as e:
        # Handle any other exceptions
        print(f"ERROR: An unexpected error occurred: {str(e)}")
        logger.error(f"ERROR: An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()