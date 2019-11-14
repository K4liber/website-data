import os
import yaml

path_to_config = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'docker-compose.yml'
)

with open(path_to_config, 'r') as yaml_file:
    yaml_config = yaml.load(yaml_file, yaml.Loader)

services = yaml_config['services']
config = dict()
config['db'] = {
    'user': 'root',
    'password': services['db']['environment']['MYSQL_ROOT_PASSWORD'],
    'name': services['api']['container_name'],
    'port': services['db']['ports'][0].split(':')[1],
    'host': services['db']['container_name'],
}
config['redis'] = {
    'host': services['redis']['container_name'],
    'port': services['redis']['ports'][0].split(':')[1]
}
