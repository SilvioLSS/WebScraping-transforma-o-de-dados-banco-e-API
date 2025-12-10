# main.py
from controller.scraping_controller import ScrapingController
from view.console_view import ConsoleView

def main():
    ConsoleView.mostrar_cabecalho()
    
    controller = ScrapingController()
    resultado = controller.executar()
    
    ConsoleView.mostrar_resultado(resultado)

if __name__ == "__main__":
    import sys
    if "--test-zip" in sys.argv:
        print("🧪 Testando ZIP...")
        from model.zipper_model import ZipModel
        resultado = ZipModel.criar_zip(".")
        print(f"Resultado: {resultado}")
    else:
        main()