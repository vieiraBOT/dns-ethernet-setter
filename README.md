
&nbsp; 🌐 DNS Ethernet Setter


![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)
![Windows](https://img.shields.io/badge/Windows-10%2B-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)


> Ferramenta automática para configurar DNS em interfaces Ethernet no Windows com interface intuitiva em português.



&nbsp; ✨ Funcionalidades



\- 🔧Configuração Automática de DNS IPv4 e IPv6

\- 🌐Multi-provedores (Cloudflare, Google, OpenDNS)

\- ✅Teste de Conexão Integrado\*\* com site específico

\- 🧹Limpeza Automática de cache DNS

\- 🔄Restauração Fácil para configuração DHCP

\- 🖱️Interface Intuitiva em português

\- 🚀Abertura Automática do site após configuração

\- 📊Detalhes Completos da interface de rede



&nbsp; 📦 Pré-requisitos



\- ✅Windows 10 ou Windows 11

\- ✅Acesso de Administrador

\- ✅Python 3.6+ (já incluso no Windows 10/11)

\- ✅Interface Ethernet conectada e ativa



&nbsp; 🚀 Instalação Rápida



&nbsp;   Método 1: Clone o repositório

git clone https://github.com/vieiraBOT/dns-ethernet-setter.git

cd dns-ethernet-setter



&nbsp;    Método 2: Download direto

1\. 📥 Baixe o arquivo `DNS\_ETHERNET\_SETTER.py`

2\. 📂 Salve em qualquer pasta de sua preferência



&nbsp; 🎯 Como Usar



&nbsp;       Execução Simples:

1\. Clique com botão direito no arquivo `DNS\_ETHERNET\_SETTER.py`

2\. Selecione "Executar como administrador"

3\. Siga o menu interativo



&nbsp;    Via Prompt de Comando:

&nbsp;  cmd

\# Navegue até a pasta do script

cd C:\\caminho\\para\\pasta



\# Execute como administrador

python DNS\_ETHERNET\_SETTER.py

```



&nbsp;  🎮 Menu de Opções



&nbsp;    1. 🌐 Cloudflare DNS

\- IPv4 Primário: `1.1.1.1`

\- IPv4 Secundário: `1.0.0.1`

\- IPv6 Primário: `2606:4700:4700::1111`

\- IPv6 Secundário: `2606:4700:4700::1001`



&nbsp;    2. 🎯 Google DNS

\- IPv4 Primário: `8.8.8.8`

\- IPv4 Secundário: `8.8.4.4`

\- IPv6 Primário: `2001:4860:4860::8888`

\- IPv6 Secundário: `2001:4860:4860::8844`



&nbsp;    3. 🔓 OpenDNS

\- IPv4 Primário: `208.67.222.222`

\- IPv4 Secundário: `208.67.220.220`

\- IPv6 Primário: `2620:119:35::35`

\- IPv6 Secundário: `2620:119:53::53`



&nbsp;    4. 🔄 Restaurar DHCP

Volta para configuração automática de DNS



&nbsp;    5. 📊 Ver DNS Atual

Mostra configurações atuais da interface



&nbsp;    6. 🧪 Testar Conexão

Testa conectividade com internet e site específico



&nbsp;   🛠️ Comandos Manuais de Referência

&nbsp;cmd

\# Ver configuração atual

netsh interface ipv4 show config name="Ethernet"

netsh interface ipv6 show config name="Ethernet"



\# Configurar DNS manualmente

netsh interface ipv4 set dns name="Ethernet" static 1.1.1.1 primary

netsh interface ipv4 add dns name="Ethernet" 1.0.0.1 index=2



\# Voltar para DHCP

netsh interface ipv4 set dns name="Ethernet" source=dhcp



\# Limpar cache DNS

ipconfig /flushdns

```



&nbsp;    ❓ Perguntas Frequentes



&nbsp;❔ O script funciona com Wi-Fi?

R: Não, este script foi desenvolvido especificamente para interfaces Ethernet.



&nbsp;❔ Preciso instalar Python?

R: Não, o Windows 10/11 já vem com Python pré-instalado.



&nbsp;❔ É seguro usar este script?

R: Sim, o código é aberto e apenas executa comandos padrão do Windows.



&nbsp;❔ Posso personalizar o site de teste?

R: Sim, edite a variável `TEST\_SITE` no código.



&nbsp;❔ Como adiciono outro provedor DNS?

R: Edite o dicionário `DNS\_SERVERS` no código fonte.



&nbsp;🐛 Solução de Problemas



&nbsp;🔴 Erro: "Interface Ethernet não encontrada"

\- Verifique se o cabo de réseau está conectado

\- Confirme se a interface está habilitada

\- Execute como Administrador



&nbsp;🔴 Erro: "Acesso negado"

\- Execute o script como Administrador

\- Clique direito → "Executar como administrador"



&nbsp;🔴 Script não inicia

\- Verifique se o Python está instalado: `python --version`

\- Execute pelo Prompt de Comando



&nbsp;🤝 Como Contribuir



1\. Faça um Fork do projeto

2\. Crie uma Branch para sua feature (`git checkout -b feature/AmazingFeature`)

3\. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)

4\. Push para a Branch (`git push origin feature/AmazingFeature`)

5\. Abra um Pull Request



&nbsp;📜 Licença



Distribuído sob licença MIT. Veja o arquivo \[LICENSE](LICENSE) para mais informações.



&nbsp;👨💻 Autor



vieiraBOT - \[GitHub](https://github.com/vieiraBOT) 



⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!



