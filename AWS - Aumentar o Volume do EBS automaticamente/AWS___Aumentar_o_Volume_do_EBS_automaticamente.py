#Teste ForceOne1
import boto3


def lambda_handler(event, context):
    # Obt�m informa��es sobre o EBS
    ebs = boto3.client('ec2').describe_volumes(VolumeIds=[event['VolumeId']])['Volumes'][0]

    # Verifica se o uso do disco est� acima de 90%
    if ebs['State'] == 'in-use' and ebs['Iops'] / ebs['Iops'] >= 0.9:
        # Calcula o novo tamanho do disco, adicionando 10% ao espa�o atual
        size = int(ebs['Size'] * 1.1)

        # Aumenta o tamanho do disco na AWS
        boto3.client('ec2').modify_volume(VolumeId=ebs['VolumeId'], Size=size)

        # Obt�m informa��es sobre a inst�ncia EC2 que o disco est� inserido
        instance = \
        boto3.client('ec2').describe_instances(InstanceIds=[ebs['Attachments'][0]['InstanceId']])['Reservations'][0][
            'Instances'][0]

        # Conecta � inst�ncia EC2 via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(instance['PublicIpAddress'], username=instance['KeyName'])

        # Executa o comando para aumentar o tamanho do disco dentro do sistema operacional
        stdin, stdout, stderr = ssh.exec_command('sudo growpart /dev/xvda 1 && sudo resize2fs /dev/xvda1')

        # Fecha a conex�o SSH
        ssh.close()

## COMO IMPLEMENTAR ##
#1- Crie uma fun��o Lambda na AWS.
#2- Instale a biblioteca Boto3, que � usada para se comunicar com a API da AWS.
#3- Instale a biblioteca Paramiko, que � usada para se conectar � inst�ncia EC2 via SSH.
#4- Copie o c�digo fornecido para a fun��o Lambda criada.
#5- Crie um gatilho para a fun��o Lambda que execute a fun��o de acordo com a sua necessidade (por exemplo, a cada hora).