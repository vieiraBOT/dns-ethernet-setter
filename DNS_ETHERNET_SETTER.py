# -*- coding: utf-8 -*-
"""
DNS_ETHERNET_SETTER.py - Configuração DNS para Interface Ethernet
Versão: 1.4 | Autor: NetworkMaster Team
Suporte para IPv4, IPv6, teste de conexão e abertura do site
"""

import os
import sys
import subprocess
import ctypes
import time
import urllib.request
import socket
import ssl
import webbrowser

# 🔧 CONFIGURAÇÕES DNS
DNS_SERVERS = {
    '1': {
        'name': 'Cloudflare', 
        'primary': '1.1.1.1', 
        'secondary': '1.0.0.1',
        'ipv6_primary': '2606:4700:4700::1111',
        'ipv6_secondary': '2606:4700:4700::1001'
    },
    '2': {
        'name': 'Google', 
        'primary': '8.8.8.8', 
        'secondary': '8.8.4.4',
        'ipv6_primary': '2001:4860:4860::8888',
        'ipv6_secondary': '2001:4860:4860::8844'
    },
    '3': {
        'name': 'OpenDNS', 
        'primary': '208.67.222.222', 
        'secondary': '208.67.220.220',
        'ipv6_primary': '2620:119:35::35',
        'ipv6_secondary': '2620:119:53::53'
    }
}

# Site específico para teste de conexão
TEST_SITE = "https://redecanais.dev/"

