# Ansible Playbook Commands
## Install ansible 
sudo apt install ansible

## ansible secreat password for all

**123456**
## create a new secret with vault
```bash
ansible-vault create xxx.yml
```
## view the secret
```bash
ansible-vault view xxx.yml
```

## Running Ansible Playbook with out Vault
```bash
ansible-playbook -i inventory.ini deploy_xxx.yml
```

## Running Ansible Playbook with Vault
```bash
ansible-playbook -i inventory.ini --vault-id @prompt deploy_xxx.yml
```

## Their is missing a private ssh file relate to the MRC which i won't private in this repo

place your private key and rename with ssh_private to run the scirpt