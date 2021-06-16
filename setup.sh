# debug
# set -o xtrace

while getopts n flag
do
    case "${flag}" in
        n) NUM_NODES=${OPTARG};;
    esac
done



KEY_NAME="cloud-course-`date +"%s"`"
KEY_PEM="$KEY_NAME.pem"

BUCKET_NAME="s3://distributed_cache_bucket"

echo "creating S3 bucket ${}"
aws s3 mb ${BUCKET_NAME} --profile idc


echo "create key pair $KEY_PEM to connect to instances and save locally"
aws ec2 create-key-pair --key-name $KEY_NAME \
    | jq -r ".KeyMaterial" > $KEY_PEM

# secure the key pair
chmod 400 $KEY_PEM

SEC_GRP="my-sg-`date +'%N'`"

echo "setup firewall $SEC_GRP"
aws ec2 create-security-group   \
    --group-name $SEC_GRP       \
    --description "Access my instances"

# figure out my ip
MY_IP=$(curl ipinfo.io/ip)
echo "My IP: $MY_IP"


echo "setup rule allowing SSH access to $MY_IP only"
aws ec2 authorize-security-group-ingress        \
    --group-name $SEC_GRP --port 22 --protocol tcp \
    --cidr $MY_IP/32

echo "setup rule allowing HTTP (port 80) access to the web"
aws ec2 authorize-security-group-ingress        \
    --group-name $SEC_GRP --port 80 --protocol tcp \
    --cidr 0.0.0.0/0

UBUNTU_20_04_AMI="ami-042e8287309f5df03"

echo "Creating Ubuntu 20.04 instance..."
RUN_INSTANCES=$(aws ec2 run-instances   \
    --image-id $UBUNTU_20_04_AMI        \
    --instance-type t3.micro            \
    --key-name $KEY_NAME                \
    --security-groups $SEC_GRP)

INSTANCE_ID=$(echo $RUN_INSTANCES | jq -r '.Instances[0].InstanceId')

echo "Waiting for instance creation..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

PUBLIC_IP=$(aws ec2 describe-instances  --instance-ids $INSTANCE_ID |
    jq -r '.Reservations[0].Instances[0].PublicIpAddress'
)

URL = "http://${PUBLIC_IP}:80"

echo "New instance $INSTANCE_ID @ $PUBLIC_IP"

echo "deploying config file to production"
/bin/bash create_env_file.sh -s URL -b BUCKET_NAME
scp -i $KEY_PEM -o "IdentitiesOnly=yes" -o "StrictHostKeyChecking=no" -o "ConnectionAttempts=60" env_file ubuntu@$PUBLIC_IP:/home/ubuntu/
rm env_file

echo "setup production environment"
ssh -i $KEY_PEM -o "IdentitiesOnly=yes" -o "StrictHostKeyChecking=no" -o "ConnectionAttempts=10" ubuntu@$PUBLIC_IP <<EOF
    sudo apt update
    sudo apt install git -y
    sudo apt install docker.io -y
    sudo git clone https://github.com/EvyatarVanunu1/distributed-cloud-cache.git
    cd distributed-cloud-cache
    sudo docker build -t distributed-cloud-cache-orc -f orchestrator.dockerfile
    sudo docker run --env-file ~/env_file -p 80:80 -d distributed-cloud-cache-orc
    exit
EOF

echo "test that it all worked"
curl  --retry-connrefused --retry 10 --retry-delay 1  http://$PUBLIC_IP:80/health


for (( c=1; c<=${NUM_NODES}; c++ ))
do
   /bin/bash createNode.sh -s SEC_GRP -b BUCKET_NAME -k KEY_NAME
done