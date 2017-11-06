## Requirements:
    python 2.7, pip

## I. Create a virtual environment

    a) install virtualenv package
        $ pip install virtualenv
        
    b) Create virtual enviroment
        $ virtualenv pg_venv
        A directory named pg_venv now exists inside PGIT_exercise_1

    c) Activate virtual enviroment
        $ source pg_venv/bin/activate (Unix)
        $ pg_venv\Scripts\activate (Windows)

        After that you should see the name of virtual enviroment (pg_venv) in the left side of terminal
        The virtual environment can be deactivated at any time by typing deactivate or closing the terminal/

## II.  Install dependencies
    Make sure that you have activated virtual environment pg_venv.
    $ pip install flask-ask zappa requests awscli boto3 wapy

## III. Configure AWS enviroment
    The first step in preparing for deployment is creating an AWS IAM user.
    1. Open the IAM Console. https://console.aws.amazon.com/iam/home#/home
    2. In the navigation pane, choose Users.
    3. Click the Add User button.
    4. Name the user pg-deploy, choose Programmatic access for the Access type, then click the "Next: Permissions" button.
    5. On the permissions page, click the Attach existing policies directly option.
    6. A large list of policies is displayed. Locate the AdministratorAccess policy, select its checkbox,
    then click the "Next: Review" button.
    7. Finally, review the information that displays, and click the Create User button.
    8. Once the user is created, its Access key ID and Secret access key are displayed (click the Show link next to the Secret access key to unmask it).

## IV Configure AWS credentials locally

    $ aws configure

Follow the prompts to input your Access key ID and Secret access key.
For Default region name, type: us-east-1.
For Default output format accept the default by hitting the Enter key.


## V  Deploy the skill with Zappa
    $ cd demo_other_api

    create a zappa configuration file by typing:

    $ zappa init

    deploy project to AWS lambda

    $ zappa deploy dev

    update project

    $ zappa update dev

    After deploying or updating, Zappa outputs the URL your skill is hosted at.
    
## Bibliography:

    1) Amazon Alexa, https://developer.amazon.com/alexa
    2) New Alexa Tutorial: Deploy Flask-Ask Skills to AWS Lambda with Zappa, https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa
    3) Google Developers Youtube Api https://developers.google.com/youtube/v3/
    4) Facebook Graph API, https://developers.facebook.com/docs/graph-api/
    5) Twitter Developers, https://developer.twitter.com/en/docs
    6) Flask-ask repository, https://github.com/johnwheeler/flask-ask
    7) Amazon DynamoDB, https://aws.amazon.com/dynamodb/
    8) Amazon EC2, https://aws.amazon.com/ec2/
    9) Amazon RDS, https://aws.amazon.com/rds/
    10) Amazon S3, https://aws.amazon.com/s3/
    11) Boto3 - AWS SDK for Python, https://github.com/boto/boto3
    12) Zappa: Serverless Python Web Services, https://github.com/Miserlou/Zappa