class EthernetDNSSetter:
    def __init__(self):
        self.is_admin = self.check_admin()
        self.interface_name = "Ethernet"  # Nome exato da interface
        
    def check_admin(self):
        """Verifica se é administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def run_as_admin(self):
        """Executa como administrador"""
        if not self.is_admin:
            print("🔄 Executando como Administrador...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)

    def verify_interface_exists(self):
        """Verifica se a interface Ethernet existe"""
        try:
            result = subprocess.run(
                ['netsh', 'interface', 'show', 'interface', 'name="Ethernet"'],
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            return "Ethernet" in result.stdout and "Connected" in result.stdout
            
        except Exception as e:
            print(f"❌ Erro ao verificar interface: {e}")
            return False

    def show_interface_details(self):
        """Mostra detalhes da interface Ethernet"""
        try:
            print(f"\n📊 Detalhes da interface '{self.interface_name}':")
            result = subprocess.run(
                ['netsh', 'interface', 'ipv4', 'show', 'config', f'name="{self.interface_name}"'],
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            print("🔹 Configuração IPv4:")
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['DNS', 'IP', 'Endereço', 'Configuration']):
                    print(f"   {line.strip()}")
            
            # Mostrar também configuração IPv6
            print("\n🔹 Configuração IPv6:")
            result_ipv6 = subprocess.run(
                ['netsh', 'interface', 'ipv6', 'show', 'config', f'name="{self.interface_name}"'],
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            lines_ipv6 = result_ipv6.stdout.split('\n')
            for line in lines_ipv6:
                if any(keyword in line for keyword in ['DNS', 'IP', 'Endereço', 'Configuration']):
                    print(f"   {line.strip()}")
                    
        except Exception as e:
            print(f"❌ Erro ao mostrar detalhes: {e}")

    def set_static_dns(self, dns_primary, dns_secondary, ipv6_primary=None, ipv6_secondary=None):
        """Configura DNS estático para Ethernet (IPv4 e IPv6)"""
        try:
            print(f"\n🔧 Configurando DNS na interface '{self.interface_name}'...")
            
            # Comandos para configurar DNS IPv4
            commands_ipv4 = [
                f'netsh interface ipv4 set dns name="{self.interface_name}" static {dns_primary} primary',
                f'netsh interface ipv4 add dns name="{self.interface_name}" {dns_secondary} index=2'
            ]
            
            print("🔹 Configurando DNS IPv4...")
            for cmd in commands_ipv4:
                print(f"   Executando: {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("   ✅ Comando executado com sucesso!")
                else:
                    error_msg = result.stderr.strip()
                    if "The object already exists" in error_msg:
                        print("   ⚠️  DNS já configurado - pulando...")
                    else:
                        print(f"   ❌ Erro: {error_msg}")
                        return False
                
                time.sleep(1)
            
            # Comandos para configurar DNS IPv6 (se fornecido)
            if ipv6_primary and ipv6_secondary:
                print("\n🔹 Configurando DNS IPv6...")
                commands_ipv6 = [
                    f'netsh interface ipv6 set dns name="{self.interface_name}" static {ipv6_primary} primary',
                    f'netsh interface ipv6 add dns name="{self.interface_name}" {ipv6_secondary} index=2'
                ]
                
                for cmd in commands_ipv6:
                    print(f"   Executando: {cmd}")
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print("   ✅ Comando executado com sucesso!")
                    else:
                        error_msg = result.stderr.strip()
                        if "The object already exists" in error_msg:
                            print("   ⚠️  DNS já configurado - pulando...")
                        else:
                            print(f"   ❌ Erro: {error_msg}")
                            return False
                    
                    time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar DNS: {e}")
            return False

    def set_dhcp_dns(self):
        """Volta para DNS automático (DHCP) para IPv4 e IPv6"""
        try:
            print(f"\n🔄 Restaurando DNS automático em '{self.interface_name}'...")
            
            # Restaurar DHCP para IPv4
            cmd_ipv4 = f'netsh interface ipv4 set dns name="{self.interface_name}" source=dhcp'
            result_ipv4 = subprocess.run(cmd_ipv4, shell=True, capture_output=True, text=True)
            
            if result_ipv4.returncode == 0:
                print("✅ DNS IPv4 automático restaurado!")
            else:
                print(f"❌ Erro IPv4: {result_ipv4.stderr.strip()}")
            
            # Restaurar DHCP para IPv6
            cmd_ipv6 = f'netsh interface ipv6 set dns name="{self.interface_name}" source=dhcp'
            result_ipv6 = subprocess.run(cmd_ipv6, shell=True, capture_output=True, text=True)
            
            if result_ipv6.returncode == 0:
                print("✅ DNS IPv6 automático restaurado!")
                return True
            else:
                print(f"❌ Erro IPv6: {result_ipv6.stderr.strip()}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def flush_dns_cache(self):
        """Limpa cache DNS"""
        try:
            print("\n🧹 Limpando cache DNS...")
            result = subprocess.run(['ipconfig', '/flushdns'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Cache DNS limpo!")
                return True
            else:
                print(f"⚠️  {result.stderr.strip()}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao limpar cache: {e}")
            return False

    def test_connection(self):
        """Testa conexão com internet (IPv4 e IPv6)"""
        try:
            print("\n🌐 Testando conexão com internet...")
            
            # Testa ping para Google (IPv4)
            print("🔹 Testando IPv4...")
            result_ipv4 = subprocess.run(['ping', '-n', '2', 'google.com'], 
                                      capture_output=True, text=True, timeout=10)
            
            if result_ipv4.returncode == 0:
                print("✅ Conexão IPv4: OK!")
            else:
                print("❌ Sem conexão IPv4")
            
            # Testa ping para Google (IPv6)
            print("🔹 Testando IPv6...")
            result_ipv6 = subprocess.run(['ping', '-n', '2', 'ipv6.google.com'], 
                                      capture_output=True, text=True, timeout=10)
            
            if result_ipv6.returncode == 0:
                print("✅ Conexão IPv6: OK!")
                ipv6_ok = True
            else:
                print("❌ Sem conexão IPv6 (pode ser normal se não houver suporte IPv6)")
                ipv6_ok = False
            
            # Testar conexão com o site específico
            print(f"\n🔗 Testando conexão com {TEST_SITE}...")
            site_ok = self.test_site_connection()
            
            return result_ipv4.returncode == 0 or ipv6_ok
                
        except Exception as e:
            print(f"❌ Erro no teste de conexão: {e}")
            return False

    def test_site_connection(self):
        """Testa a conexão com o site específico"""
        try:
            # Criar um contexto SSL que ignora erros de certificado (para evitar problemas)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Extrair o hostname da URL
            hostname = TEST_SITE.split("//")[-1].split("/")[0]
            
            # Primeiro, tentar resolver o DNS
            print(f"   🔍 Resolvendo DNS para {hostname}...")
            try:
                ip_address = socket.gethostbyname(hostname)
                print(f"   ✅ DNS resolvido: {ip_address}")
            except socket.gaierror:
                print("   ❌ Falha ao resolver DNS")
                return False
            
            # Tentar conectar via HTTP
            print("   🌐 Testando conexão HTTP...")
            try:
                # Usar urllib com timeout
                with urllib.request.urlopen(TEST_SITE, timeout=10, context=ssl_context) as response:
                    if response.getcode() == 200:
                        print("   ✅ Conexão com o site bem-sucedida!")
                        return True
                    else:
                        print(f"   ⚠️  Site retornou código: {response.getcode()}")
                        return True  # Ainda considera sucesso pois conseguiu conectar
            except urllib.error.URLError as e:
                print(f"   ❌ Erro de URL: {e.reason}")
                return False
            except Exception as e:
                print(f"   ⚠️  Erro na conexão: {e}")
                return False
                
        except Exception as e:
            print(f"   ❌ Erro inesperado ao testar site: {e}")
            return False

    def open_website(self):
        """Abre o site no navegador padrão"""
        try:
            print(f"\n🌐 Abrindo {TEST_SITE} no navegador...")
            webbrowser.open(TEST_SITE)
            print("✅ Site aberto no navegador!")
            return True
        except Exception as e:
            print(f"❌ Erro ao abrir o site: {e}")
            return False

    def show_current_dns(self):
        """Mostra DNS atual (IPv4 e IPv6)"""
        try:
            print(f"\n🔍 DNS atual na interface '{self.interface_name}':")
            
            # Mostrar DNS IPv4
            print("🔹 DNS IPv4:")
            result_ipv4 = subprocess.run(
                ['netsh', 'interface', 'ipv4', 'show', 'dns', f'name="{self.interface_name}"'],
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if result_ipv4.stdout.strip():
                print(result_ipv4.stdout)
            else:
                print("   Usando DNS automático (DHCP)")
            
            # Mostrar DNS IPv6
            print("\n🔹 DNS IPv6:")
            result_ipv6 = subprocess.run(
                ['netsh', 'interface', 'ipv6', 'show', 'dns', f'name="{self.interface_name}"'],
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if result_ipv6.stdout.strip():
                print(result_ipv6.stdout)
            else:
                print("   Usando DNS automático (DHCP)")
                
        except Exception as e:
            print(f"❌ Erro ao ver DNS atual: {e}")

def ask_to_open_website():
    """Pergunta se o usuário deseja abrir o site"""
    print("\n" + "=" * 60)
    print("🎯 CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 60)
    
    while True:
        choice = input("Deseja abrir o site no navegador? (S/N): ").strip().lower()
        
        if choice in ['s', 'sim', 'y', 'yes']:
            setter = EthernetDNSSetter()
            setter.open_website()
            break
        elif choice in ['n', 'não', 'nao', 'no']:
            print("✅ Tudo pronto! Você pode fechar o programa.")
            break
        else:
            print("❌ Por favor, responda com S (Sim) ou N (Não)")

def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 DNS ETHERNET SETTER - CONFIGURAÇÃO PARA INTERFACE ETHERNET")
    print(f"🔹 Teste de conexão com: {TEST_SITE}")
    print("=" * 60)
    
    # Verifica privilégios
    setter = EthernetDNSSetter()
    setter.run_as_admin()
    
    # Verifica se a interface existe
    if not setter.verify_interface_exists():
        print("❌ Interface 'Ethernet' não encontrada ou desconectada!")
        print("\n💡 Verifique:")
        print("   1. Se o cabo de rede está conectado")
        print("   2. Se a interface está habilitada")
        print("   3. Execute no CMD como Admin:")
        print("      netsh interface show interface")
        input("\nPressione Enter para sair...")
        return
    
    print("✅ Interface 'Ethernet' encontrada e conectada!")
    
    # Mostra menu
    print("\n🌐 Escolha o provedor DNS:")
    for key, server in DNS_SERVERS.items():
        print(f"   {key}. {server['name']} (IPv4: {server['primary']}, IPv6: {server['ipv6_primary']})")
    print("   4. Restaurar DNS automático (DHCP) - IPv4 e IPv6")
    print("   5. Ver DNS atual")
    print("   6. Testar conexão (incluindo site específico)")
    print("   7. Testar apenas conexão com o site")
    
    choice = input("\n🎯 Escolha uma opção: ").strip()
    
    # Processa escolha
    if choice in DNS_SERVERS:
        dns_config = DNS_SERVERS[choice]
        print(f"\n🚀 Configurando {dns_config['name']}...")
        
        setter.show_interface_details()
        
        if setter.set_static_dns(
            dns_config['primary'], 
            dns_config['secondary'],
            dns_config['ipv6_primary'],
            dns_config['ipv6_secondary']
        ):
            setter.flush_dns_cache()
            connection_ok = setter.test_connection()
            
            # Se a conexão foi bem-sucedida, pergunta se quer abrir o site
            if connection_ok:
                ask_to_open_website()
        
    elif choice == '4':
        print("\n🔄 Restaurando DNS automático...")
        if setter.set_dhcp_dns():
            setter.flush_dns_cache()
            connection_ok = setter.test_connection()
            
            # Se a conexão foi bem-sucedida, pergunta se quer abrir o site
            if connection_ok:
                ask_to_open_website()
        
    elif choice == '5':
        setter.show_current_dns()
        input("\nPressione Enter para continuar...")
        main()  # Volta ao menu principal
        
    elif choice == '6':
        connection_ok = setter.test_connection()
        
        # Se a conexão foi bem-sucedida, pergunta se quer abrir o site
        if connection_ok:
            ask_to_open_website()
        else:
            input("\nPressione Enter para continuar...")
            main()  # Volta ao menu principal
        
    elif choice == '7':
        site_ok = setter.test_site_connection()
        
        # Se a conexão foi bem-sucedida, pergunta se quer abrir o site
        if site_ok:
            ask_to_open_website()
        else:
            input("\nPressione Enter para continuar...")
            main()  # Volta ao menu principal
        
    else:
        print("❌ Opção inválida!")
        input("\nPressione Enter para continuar...")
        main()  # Volta ao menu principal
    
    # Comandos manuais de referência
    print("\n" + "=" * 60)
    print("📋 COMANDOS MANUAIS PARA ETHERNET:")
    print("=" * 60)
    print("🔍 Ver configuração atual:")
    print("   netsh interface ipv4 show config name=\"Ethernet\"")
    print("   netsh interface ipv6 show config name=\"Ethernet\"")
    print("\n⚡ Configurar Cloudflare (IPv4 e IPv6):")
    print("   netsh interface ipv4 set dns name=\"Ethernet\" static 1.1.1.1 primary")
    print("   netsh interface ipv4 add dns name=\"Ethernet\" 1.0.0.1 index=2")
    print("   netsh interface ipv6 set dns name=\"Ethernet\" static 2606:4700:4700::1111 primary")
    print("   netsh interface ipv6 add dns name=\"Ethernet\" 2606:4700:4700::1001 index=2")
    print("\n🔄 Voltar para automático:")
    print("   netsh interface ipv4 set dns name=\"Ethernet\" source=dhcp")
    print("   netsh interface ipv6 set dns name=\"Ethernet\" source=dhcp")
    print("\n🧹 Limpar cache DNS:")
    print("   ipconfig /flushdns")

if __name__ == "__main__":
    # Verifica se é Windows
    if os.name != 'nt':
        print("❌ Este script só funciona no Windows")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Operação cancelada")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
    
    input("\n🎯 Pressione Enter para sair...")