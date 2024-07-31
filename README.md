# bikes_rental

## Deployment and customization

1. Repository cloning

Clone the project and navigate to the project root 
```
git clone https://github.com/Alangard/bikes_rental.git
cd bikes_rental
```

2. Registering and configuring AWS S3

* Register or log in to the AWS Management Console.
* Go to S3 Service and create a new bucket.
* Go to IAM and create a new user with access to S3:
* Create a group with the AmazonS3FullAccess policy.
* Create a user and add it to the group.
* Save the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY_ID and the name of the bucket.

3. setting environment variables
Create a `.env` folder in the project root and inside it a `.env.dev` file, add the following variables to the file by replacing `your_secret_key`, `your_bd_name`, `your_bd_username`, `your_bd_pass`, `your_aws_access_key_id`, `your_aws_secret_access_key`, `your_s3_bucket_name` with your values :

```
SECRET_KEY=your_secret_key
DEBUG=1
PROD=0
DEV=1
TEST=0
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_NAME=your_bd_name
POSTGRES_USER=your_bd_username
POSTGRES_PASSWORD=your_bd_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
```

4. Creating SSH keys and setting up the VPS
 * On your local machine, create SSH keys (if you don't already have them) by replacing `your_email@example.com` with an identifying comment:
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
* Save the keys and add the public key to your VPS server in `~/.ssh/authorized_keys` file.

* Log in to your VPS and install Docker and Docker Compose:

```
sudo apt update
sudo apt install docker.io
sudo apt install docker-compose
```

* Make sure that Docker and Docker Compose are running:

```
sudo systemctl start docker
sudo systemctl enable docker
docker --version
docker-compose --version
```

5. Customizing GitLab CI/CD
* Bring your project to your Gitab account
* Go to your project on GitLab and open the CI/CD settings.
* Add the following secrets to the CI / CD > Variables section:
* Make sure that Docker and Docker Compose are running:

```
SECRET_KEY - A key used for cryptographic signing in Django applications. 
ALLOWED_HOSTS - A list of host/domain names that Django is allowed to serve. 
POSTGRES_ENGINE - The database engine used by Django, typically set to django.db.backends.postgresql for PostgreSQL 
POSTGRES_NAME - The name of the PostgreSQL database to connect to.
POSTGRES_USER - The username for authenticating with the PostgreSQL database.
POSTGRES_PASSWORD - The password for the PostgreSQL database user.
POSTGRES_HOST - The hostname or IP address of the PostgreSQL database server.
POSTGRES_PORT - The port number on which the PostgreSQL database server is listening, usually 5432.
REDIS_URL - The URL for connecting to the Redis server, used for caching and other purposes.
CELERY_BROKER_URL - The URL for the message broker used by Celery.
CELERY_RESULT_BACKEND - The URL or backend for storing Celery task results.
AWS_ACCESS_KEY_ID - The access key ID for AWS services, required to authenticate with AWS.
AWS_SECRET_ACCESS_KEY - The secret access key for AWS services, used in conjunction with the access key ID.
AWS_STORAGE_BUCKET_NAME - The name of the S3 bucket used for storing static files and other assets on AWS.
CI_REGISTRY_USER - The username used to authenticate with the container registry in CI/CD pipelines.
CI_REGISTRY_PASSWORD - The password or token used to authenticate with the container registry in CI/CD pipelines.
CI_REGISTRY - The URL of the container registry where Docker images are pushed and pulled.
CI_PIPELINE_IID - A unique identifier for the current CI/CD pipeline.
DOMAIN_NAME - The domain name of the server where the application will be deployed.
SERVER_USERNAME - The username used to SSH into the server for deployment or other administrative tasks.
```

The pipeline will only run if the branch being modified is called main

## Local startup
1. Starting Docker Compose for development
To start the project in development mode, use:
```
docker-compose -f docker-compose.dev.yml up --build
```
2. Run tests
```
docker-compose -f docker-compose.testing.yml up --build
docker exec -it DjangoAPI pytest
```
3. Run in production

```
docker-compose -f docker-compose.prod.yml up --build
```


## Sample requests
See the chemas on: http://{your_domain_name}/api/docs/ 