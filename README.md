# distributed-cloud-cache

## setup.sh
run in order to deploy the system to aws. note that an aws account must 
be configured. 

usage -> ```/bin/bash setup.sh -n <num-nodes>```

## API Routs
### /cache
* Get - /cache/<key> - return JSON {data: <data>} or {}
* Put - /cache/<key> - req body expecting JSON data (type string), expiration_date (formatted as isoformat)}
## Command Line Arguments For Create Node
* KEY_NAME - The name of the pem file (name only, without ".pem").
* SEC_GRP - The security group name for the EC2 instances.
* BUCKET_NAME - The S3 Bucket name.
## Notes
* Do not remove the first EC2 instance - it is the load balancer
