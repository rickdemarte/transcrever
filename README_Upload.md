# 📂 Como usar **upload.py** para transferir a gravação da entrevista do seu smartphone para o computador

> **Objetivo**  
> 1️⃣ Iniciar o servidor Flask no PC.  
> 2️⃣ Criar uma rede local (hotspot) entre o smartphone e o PC – sem precisar de internet.  
> 3️⃣ Abrir a página de upload no celular, escolher o arquivo de áudio/vídeo e enviá‑lo para o computador.  

A seguir você encontrará tudo o que precisa: requisitos, preparação da rede, execução do script e dicas de solução de problemas.

---

## 1️⃣ Requisitos

| Item | Como obter / instalar |
|------|-----------------------|
| **Python 3.8+** | <ul><li>Windows: <code>winget install Python.Python.3</code> ou baixe do site python.org.</li><li>macOS: <code>brew install python</code> (Homebrew) ou use o instalador oficial.</li><li>Linux: <code>sudo apt-get install python3 python3-pip</code> (Debian/Ubuntu) ou equivalente.</li></ul> |
| **venv** (opcional, mas altamente recomendado) | <ul><li><code>python3 -v venv .venv</code> (na pasta onde está o script).</li><li><code>source .venv/bin/activate</code></li></ul> |
| **Flask** (e **Werkzeug**) | ```bash pip install Flask Werkzeug``` </li> |
| **Smartphone** (Android ou iOS) com a gravação salva na galeria ou em “Arquivos”. |
| **Um cabo USB** (opcional) – só para a primeira configuração, caso queira copiar o script para o PC. |
| **Acesso ao terminal / prompt** no computador. |

> **Obs.:** O script `upload.py` já está pronto – basta salvá‑lo em uma pasta vazia do seu PC.

---

## 2️⃣ Preparando a rede local (sem internet)

 **Execute esses passos apenas se os equipamentos não estiverem na mesma rede, ou tiver algum bloqueio de rede**
 
 *Algumas redes sem fio possuem isolamento dos clientes, Exemplo: Redes públicas, Rede Eduroam (Universidades), e até alguns roteadores residenciais possuem essa configuração.*

### 2.1 Opção A – **Hotspot do smartphone** (mais simples)

| Sistema | Passos |
|---------|--------|
| **Android** (Android 10 ou superior) | 1. **Configurações → Rede e Internet → Hotspot e tethering**.<br>2. Ative **Hotspot Wi‑Fi**.<br>3. Defina um **nome (SSID)** e **senha** (ex.: `EntrevistaHotspot` / `12345678`).<br>4. Anote o **IP do hotspot** que o Android exibe (geralmente algo como `192.168.43.1`). |
| **iOS** (iPhone) | 1. **Ajustes → Compartilhamento de Internet**.<br>2. Ative **Permitir que outros se conectem**.<br>3. Defina a senha da rede Wi‑Fi.<br>4. O iPhone funciona como gateway `172.20.10.1` (ou similar). |

> **Resultado:** Seu telefone cria uma rede Wi‑Fi própria. O PC se conecta a ela como se fosse um roteador comum.

### 2.2 Opção B – **Hotspot do computador** (caso prefira que o PC seja o ponto de acesso)

| Sistema | Passos |
|--------|--------|
| **Windows 10/11** | 1. **Configurações → Rede e Internet → Hotspot móvel**.<br>2. Ative **Compartilhar minha conexão com outros dispositivos**.<br>3. Escolha “Wi‑Fi” como compartilhamento e configure SSID + senha.<br>4. Anote o IP do PC (geralmente `192.168.137.1`). |
| **macOS** | 1. **Preferências do Sistema → Compartilhamento**.<br>2. Marque **Compartilhamento de Internet** → “Compartilhar conexão de: Ethernet” para “Computadores usando: Wi‑Fi”.<br>3. Clique em **Opções de Wi‑Fi** e configure SSID + senha.<br>4. O IP do Mac será algo como `192.168.2.1`. |
| **Linux (Ubuntu)** | ```bash sudo nmcli device wifi hotspot ifname <interface> ssid EntrevistaHotspot password 12345678```<br>O IP padrão será `10.42.0.1`. |

