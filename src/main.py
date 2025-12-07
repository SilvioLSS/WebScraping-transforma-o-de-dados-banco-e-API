from controller.scraping_controller import ScrapingController
from view.console_view import ConsoleView

def main():

    ConsoleView.mostrar_cabecalho()
    
    controller = ScrapingController()
    resultado = controller.executar()
    
    ConsoleView.mostrar_resultado(resultado)

if __name__ == "__main__":
    main()