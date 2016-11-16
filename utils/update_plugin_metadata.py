import argparse
import yaml
from fuelclient.objects.environment import Environment

parser = argparse.ArgumentParser(description='Script for check and update plugins')
parser.add_argument('-e', action='store', dest='env',
                    help='Fuel Environment ID')
parser.add_argument('-u', action='store_true', dest='update',
                    help='Update plugins metadata')

args = parser.parse_args()
env = Environment(args.env)
default_attributes = env.get_default_settings_data()
current_attributes = env.get_settings_data()

def dict_merge(dct, default_dct, plugin):
    if isinstance(dct, dict) and isinstance(default_dct, dict):
        for k,v in default_dct.iteritems():
            if k not in dct:
                print "%s key in %s plugin missing and needs to be updated" % (k, plugin)
                dct[k] = default_dct[k]
            elif isinstance(v, dict):
                dict_merge(dct.get(k, {}), v, plugin)
        return dct

for plugin,value in current_attributes['editable'].items():
    try:
        # Update all missing values, buttons for plugins to keep fuel UI up-to date
        if current_attributes['editable'][plugin]['metadata']['class'] == 'plugin':
            current_versions = current_attributes['editable'][plugin]['metadata']['versions'][-1]
            default_versions = default_attributes['editable'][plugin]['metadata']['versions'][-1]
            updated_versions = dict_merge(current_versions, default_versions, plugin)

            current_attributes['editable'][plugin]['metadata']['versions'][-1] = updated_versions
    except KeyError:
        continue

if args.update:
    env.set_settings_data(current_attributes)
