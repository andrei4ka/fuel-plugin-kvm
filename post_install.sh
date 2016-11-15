#!/bin/bash

DEBUG=true
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR='/var/www/nailgun/plugins/fuel-plugin-kvm-1.0'   # To do - replace hardcoded plugin name with some better solution
REL_NAME='Ubuntu 14.04'

FUEL='/usr/bin/fuel'
REL=`$FUEL rel | grep -i "${REL_NAME}.* available " | awk '{print $1}'`
FUEL_REL=`$FUEL rel | grep -i "${REL_NAME}.* available " | awk '{print $NF}'`

function set_min_controller_count {
  count=$1
  workdir=$(mktemp -d /tmp/modifyenv.XXXX)
  $FUEL role --rel $REL --role controller --file $workdir/controller.yaml
  sed -i "s/    min: ./    min: ${count}/" $workdir/controller.yaml
  $FUEL role --rel $REL --update --file $workdir/controller.yaml
  rm -rf $workdir
}

function hide_default_roles {
  local tmpdir=$(mktemp -d /tmp/hide_roles.XXXX)
  local def_roles=(compute-vmware compute cinder-vmware virt base-os controller cinder ironic ceph-osd cinder-block-device mongo)

  for role in ${def_roles[@]}; do
    fuel role --rel $REL --role $role --file $tmpdir/${role}.yaml
    grep -q 'fuel-plugin-kvm.metadata.enabled == true' $tmpdir/${role}.yaml
    if [[ $? == 1 ]]; then
      ${DIR}/utils/hide_roles.py $tmpdir/${role}.yaml
      fuel role --rel $REL --update --file $tmpdir/${role}.yaml
    fi
  done
  rm -rf $tmpdir
}

set_min_controller_count 0
hide_default_roles
