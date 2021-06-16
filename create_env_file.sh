while getopts s:b flag
do
    case "${flag}" in
        s) SERVER_URL=${OPTARG};;
        b) BUCKET_NAME=${OPTARG};;
    esac
done


echo "AWS_DEFAULT_REGION=`aws configure get region`" >> env_file
echo "AWS_ACCESS_KEY_ID=`aws configure get aws_access_key_id`" >> env_file
echo "AWS_SECRET_ACCESS_KEY=`aws configure get aws_secret_access_key`" >> env_file
echo "SERVER_URL=${SERVER_URL}"
echo "S3_BUCKET_NAME=${BUCKET_NAME}"
