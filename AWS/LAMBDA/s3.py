import boto3

s3 = boto3.client('s3')

# defining default lambda function
def lambda_handler(event,context):
    try: # Getting bucket name from event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        # Getting object key from event 
        object_key = event['Records'][0]['s3']['object']['key']
        # Downloading the object uploaded in the bucket 
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        # Reading data in the object
        
        object_data = response['Body'].read()
        # Putting the object in the another s3 bucket 
        s3.put_object(Bucket='aws.week3.cloudtraining', Key=object_key, Body=object_data)
        print(" SUCCESS : Object successfully placed in bucket aws.week3.cloudtraining ")

        return {
                'statusCode': 200,
                'body': 'Success'
            }
    except Exception as e:
        # Print the error for debugging
        print(f"Error processing event: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': 'Error'
        }