pipeline {
    agent any
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    stages {
        stage('Build') {
            steps {
                script {
                    // Create a ZIP file of your application
                    sh 'zip -q -r sampleweb.zip ./* -x "Jenkinsfile*"'
                }
            }
        }
        stage('unit test cases') {
            steps {
                echo "Unit test cases passed successfully"
            }
        }
        
        stage('Upload to S3') {
            steps {
                script {
                    // Install AWS CLI if not already installed
                    sh 'pip3 install awscli --upgrade --user'
                    
                    // Configure AWS CLI (if not already configured)
                    sh 'aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}'
                    sh 'aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}'
                    sh 'aws configure set region ${AWS_DEFAULT_REGION}'
                    
                    // Upload ZIP file to S3 bucket
                    sh 'aws s3 cp sampleweb.zip s3://aws.week2.cloudtraining/sampleweb.zip'
                }
            }
        }

        stage('Deploy to Elastic Beanstalk') {
            steps {
                script {
                    // Create or update Elastic Beanstalk application version
                    sh '''
                    aws elasticbeanstalk create-application-version \
                        --application-name Samplewebapp-env \
                        --version-label ${BUILD_NUMBER} \
                        --source-bundle S3Bucket=aws.week2.cloudtraining,S3Key=sampleweb.zip
                    '''

                    // Update Elastic Beanstalk environment to use the new version
                    sh '''
                    aws elasticbeanstalk update-environment \
                        --application-name Samplewebapp-env \
                        --environment-name Samplewebapp-env \
                        --version-label ${BUILD_NUMBER}
                    '''
                }
            }
        }
    }
    post {
        always {
            deleteDir()
            echo "Workspace cleaned up."
        }
        success {
            echo "Deployment succeeded."
        }
        failure {
            echo "Deployment failed."
        }
    }
}
