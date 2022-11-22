import boto3


class EC2(object):
    def __init__(self, credential: dict):
        self.client = boto3.client('ec2', aws_access_key_id=credential['aws_access_key_id'],
                                   aws_secret_access_key=credential['aws_secret_access_key'],
                                   region_name=credential['region'])

    def update_ec2_tags(self, instance_id: str, tags: dict, is_override: False):
        tags_list = []
        for key, value in tags.items():
            tags_list.append({'Key': key, 'Value': value or ' '})
        if not is_override:
            response = self.client.describe_instances(InstanceIds=[instance_id])
            exist_tags = response['Reservations'][0]['Instances'][0]['Tags']
            if exist_tags:
                tag_keys = [tag['Key'] for tag in exist_tags]
                for key in tag_keys:
                    tags_list = list(filter(lambda i: i['Key'] != key, tags_list))
        if tags_list:
            self.client.create_tags(Resources=[instance_id], Tags=tags_list)
