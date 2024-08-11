#!/usr/bin/env python3

from fqdn import FQDN
from proxmoxer import ProxmoxAPI
from proxmoxer.tools import Tasks
from tomllib import load as loadtoml
import argparse

parser = argparse.ArgumentParser(description='This script copys the debian template, creates a VM, registers IPs in NETVS and sets CNAME in hosting.de')
parser.add_argument('--fqdn', type=str, required=True, help='fqdn to name VM and register ip addresses')
parser.add_argument('--template', type=str, required=True, help='Name of the template to clone')
parser.add_argument('--cname', type=str, required=True, help='cname in hosting.de for custom DN')
parser.add_argument('--pool', type=str, required=True, help='Resource pool to use for VM')
parser.add_argument('--node', type=str, required=False, help='Node to clone VM to')

args = parser.parse_args()

vm_fqdn = args.fqdn
template_name = args.template
hosting_de_cname = args.cname
resource_pool = args.pool
cluster_node = args.node

if FQDN(vm_fqdn).is_valid is False:
    print("Given FQDN is not a valid FQDN")
    exit(0)

if FQDN(hosting_de_cname).is_valid is False:
    print("Given CNAME is not a valid FQDN")
    exit(0)

with open("config.toml", "rb") as f:
    data = loadtoml(f)

host = data['host']
user = data['user']
realm = data['realm']
token_name = data['token_name']
token_secret = data['token_secret']
verify_ssl = data['verify_ssl']

proxmox_api = ProxmoxAPI(
    host=host,
    user=f'{user}@{realm}',
    token_name=token_name,
    token_value=token_secret,
    verify_ssl=verify_ssl,
)

vms = proxmox_api.cluster.resources.get(type='vm')
template = [vm for vm in vms if vm['name'] == template_name and vm['template'] == 1][0]
template_id = int(template['vmid'])
clone_vm_id = int(proxmox_api.cluster.nextid.get())
if not cluster_node:
    cluster_node = template['node']

clone_task = proxmox_api.nodes(cluster_node).qemu(template_id).clone.create(newid=clone_vm_id, pool=resource_pool)

Tasks.blocking_status(proxmox_api, clone_task)

proxmox_api.nodes(cluster_node).qemu(clone_vm_id).status.start()
