## Amazon S3 e Transcribe
**Objetivo:**  

1. Criar (ou confirmar) sua conta na AWS.  
2. Criar um usuário IAM que será usado pelo **aws‑cli** e conceder permissão apenas para **Amazon Transcribe**, **Amazon Polly** e **Amazon S3**.  
3. Instalar e configurar o **aws‑cli** em um ambiente Linux (ou no Windows Subsystem for Linux – WSL).

> **⚠️ Atenção:** Sempre siga o princípio do menor privilégio (least‑privilege). Conceda ao usuário somente as permissões necessárias para o que você realmente vai usar.

---

## 1️⃣ Criando sua conta na AWS (se ainda não tem)

| Etapa | O que fazer |
|------|--------------|
| 1.1 | Acesse <https://aws.amazon.com/> e clique em **“Create an AWS Account”** (Criar uma conta AWS). |
| 1.2 | Preencha **e‑mail**, **nome da conta**, **senha** e clique em **“Continue”**. |
| 1.3 | Insira **informações de contato** (pessoa física ou empresa). |
| 1.4 | Escolha o **tipo de plano** (Free Tier – gratuito por 12 meses) e continue. |
| 1.5 | **Método de pagamento** – insira um cartão de crédito/débito válido. (A AWS pode cobrar se você ultrapassar o limite gratuito). |
| 1.6 | **Verificação de identidade** – normalmente um código enviado por SMS ou chamada telefônica. |
| 1.7 | **Escolha do suporte** – “Basic” (gratuito) já basta para começar. |
| 1.8 | Aguarde a ativação (pode levar alguns minutos). Quando a página mudar para o **AWS Management Console**, sua conta está pronta. |

> **Dica:** Guarde o e‑mail e a senha em um gerenciador de senhas. Não compartilhe a senha da conta raiz (root) com ninguém.

---

## 2️⃣ Criando um usuário IAM para o aws‑cli

> **Por que não usar a conta raiz?**  
> A conta raiz tem permissões ilimitadas. Usar um usuário IAM com permissões específicas reduz o risco de comprometimento.

### 2.1 Acesse o console IAM

1. No **AWS Management Console**, procure por **IAM** (Identity & Access Management) e clique.  
2. No painel esquerdo, selecione **“Users”** (Usuários) → **“Add user”** (Adicionar usuário).

### 2.2 Defina o usuário

| Campo | Valor recomendado |
|------|--------------------|
| **User name** | `aws-cli-transcribe-polly-s3` (ou outro nome que faça sentido) |
| **Access type** | Marque **“Programmatic access”** (Acesso programático) – isso gera uma *Access Key ID* e *Secret Access Key* que o aws‑cli usará. |
| **Console access** | Opcional – se quiser também login via console, marque e escolha “Custom password”. |

Clique **Next: Permissions**.

### 2.3 Conceda permissões (menor privilégio)

#### Opção 1 – Anexar políticas gerenciadas (mais simples)

Selecione **“Attach existing policies directly”** e procure por:

| Política | O que permite | Por que usar |
|----------|--------------|--------------|
| `AmazonS3FullAccess` (ou `AmazonS3ReadOnlyAccess` se só precisar ler) | Acesso total (ou somente leitura) a todos os buckets S3. | Necessário para armazenar/recuperar arquivos de áudio e transcrições. |
| `AmazonTranscribeFullAccess` | Criação, execução e leitura de jobs de transcrição. | Necessário para usar o Amazon Transcribe. |
| `AmazonPollyFullAccess` | Sintetizar voz, listar vozes, etc. | Necessário para usar o Amazon Polly. |

> **Obs.:** Se quiser restringir ainda mais (ex.: acesso a um bucket específico ou a uma região), crie políticas **customizadas** (ver passo 2.4).

#### Opção 2 – Políticas customizadas (recomendado para produção)

Clique em **“Create policy”** → **JSON** e cole o seguinte (ajuste os ARNs conforme sua necessidade):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3AccessSpecificBucket",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::meu-bucket-transcribe-polly",
                "arn:aws:s3:::meu-bucket-transcribe-polly/*"
            ]
        },
        {
            "Sid": "TranscribeFullAccess",
            "Effect": "Allow",
            "Action": [
                "transcribe:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "PollyFullAccess",
            "Effect": "Allow",
            "Action": [
                "polly:*"
            ],
            "Resource": "*"
        }
    ]
}
```

1. Clique em **“Review policy”**, dê um nome (ex.: `TranscribePollyS3CustomPolicy`) e salve.  
2. Volte à tela de criação de usuário e **procure** a política que acabou de criar. Selecione-a e avance.

### 2.4 Tags (opcional)

Adicione tags como `Project=MeuProjeto` ou `Owner=SeuNome` para facilitar auditoria. Clique **Next: Review**.

### 2.5 Revisar e criar

Revise tudo. Se tudo estiver correto, clique **“Create user”**.

### 2.6 Anote as credenciais

Na tela final, você verá:

- **Access key ID**
- **Secret access key**

> **⚠️ IMPORTANTE:** Salve a *Secret access key* agora – ela não será exibida novamente!  
> Você pode baixar o arquivo CSV ou copiar para um gerenciador de senhas.

---

## 3️⃣ Instalando o AWS CLI (Linux ou WSL)

### 3.1 Pré‑requisitos

| Requisito | Como verificar |
|-----------|----------------|
| **Python 3.7+** (já vem na maioria das distribuições recentes) | `python3 --version` |
| **pip** (gerenciador de pacotes Python) | `pip3 --version` |
| **curl** ou **wget** | `curl --version` ou `wget --version` |

> **Dica:** Se estiver usando WSL, recomendo a distribuição **Ubuntu 22.04 LTS** (ou outra LTS).  

### 3.2 Instalação usando o instalador oficial (recomendado)

```bash
# 1️⃣ Baixe o instalador zip da AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# 2️⃣ Descompacte
unzip awscliv2.zip

