#Teste ForceOne1
import boto3


def lambda_handler(event, context):
    # Obtém informações sobre o EBS
    ebs = boto3.client('ec2').describe_volumes(VolumeIds=[event['VolumeId']])['Volumes'][0]

    # Verifica se o uso do disco está acima de 90%
    if ebs['State'] == 'in-use' and ebs['Iops'] / ebs['Iops'] >= 0.9:
        # Calcula o novo tamanho do disco, adicionando 10% ao espaço atual
        size = int(ebs['Size'] * 1.1)

        # Aumenta o tamanho do disco na AWS
        boto3.client('ec2').modify_volume(VolumeId=ebs['VolumeId'], Size=size)

        # Obtém informações sobre a instância EC2 que o disco está inserido
        instance = \
        boto3.client('ec2').describe_instances(InstanceIds=[ebs['Attachments'][0]['InstanceId']])['Reservations'][0][
            'Instances'][0]

        # Conecta à instância EC2 via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(instance['PublicIpAddress'], username=instance['KeyName'])

        # Executa o comando para aumentar o tamanho do disco dentro do sistema operacional
        stdin, stdout, stderr = ssh.exec_command('sudo growpart /dev/xvda 1 && sudo resize2fs /dev/xvda1')

        # Fecha a conexão SSH
        ssh.close()

## COMO IMPLEMENTAR ##
#1- Crie uma função Lambda na AWS.
#2- Instale a biblioteca Boto3, que é usada para se comunicar com a API da AWS.
#3- Instale a biblioteca Paramiko, que é usada para se conectar à instância EC2 via SSH.
#4- Copie o código fornecido para a função Lambda criada.
#5- Crie um gatilho para a função Lambda que execute a função de acordo com a sua necessidade (por exemplo, a cada hora).