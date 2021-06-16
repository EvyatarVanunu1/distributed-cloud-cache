# debug
# set -o xtrace

while getopts k:s:b: flag
do
    case "${flag}" in
        k) KEY_NAME=${OPTARG};;
        s) SEC_GRP=${OPTARG};;
        b) BUCKET_NAME=${OPTARG};;
    esac
done


KEY_PEM="$KEY_NAME.pem"

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
    sudo docker build . -t distributed-cloud-cache-orc -f node.dockerfile
    sudo docker run --env-file ~/env_file -p 80:80 -d distributed-cloud-cache-node
    exit
EOF

echo "test that it all worked"
curl  --retry-connrefused --retry 10 --retry-delay 1  http://$PUBLIC_IP:80/health