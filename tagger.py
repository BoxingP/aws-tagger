import json
import os.path

from ec2 import EC2


def main():
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file, 'r', encoding='UTF-8') as file:
        config = json.load(file)
    for resource in config['aws']:
        ec2 = EC2(resource['credential'])
        for instances in resource['instance']:
            for instance_id in instances['id']:
                ec2.update_ec2_tags(instance_id, resource['tags'], is_override=True)
                ec2.update_ec2_tags(instance_id, instances['tags'], is_override=True)


if __name__ == "__main__":
    main()
