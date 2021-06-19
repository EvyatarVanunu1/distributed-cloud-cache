# distributed-cloud-cache
## API Routs
### /cache
* Get - /cache/<key> - return data or None
* Put - /cache/<key> - req body expecting ```json {data (type string), expiration_date (formatted as isoformat}```
## Command Line Arguments For Create Node
* KEY_NAME - The name of the pem file (name only, without ".pem").
* SEC_GRP - The security group name for the EC2 instances.
* BUCKET_NAME - The S3 Bucket name.
## Notes
* Do not remove the first EC2 instance - it is the load balancer
