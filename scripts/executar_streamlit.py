#!/usr/bin/env python3
"""
Script para executar o sistema de locação com Streamlit
Inicializa o banco de dados e executa a aplicação web
"""

import subprocess
import sys
import os

# Adicionar src ao path para importar database
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import db_manager

def inicializar_banco():
    """Inicializa o banco de dados"""
    print("🔧 Inicializando banco de dados...")
    
    try:
        db_manager.execute_script('SQL/v2-ldi.sql')
        print("✅ Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def executar_streamlit():
    """Executa o aplicativo Streamlit"""
    print("🚀 Iniciando aplicação Streamlit...")
    print("📱 A aplicação será aberta no seu navegador em: http://localhost:8501")
    print("🛑 Para parar, pressione Ctrl+C")
    print("\n⚠️  IMPORTANTE: Use SEMPRE 'streamlit run' para executar o app!")
    print("   ❌ NÃO: python src/app_streamlit.py")
    print("   ✅ SIM: streamlit run src/app_streamlit.py")
    
    try:
        # Caminho correto para o app_streamlit.py
        app_path = os.path.join("..", "src", "app_streamlit.py")
        if not os.path.exists(app_path):
            app_path = os.path.join("src", "app_streamlit.py")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada!")
    except FileNotFoundError:
        print("❌ Streamlit não está instalado!")
        print("🔧 Instale com: pip install streamlit")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {e}")
        print("\n🔧 Tente executar manualmente:")
        print("   streamlit run src/app_streamlit.py")

def main():
    """Função principal"""
    print("🏠 SISTEMA DE LOCAÇÃO DE IMÓVEIS - STREAMLIT")
    print("=" * 50)
    
    # Verificar se o banco está acessível
    if inicializar_banco():
        print("\n" + "=" * 50)
        executar_streamlit()
    else:
        print("❌ Não foi possível inicializar o sistema.")
        sys.exit(1)

if __name__ == "__main__":
    main()