> **Dica:** Se o PC já estiver conectado a outra rede (ex.: Wi‑Fi da casa), desconecte‑se antes de ativar o hotspot para evitar conflitos de IP.

---

## 3️⃣ Executando o script **upload.py** no computador

1. **Abra um terminal** (Prompt de Comando, PowerShell, Terminal macOS ou Linux) e navegue até a pasta onde salvou `upload.py`.

   ```bash
   cd /caminho/para/pasta/do/script
   ```

2. **Instale as dependências** (caso ainda não tenha feito):

   ```bash
   python3 -v venv .venv # [Opcional] Executa apenas uma vez, pra não instalar muita coisa no computador.
   source .venv/bin/activate # Sempre que executar o script (caso saia do Prompt)
   pip install Flask Werkzeug
   ```

3. **Execute o script**:

   ```bash
   python upload.py
   ```

   Você verá algo como:

   ```
   * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   ```

   - `0.0.0.0` significa “aceitar conexões de qualquer IP da rede”.
   - A porta padrão é **5000** (você pode mudar alterando `app.run(host='0.0.0.0', port=5000, debug=True)`).

4. **Descubra o IP local do seu computador** (necessário para o celular acessar o servidor).

   - **Windows**: `ipconfig` → procure o campo *Endereço IPv4* da interface que está conectada ao hotspot (ex.: `192.168.43.100`).
   - **macOS / Linux**: `ifconfig` ou `ip addr show` → procure o endereço da interface `wlan0`, `en0`, `eth0`, etc.

   **Exemplo:** `192.168.43.100`

---

## 4️⃣ Conectando o smartphone ao hotspot e enviando o arquivo

### 4.1 Conecte ao hotspot (apenas se não estiverem na mesma rede, ou não for possível no "Wi-Fi" atual)

1. No **Android** ou **iOS**, vá para **Configurações → Wi‑Fi**.
2. Selecione o SSID que você criou (`Rede sem fio`) e digite a senha.
3. Verifique que o telefone recebeu um IP na mesma sub‑rede (ex.: `192.168.43.101`).

### 4.2 Abra a página de upload

1. No navegador do celular (Chrome, Safari, etc.) digite o endereço completo do servidor Flask:

   ```
   http://<IP_DO_PC>:5000/
   ```

   **Exemplo:** `http://192.168.43.100:5000/`

2. A página aparecerá assim:

   ![exemplo de página upload] (texto explicativo – não é necessário imagem real)

   - Campo **Escolher arquivo** → toque e selecione a gravação (geralmente em *Arquivos* ou *Galeria* → *Áudio* / *Vídeo*).
   - Toque em **Upload**.

3. O servidor receberá o arquivo, salvando‑o no diretório onde o script está rodando. A página será recarregada mostrando a lista de arquivos já presentes, com links **download** ao lado.

### 4.3 Baixe o arquivo no PC (opcional)

- Se quiser copiar o arquivo para outra pasta, basta clicar no link **download** na lista (ou abrir a pasta do script no PC, pois o arquivo já está lá).

---

## 5️⃣ Dicas avançadas & segurança

| Tema | Recomendações |
|------|---------------|
| **Alterar a pasta de destino** | Edite a constante `UPLOAD_FOLDER` no início do script: <br>`UPLOAD_FOLDER = os.path.abspath('uploads')` <br>Crie a pasta `uploads` antes de iniciar o servidor. |
| **Mudar a porta** | `app.run(host='0.0.0.0', port=8080, debug=True)` – útil se a porta 5000 estiver bloqueada. |
| **Desativar o modo debug em produção** | Troque `debug=True` por `debug=False` ou remova o parâmetro. |
| **Firewall** | Certifique‑se de que o firewall do PC permite tráfego na porta escolhida (ex.: 5000). No Windows: *Painel de Controle → Sistema e Segurança → Firewall do Windows → Configurações avançadas → Regras de entrada → Nova Regra → Porta → TCP → 5000 → Permitir*. |
| **Limitar tamanho máximo** | Adicione `app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024` (500 MB) antes das rotas. |
| **HTTPS (opcional)** | Para transferências sensíveis, use `flask-talisman` ou um proxy reverso (Nginx) com certificado auto‑assinado. Não é obrigatório para uso interno em hotspot. |
| **Desligar hotspot** | Quando terminar, desative o hotspot no telefone/computador para economizar bateria e evitar acessos indesejados. |

