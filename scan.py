import sys
import boto3
import botocore

def main():
    aws_profile = sys.argv[1]
    search_param = sys.argv[2]

    session = boto3.Session(profile_name=aws_profile)
    client = session.client('s3')
    list_buckets_response = client.list_buckets()

    bucket_name_list = []
    for each_bucket in list_buckets_response['Buckets']:
        bucket_name = each_bucket['Name']
        bucket_name_list.append(bucket_name)

    bucket_match_list = []
    for each_bucket in bucket_name_list:
        try:
            bucket_policy = client.get_bucket_policy(Bucket=each_bucket)
        except botocore.exceptions.ClientError:
            print('No policy for bucket %s....skipping' % each_bucket)
            continue
        if search_param in bucket_policy['Policy']:
            bucket_match_list.append(each_bucket)
    print('Matches found in:')
    print(bucket_match_list)

if __name__ == "__main__":
    main()
