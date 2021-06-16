# distributed-cloud-cache
## API Routs
### /cache
* Get - /cache/key - return data or None
* Put - /cache/key - req body expecting json {data, expiration_date}
## Command Line Arguments For Create Node
* KEY_NAME - The name of the pem file (name only, without ".pem").
* SEC_GRP - The security group name for the EC2 instances.
* BUCKET_NAME - The S3 Bucket name.
