import boto3

s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)


try:
    data = open('test_data.txt', 'rb')
    s3.Bucket('dec601').put_object(Key='test_data.txt', Body=data)
except Exception as e:
    print(e)
