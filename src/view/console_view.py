class ConsoleView:
    
    @staticmethod
    def mostrar_cabecalho():
        print("\n" + "="*60)
        print("          SCRAPING - GOV.BR - ANS")
        print("="*60)
    
    def mostrar_resultado(resultado):
            if not resultado['sucesso']:
                print(f"\n❌ {resultado['mensagem']}")
                return
            
            print(f"\n✅ {resultado['mensagem']}")
            print(f"📁 Pasta: {resultado['pasta']}")

            print("\n" + "-"*60)
            print("📄 ARQUIVOS BAIXADOS:")
            print("-"*60)
            
            for arquivo in resultado['arquivos']:
                if arquivo['sucesso']:
                    print(f"   ✅ {arquivo['nome']}")
                else:
                    print(f"   ❌ {arquivo['nome']} - FALHOU")

            if resultado.get('zip') and resultado['zip']['sucesso']:
                zip_info = resultado['zip']
                print("\n" + "="*60)
                print("📦 ARQUIVO ZIP CRIADO:")
                print("="*60)
                print(f"   📍 Caminho: {zip_info['caminho_zip']}")
                print(f"   📊 Tamanho: {zip_info['tamanho_mb']} MB")
                print(f"   📁 Arquivos dentro: {zip_info['quantidade_arquivos']}")
                print(f"   📋 Conteúdo: {', '.join(zip_info['arquivos'])}")
            
            print("\n" + "="*60)
            print("🎉 PROCESSO CONCLUÍDO!")
            print("="*60 + "\n")
    
    @staticmethod
    def mostrar_erro(mensagem):

        print(f"\n🔥 ERRO: {mensagem}")