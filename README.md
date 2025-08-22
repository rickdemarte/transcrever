# 📄 Como usar – **`transcreve`**  
*Script Bash que envia um arquivo de áudio para o **AWS Transcribe**, aguarda a conclusão, baixa o JSON resultante e o converte em CSV.*

***IMPORTANTE:** *Esse Script foi feito para transcrever uma entrevista, ou seja, 2 pessoas falando.*
*Caso queira usa-lo para mais pessoas, altere o parâmentro `--settings`*

---  

## 1️⃣ Pré‑requisitos

**Arquivo de áudio**: *Caso você não tenha o arquivo de áudio no computador que vai executar o script, você pode usar o upload.py para isso.*

*O passo a passo [está aqui](README_Upload.md).*

**AWS-Cli**: *Você precisa do aws-cli instalado e configurado.*

*O passo a passo [está aqui](README_AWS-Cli.md).*


| Ferramenta | Versão mínima | Como instalar |
|------------|----------------|---------------|
| **Bash** | 4.x+ (já vem na maioria dos *nix) | No Microsoft Windows: Veja [Como Instalar WSL](https://learn.microsoft.com/pt-br/windows/wsl/install) |
| **AWS CLI** | 2.x | `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"` → unzip → `sudo ./aws/install` |
| **jq** (processador JSON) | 1.6 | `sudo apt-get install jq`  /  `brew install jq` |
| **Credenciais AWS** (Access Key + Secret) configuradas | – | `aws configure` (defina *region* e *output* padrão) |
| **Bucket S3** | – | Crie via console ou CLI (`aws s3 mb s3://BUCKET`) |

> **Dica:** O script usa a região **`us-west-2`**; ajuste se necessário (variável `--region`).

---

## 2️⃣ Visão geral
| O que faz | Como funciona |
|-----------|---------------|
| **Upload** do áudio para um bucket S3 | `aws s3 cp` |
| **Inicia** um job de transcrição no Amazon Transcribe | `aws transcribe start‑transcription-job` |
| **Monitora** o status até terminar | `aws transcribe get‑transcription-job` (loop a cada 30 s) |
| **Baixa** o JSON de saída | `aws s3 cp` |
| **Exporta** os segmentos de áudio para CSV (usando `jq`) | Função `export_audio_segments_to_csv` |

> **Obs.:** O script assume que o bucket S3 já existe e que o usuário tem permissão para ler/escrever nele.

---

## 3️⃣ Instalação do script

1. **Copie** o código abaixo para um arquivo chamado `transcreve` (sem extensão).  
2. **Torne‑o executável**:  

```bash
chmod +x transcreve
```

> Se preferir, coloque o arquivo em um diretório presente no `$PATH` (ex.: `~/bin`).

---

## 4️⃣ Como usar

### Sintaxe básica

```bash
./transcreve caminho/do/arquivo.ext
```

- **`caminho/do/arquivo.ext`** – caminho absoluto ou relativo para o áudio que será transcrito.  
- O script aceita **qualquer** formato suportado pelo Transcribe (`mp3`, `mp4`, `wav`, `flac`, `ogg`, `webm`).

### Exemplo rápido

```bash
# áudio local
./transcreve entrevista.mp3

# áudio em outro diretório
./transcreve /tmp/gravacoes/reuniao.wav

# script em outro diretório
/caminho/do/script/transcreve entrevista.mp3
```

### O que acontece após a execução?

| Etapa | Ação | Arquivo gerado | Local |
|-------|------ | ----------|-------|
| 01 | **Upload** do áudio → S3 | `s3://Bucket/audio/<nome>` | – |
| 02 | **Job** de transcrição iniciado | – | – |
| 03 | **Download** do JSON | `<nome>.json` | diretório onde o script foi executado |
| 04 | **Exportação** para CSV | `<nome>.csv` | diretório onde o script foi executado |

---

## 5️⃣ Parâmetros internos (não expostos)

| Variável | Valor padrão | Comentário |
|----------|--------------|------------|
| `BUCKET` | `BUCKET` | Nome do bucket S3 usado para áudio e transcrições |
| `BUCKET_AUDIO` | `s3://BUCKET/audio` | Prefixo onde o áudio é armazenado |
| `BUCKET_TRANSCRICAO` | `s3://BUCKET/transcriptions` | Onde o JSON de saída será salvo |
| `JOB_NAME` | `TranscricaoEntrevista_YYYYMMDDHHMMSS` | Nome único do job |
| `--region` | `us-west-2` | Região da AWS – altere se seu bucket estiver em outra região |
| `--language-code` | `pt-BR` | Idioma da transcrição – troque para `en-US`, `es-ES`, etc., se precisar |
| `--settings` | `ShowSpeakerLabels:true, MaxSpeakerLabels:2` | Habilita identificação de até 2 palestrantes |

> Para mudar algum valor, edite o script antes de rodá‑lo.

---

## 6️⃣ Dicas de uso

| Situação | Solução |
|----------|---------|
| **Arquivos grandes** (≥ 2 GB) | O Transcribe aceita até 4 GB. Divida o áudio em partes menores antes de chamar o script. |
| **Mais de 2 palestrantes** | Altere o JSON de `--settings`: `"MaxSpeakerLabels":5` (ou o número desejado). |
| **Outra região** | Substitua `us-west-2` nas linhas que usam `--region`. |
| **Nome do bucket diferente** | Troque a variável `BUCKET` e os prefixes `BUCKET_AUDIO`/`BUCKET_TRANSCRICAO`. |
| **Erro “jq não está instalado”** | Instale `jq` (ver pré‑requisitos). |
| **Job falha** | Verifique o console da AWS → *Transcribe → Jobs* para detalhes. Também confira se o bucket tem política de leitura/escrita correta. |

---

## 7️⃣ Resolução de problemas (FAQ)

| Erro | Possível causa | Como corrigir |
|------|----------------|---------------|
| `Uso: ./transcreve <caminho/para/arquivo>` | Nenhum argumento ou mais de um passado | Passe exatamente **um** caminho de arquivo. |
| `Arquivo não encontrado` | Caminho errado ou permissão de leitura | Verifique `ls -l` e corrija o caminho. |
| `aws: command not found` | AWS CLI não instalado ou não está no `$PATH` | Instale a AWS CLI e reinicie o terminal. |
| `jq não está instalado` | `jq` ausente | `sudo apt-get install jq` (Debian/Ubuntu) ou equivalente. |
| `Job falhou` | Formato não suportado, áudio corrompido ou falta de permissão no bucket | Verifique o log do job no console AWS; teste com um áudio pequeno e válido. |
| `Permission denied (publickey)` ao usar `aws s3 cp` | Credenciais AWS ausentes ou chave SSH inválida (se usando EC2) | Rode `aws configure` novamente ou ajuste o IAM role. |
| CSV vazio ou sem cabeçalho | JSON de saída não contém `results.audio_segments` (p.ex., áudio sem fala) | Verifique o JSON manualmente; talvez o áudio seja silencioso. |

---

## 8️⃣ Cheat‑sheet (comandos rápidos)

```bash
# 1️⃣ Tornar o script executável
chmod +x transcreve

# 2️⃣ Executar
./transcreve caminho/arquivo.mp3

# 3️⃣ Verificar status do job manualmente (se precisar)
aws transcribe get-transcription-job \
    --transcription-job-name <JOB_NAME> \
    --query 'TranscriptionJob.TranscriptionJobStatus' \
    --output text

# 4️⃣ Baixar o JSON sem usar o script (exemplo)
aws s3 cp s3://BUCKET/transcriptions/arquivo.json .

# 5️⃣ Converter JSON → CSV (mesma lógica da função)
jq -r '
  .results.audio_segments[0] | keys_unsorted | @csv,
  .results.audio_segments[] |
    [ .id, .transcript, .start_time, .end_time,
      .speaker_label, (.items|@json) ] | @csv
' arquivo.json > arquivo.csv
```

---

## 9️⃣ Considerações finais

- **Segurança:** O script não criptografa o áudio nem o JSON. Se o conteúdo for sensível, habilite **S3 Server‑Side Encryption** ou **client‑side encryption**.  
- **Custos:** O Amazon Transcribe cobra por minuto de áudio processado. Verifique a fatura da sua conta AWS.  
- **Escalabilidade:** Para processar lotes de arquivos, crie um *loop* que chame `transcreve` para cada arquivo ou use o AWS Batch/Step Functions.

Pronto! Agora você tem tudo que precisa para usar o comando **`transcreve`** de forma simples e segura. 🎙️🚀