class ConsoleView:
    
    @staticmethod
    def mostrar_cabecalho():
        print("\n" + "="*60)
        print("          SCRAPING - GOV.BR - ANS")
        print("="*60)
    
    @staticmethod
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
                print(f"      📍 {arquivo['caminho']}")
            else:
                print(f"   ❌ {arquivo['nome']} - FALHOU")
        
        print("\n" + "="*60)
        print("🎉 PROCESSO CONCLUÍDO!")
        print("="*60 + "\n")
    
    @staticmethod
    def mostrar_erro(mensagem):
        print(f"\n🔥 ERRO: {mensagem}")