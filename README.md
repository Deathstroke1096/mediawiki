# mediawiki 1.38.2 installation using blue-green deployment

 What was the requirement?
-> Automate the deployment of mediawiki using CloudFormation Template in AWS


## BEFORE YOU START HERE ARE THINGS YOU MUST FOLLOW
1. Make sure boto3 for python is installed in your system
2. create your vpc in default and default only otherwise the instances created keeps in changing so does your public ip ( this is a must do )
3. Don't forget to have a clean workspace before you start
4. Create user group and user admin and also the key-pair ( my_ec2_key.pem in my case )


## STEPS for creating VPC 
1. Go to your aws console and before you create any vpc go and create a default vpc.
      This vpc will automatically allocate subnets, route tables and internet gateways for that vpc and moreover the instances created will not change. ( this is the most dangerous and iritating problem that i faced while doing this )
      
      ![image](https://user-images.githubusercontent.com/49493062/180637383-744f1479-2fa1-486c-a45a-f9854a0d9640.png)
      
      
## Configure aws in your system first
 1. ```aws configure``` and then insert the acces id and access id secret that you got while creating user admin
 2. check the configurations using -- ```aws configure list```
 3. for my case it shows different
 4. ![image](https://user-images.githubusercontent.com/49493062/180637667-a5fb1edd-d0a5-415c-b506-ebc4f811720f.png)

 
 
      
## now the steps for creating the blue-green stack
1. first find out your vpc id and the subnets ids from the console and the change the values in param.json accordingly
2. you can also change the region and values and the ami value in the blueGreen.yaml template and also the disk size according to your needs 
![image](https://user-images.githubusercontent.com/49493062/180637512-8e23842d-35ee-4778-b8ac-48ab3afce150.png)
3. Now run the command --- ```aws cloudformation create-stack --stack-name blue-green --template-body file://blueGreen.yaml --parameters file://param.json```   for the creating of the CFT stack
![Create-Stack-blue-green](https://user-images.githubusercontent.com/49493062/180637568-5a5a5e25-c78e-4f90-b8c7-9baa8aeac28c.JPG)
4. in the console you get an output like this
5. ![stack-formation](https://user-images.githubusercontent.com/49493062/180637958-686e7c65-e333-4252-acf5-193a3019d00e.JPG)

## create an inventory file before the next step
1. create an inventory file with header as [servers] before going to the next step
2. like this ![image](https://user-images.githubusercontent.com/49493062/180638137-cbf474eb-2b2a-46a6-a08e-5e4c8a5ab2f9.png)


## once the stack is created now run the dynamicInventory.py
1. you can change the values inside the file according to the values you gave in the blueGreen.yaml file 
2. ![image](https://user-images.githubusercontent.com/49493062/180637819-106942a0-8d26-4ea6-a7f7-2e77f103e604.png)
    you can find these values at the very last
3. then run the command ```python3 dynamicinventory.py``` ( or in my case ```python dynamicInventory.py``` because I have already assigned the home variable in my env to Python)
4. then you get an output like this!
5. ![image](https://user-images.githubusercontent.com/49493062/180637948-893c68a2-968e-496d-ba5b-a2ec87af0578.png)

## value inside playbook.yaml
1. If you want to install any other softwere or other version of mediawiki then change the values inside the playbook.yaml


## once this is done then copy the plaaybook.yaml and inventory.txt to /tmp/ansible
1. I did this because ansible was throwing errors continuously while executing.
2. so ```cp inventory.txt /tmp/ansible ```
3. then ```cp playbook.yaml /tmp/ansible ```

![copy-inventory](https://user-images.githubusercontent.com/49493062/180638164-514ffe3b-b8fa-4b79-9c05-22b49afeaad8.JPG)


## then go to /tmp/ansible and perfrom run the playbook
1. ```cd /tmp/ansible```
2. ```ansible-playbbok playbook.yaml -i inventory.txt```
3. you get outputs like this
4. ![ansible-playbook-1](https://user-images.githubusercontent.com/49493062/180638235-109732a7-4945-43ec-b0a6-3a6999739e07.JPG)
![ansible-playbook-2](https://user-images.githubusercontent.com/49493062/180638240-f552b322-520a-4aaf-bb76-f3e0e032d4b2.JPG)
![ansible-playbook-3](https://user-images.githubusercontent.com/49493062/180638243-3ed16da9-42fe-41e6-a2a0-ca262940803e.JPG)


## once the above steps are complete then go to aws console and then the load balancer and the connect using the load balancer to something like this
![mediaWiki-home](https://user-images.githubusercontent.com/49493062/180638286-c7991d91-4e4c-4d34-b2e2-e507ba37aa69.JPG)
![mediaWiki-final](https://user-images.githubusercontent.com/49493062/180638294-363c8ac3-46c8-44e7-9a5e-4bd6c0133165.JPG)



## problems I faced while doing this
1. My biggest priblem was i don't know aws. I know only azure. So i had only very basic knowledge on the components in azure. So I had to learn and do the whole thing within a days time. Biggest achievement so far!
2. I build the project again and again on a differnet vpc and not the default vpc and so my instances kept on changing so my builds kept on failing
3. do not forget to create users first
4. change the values in the json and yaml files accordingly. Please check multiple times before performing the abobe steps.
5. I tried to automate using a shell script ( install.sh ) but could not do because i had to go inside the /tmp/ansible folder again and again

## references i needed
1.Tutorial: Creating a service using a blue/green deployment - Amazon Elastic Container Service![image](https://user-images.githubusercontent.com/49493062/180638695-75b00604-a557-4b15-b80e-1cd30f519904.png)
2.Prerequisites to use the AWS CLI version 2 - AWS Command Line Interface (amazon.com)![image](https://user-images.githubusercontent.com/49493062/180638707-df77edc9-fca8-41c9-b09d-96fad4e2ccaf.png)


Due to time constraint i did what i could. If i had more time then i would have created a jenkins job to automate the whole process.



 



