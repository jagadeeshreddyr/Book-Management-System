#!/bin/bash

### sample to setup aws data ##

INSTANCE_ID=$(aws ec2 run-instances --image-id ami-0123456789abcdef --count 1 --instance-type t2.micro --key-name MyKeyPair --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids $INSTANCE_ID

PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

ssh -i "MyKeyPair.pem" ec2-user@$PUBLIC_IP << 'EOF'
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
docker run -d -p 80:80 my-book-management-system
EOF

echo "Application deployed at http://$PUBLIC_IP"