# 3️⃣ Instale (pode precisar de sudo)
sudo ./aws/install

# 4️⃣ Verifique a versão
aws --version
```

Saída esperada (exemplo):

```
aws-cli/2.15.6 Python/3.11.9 Linux/5.15.0-1042-aws exe/x86_64.ubuntu.22 prompt/off
```

#### Instalação alternativa (via `pip`)

> **Atenção:** A versão `pip` instala a CLI v1. Para a maioria dos recursos modernos (ex.: S3 Transfer Acceleration, novos parâmetros), use a v2 conforme acima.

```bash
python3 -m pip install --upgrade --user awscli
# Adicione ao PATH se necessário
export PATH=$HOME/.local/bin:$PATH
aws --version
```

### 3.3 Configurando o AWS CLI

Execute o comando interativo:

```bash
aws configure
```

Ele solicitará:

| Prompt | O que colocar |
|--------|----------------|
| **AWS Access Key ID** | *Cole a Access Key ID* que você anotou na etapa 2.6 |
| **AWS Secret Access Key** | *Cole a Secret Access Key* |
| **Default region name** | Ex.: `us-east-1` (ou a região onde você pretende usar Transcribe/Polly/S3) |
| **Default output format** | `json` (padrão) ou `text`/`table` se preferir |

> **Resultado:** As credenciais são gravadas em `~/.aws/credentials` e a configuração regional em `~/.aws/config`.

#### Verificando se tudo está funcionando

```bash
# Testa chamada ao S3 (list buckets)
aws s3 ls

# Testa chamada ao Transcribe (lista jobs – deve retornar vazio)
aws transcribe list-transcription-jobs

# Testa chamada ao Polly (lista vozes)
aws polly describe-voices --language-code pt-BR
```

Se nenhum erro aparecer, a configuração está correta.

---

## 4️⃣ (Opcional) Criando um bucket S3 para armazenar áudios e transcrições

```bash
# Substitua <nome-do-bucket> por um nome globalmente único
aws s3api create-bucket \
    --bucket meu-bucket-transcribe-polly \
    --region us-east-1 \
    --create-bucket-configuration LocationConstraint=us-east-1
```

**Política de bucket (exemplo)** – permite que o usuário IAM acesse apenas esse bucket:

```json
{
  "Version":"2012-10-17",
  "Statement":[{
    "Sid":"AllowUserAccess",
    "Effect":"Allow",
    "Principal":{"AWS":"arn:aws:iam::<ACCOUNT_ID>:user/aws-cli-transcribe-polly-s3"},
    "Action":["s3:GetObject","s3:PutObject","s3:ListBucket"],
    "Resource":["arn:aws:s3:::meu-bucket-transcribe-polly","arn:aws:s3:::meu-bucket-transcribe-polly/*"]
  }]
}
```

> **Como aplicar:** Salve o JSON em `bucket-policy.json` e execute  
> `aws s3api put-bucket-policy --bucket meu-bucket-transcribe-polly --policy file://bucket-policy.json`

---

## 5️⃣ Resumo rápido (cheat‑sheet)

```bash
# 1️⃣ Instalação (Linux/WSL)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version   # verifica

# 2️⃣ Configuração
aws configure
#   AWS Access Key ID: <sua-access-key>
#   AWS Secret Access Key: <sua-secret-key>
#   Default region name: us-east-1
#   Default output format: json

# 3️⃣ Testes rápidos
aws s3 ls
aws transcribe list-transcription-jobs
aws polly describe-voices

# 4️⃣ Criar bucket (opcional)
aws s3api create-bucket --bucket meu-bucket-transcribe-polly --region us-east-1 \
    --create-bucket-configuration LocationConstraint=us-east-1
```

---

## 6️⃣ Boas práticas de segurança

| Prática | Por quê? |
|---------|----------|
| **MFA (Multi‑Factor Authentication)** na conta raiz e nos usuários IAM críticos. | Reduz risco de acesso não autorizado. |
| **Rotação de credenciais** a cada 90‑120 dias. | Minimiza impacto caso a chave seja comprometida. |
| **Políticas de sessão** (`aws:RequestedRegion`, `aws:TagKeys`, etc.) para limitar onde e como a chave pode ser usada. | Controle adicional de uso. |
| **Logs de auditoria** – habilite o **AWS CloudTrail** para registrar todas as chamadas da API. | Facilita investigação de incidentes. |
| **Restrinja IP** – se o usuário for usado apenas de um IP ou VPC, adicione condição `aws:SourceIp` na política. | Reduz superfície de ataque. |

---

## 7️⃣ Próximos passos (se quiser avançar)

1. **Script de transcrição** – use `aws transcribe start-transcription-job` apontando para o bucket S3.  
2. **Integração com Polly** – após obter a transcrição, chame `aws polly synthesize-speech` para gerar áudio.  
3. **Automação** – crie um pequeno script Bash ou Python (boto3) que encadeie as duas etapas.  
4. **Monitoramento** – configure **Amazon CloudWatch Alarms** para alertar caso haja falhas nos jobs.  

---

### 🎉 Pronto! 🎉  

Você agora tem:

- Uma conta AWS (ou confirmou que já possui).  
- Um usuário IAM limitado ao Transcribe, Polly e S3, com credenciais prontas para o `aws-cli`.  
- O `aws-cli` instalado e configurado no seu Linux/WSL.  

Qualquer dúvida ou necessidade de ajuste (por exemplo, restrição a regiões específicas ou uso de políticas mais granulares), é só chamar! Boa jornada na nuvem! 🚀