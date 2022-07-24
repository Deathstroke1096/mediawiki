echo "Create stact"
aws cloudformation create-stack --stack-name blue-green --template-body file://blueGreen.yaml --parameters file://param.json

echo "Cretae inventory"
python3 dynamicInventory.py 

echo "Run playbook"
ansible-playbook playbook.yaml -i invertory.txt