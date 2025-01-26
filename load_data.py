import os

import boto3
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")
endpoint_url = os.getenv("ENDPOINT_URL")

#credenciais
s3_client = boto3.client('s3',
                         endpoint_url=endpoint_url,
                         aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key)

# Diretório local para salvar as imagens
output_folder = './imagens'
os.makedirs(output_folder, exist_ok=True)

# Contar arquivos na pasta "imagens"
num_files = len(os.listdir(output_folder))
print(f"Número de arquivos na pasta 'imagens': {num_files}")

# Nome do último arquivo baixado
last_downloaded = '20241015004258'

# Configuração do cliente R2 usando boto3
s3_client = boto3.client('s3',
                         endpoint_url=endpoint_url,
                         aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key)

# Listar e baixar todos os arquivos com paginação
continuation_token = None
while True:
    # Pega uma página de resultados
    if continuation_token:
        objects = s3_client.list_objects_v2(Bucket=bucket_name, ContinuationToken=continuation_token)
    else:
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Processar os objetos encontrados na página
    if 'Contents' in objects:
        for obj in objects['Contents']:
            key = obj['Key']
            if key > last_downloaded:
                file_path = os.path.join(output_folder, key)
                try:
                    print(f"Baixando {key} para {file_path}")
                    s3_client.download_file(bucket_name, key, file_path)
                except Exception as e:
                    print(f"Erro ao baixar {key}: {e}")
    
    # Verificar se há mais páginas de resultados
    if objects.get('IsTruncated'):
        continuation_token = objects['NextContinuationToken']
        print("Indo para a próxima página de resultados...")
    else:
        print("Todos os arquivos foram processados.")
        break