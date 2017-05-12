from __future__ import unicode_literals

import re
import warnings
import collections

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def truncate_middle(max_len, message, truncate_message='...'):
    if message and max_len and len(message) > max_len:
        subsize = int((max_len - len(truncate_message)) / 2)
        message = message[0:subsize] + truncate_message + message[-subsize:]
    return message


class CimiResource(object):

    # _attributes_names = ['id', 'resourceURI', 'created', 'updated', 'acl', 'name', 'description', 'properties', 'operations']

    def __init__(self, json):
        self.json = json
        self._attributes_names = []
        self.extract_and_set_attributes()
        self.operations_by_name = self.get_operations_by_name()

    def get_operations_by_name(self):
        operations = self.json.get('operations', [])
        return {op['rel']: op for op in operations if 'rel' in op}

    def extract_and_set_attributes(self):
        for key, value in list(self.json.items()):
            name = camel_to_snake(key)
            if hasattr(self, name):
                warnings.warn('Cannot set attribute "{}" because it is already set'.format(name), RuntimeWarning)
            else:
                setattr(self, name, value)
                self._attributes_names.append(name)

    def __str__(self):
        data = ['{}: {}'.format(attr, truncate_middle(80, str(getattr(self, attr))))
                for attr in self._attributes_names
                if getattr(self, attr, None) is not None]
        return '{}:\n{}'.format(self.__class__.__name__, '\n'.join(sorted(data)))


class CloudEntryPoint(CimiResource):

    # _attributes_names = CimiResource._attributes_names + ['baseURI', 'href']

    def __init__(self, json):
        super(CloudEntryPoint, self).__init__(json)
        self.entry_points = self.extract_entry_points()

    def extract_entry_points(self):
        return {k: v['href'] for k,v in list(self.json.items()) if isinstance(v, dict) and 'href' in v}






App = collections.namedtuple('App', [
    'name',
    'type',
    'version',
    'path',
])

Deployment = collections.namedtuple('Deployment', [
    'id',
    'module',
    'status',
    'started_at',
    'last_state_change',
    'clouds',
    'username',
    'abort',
    'service_url',
    'scalable',
])

Node = collections.namedtuple('Node', [
    'path',
    'name',
    'cloud',
    'multiplicity',
    'max_provisioning_failures',
    'network',
    'cpu',
    'ram',
    'disk',
    'extra_disk_volatile',
])

VirtualMachine = collections.namedtuple('VirtualMachine', [
    'id',
    'cloud',
    'status',
    'deployment_id',
    'deployment_owner',
    'node_name',
    'node_instance_id',
    'ip',
    'cpu',
    'ram',
    'disk',
    'instance_type',
    'is_usable',
])

Usage = collections.namedtuple('Usage', [
    'cloud',
    'run_usage',
    'vm_usage',
    'inactive_vm_usage',
    'others_vm_usage',
    'pending_vm_usage',
    'unknown_vm_usage',
    'quota',
])

Module = collections.namedtuple('Module', [
    'name',
    'type',
    'created',
    'modified',
    'description',
    'version',
    'path',
])

User = collections.namedtuple('User', [
    'username',
    'cyclone_login',
    'github_login',
    'email',
    'first_name',
    'last_name',
    'organization',
    'roles',
    'configured_clouds',
    'default_cloud',
    'ssh_public_keys',
    'keep_running',
    'timeout',
    'privileged',
])

