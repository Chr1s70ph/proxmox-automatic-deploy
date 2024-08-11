# **P**roxmox **A**utomatic **D**eploy (PAD)

PAD is used to completely automate the vm deployment.
It clones a template, configures DNS and deploys a basic ansible playbook.

## Usage

1. 🚗 Copy the config file
```
cp config.example.py config.py
```
2. 🧑🏽‍💻 Set your variables accordingly in `config.py`
3. 🧐 For instructions on how to use PAD check the inbuilt help function
```
./automatic_deploy.py -h
usage: automatic_deploy.py [-h] --fqdn FQDN --template TEMPLATE --cname CNAME --pool POOL [--node NODE]

This script copys the debian template, creates a VM, registers IPs in NETVS and sets CNAME in hosting.de

options:
  -h, --help           show this help message and exit
  --fqdn FQDN          fqdn to name VM and register ip addresses
  --template TEMPLATE  Name of the template to clone
  --cname CNAME        cname in hosting.de for custom DN
  --pool POOL          Resource pool to use for VM
  --node NODE          Node to clone VM to
```
4. 🤑 Profit