---

## 6️⃣ Solução de problemas mais comuns

| Sintoma | Possível causa | Como resolver |
|---------|----------------|----------------|
| **Página não carrega no celular** | IP incorreto ou firewall bloqueando a porta. | Verifique o IP do PC (`ipconfig`/`ifconfig`). Abra a porta 5000 no firewall. |
| **O celular não vê o hotspot** | Hotspot desativado ou senha errada. | Reative o hotspot, reconecte o celular. |
| **Upload falha / “File not found”** | O arquivo não foi enviado (campo vazio). | Certifique‑se de ter escolhido o arquivo antes de tocar em **Upload**. |
| **Arquivo aparece corrompido** | Conexão interrompida ou limite de tamanho. | Aumente `MAX_CONTENT_LENGTH` ou verifique a força do sinal Wi‑Fi. |
| **O PC não tem endereço IP na rede do hotspot** | O hotspot está configurado para “Compartilhar internet” mas a interface Wi‑Fi do PC está desativada. | Conecte o PC ao hotspot como faria com qualquer rede Wi‑Fi. |
| **O script não inicia (erro de importação)** | Bibliotecas ausentes. | Rode `pip install Flask Werkzeug` novamente. |

---

## 7️⃣ Resumo rápido (passo a passo)

1. **No PC**  
   ```bash
   cd pasta/do/script
   pip install Flask Werkzeug
   python upload.py
   ipconfig   # ou ifconfig → anote o IP
   ```

2. **No smartphone**  
   - Ative **Hotspot Wi‑Fi** (Android) ou **Compartilhamento de Internet** (iOS).  
   - Conecte o PC ao hotspot (ou o smartphone ao hotspot do PC).  

3. **No navegador do celular**  
   - Digite `http://<IP_DO_PC>:5000/`.  
   - Selecione o arquivo da entrevista → **Upload**.  

4. **No PC**  
   - O arquivo aparece na mesma pasta do script (ou na pasta configurada).  
   - Opcional: clique em **download** na página para baixar novamente ou mova o arquivo para outro diretório.

---

## 8️⃣ Perguntas frequentes (FAQ)

| Pergunta | Resposta |
|----------|----------|
| **Preciso de internet para que o hotspot funcione?** | Não. O hotspot cria uma rede local mesmo sem conexão à internet. |
| **Posso usar Wi‑Fi Direct em vez de hotspot?** | Sim, mas o Flask precisa de um endereço IP estável. O hotspot é mais simples porque o PC recebe um IP via DHCP. |
| **O que acontece se eu fechar o terminal?** | O servidor Flask para. Basta reabrir o terminal e executar `python upload.py` novamente. |
| **Como faço para que o script rode automaticamente ao ligar o PC?** | Crie um atalho/serviço (Windows Task Scheduler, macOS LaunchAgent, systemd no Linux) que execute `python /caminho/upload.py`. |
| **Existe risco de alguém da vizinhança acessar meus arquivos?** | Enquanto o hotspot estiver ativo, qualquer dispositivo que conheça a senha pode acessar o servidor. Use senha forte e desative o hotspot quando terminar. |

---

## 9️⃣ Referências úteis

- **Flask Documentation** – https://flask.palletsprojects.com/
- **Como criar hotspot no Android** – https://support.google.com/android/answer/9059108
- **Personal Hotspot no iPhone** – https://support.apple.com/pt-br/HT204023
- **Configurar firewall no Windows** – https://support.microsoft.com/pt-br/windows/abrir-uma-porta-no-firewall-do-windows-10-5c0c5b2c-5b6f-0d71-5c9c-2f6c5e6a1a0b

---

> **Pronto!** Agora você tem um método rápido, barato e sem depender de internet para transferir gravações do seu smartphone para o computador usando apenas o script `upload.py` e o hotspot Wi‑Fi do seu telefone. Boa captura de entrevistas! 🎙️🚀