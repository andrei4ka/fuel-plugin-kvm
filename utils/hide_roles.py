#!/usr/bin/python

import sys
import yaml

if len(sys.argv) < 2:
    sys.exit("ERROR: At least one argument is required.")

for file in sys.argv[1:]:
    with open(file, 'r') as f:
        role = yaml.safe_load(f)

    if 'restrictions' not in role['meta']:
        role['meta']['restrictions'] = []

    role['meta']['restrictions'].append({
        'condition': 'settings:fuel-plugin-kvm.metadata.enabled == true',
        'action': 'hide'
    })

    with open(file, 'w') as f:
        yaml.dump(role, f, default_flow_style=False)

