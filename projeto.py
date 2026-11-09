import ctypes
import subprocess
import sys


# Programas disponíveis para instalação
programas = {
    "1": ("7-Zip", "7zip.7zip"),
    "2": ("Notepad++", "Notepad++.Notepad++"),
    "3": ("VLC", "VideoLAN.VLC")
}


# Verifica se o programa está sendo executado como administrador
def verificar_administrador():
    return ctypes.windll.shell32.IsUserAnAdmin()


# Solicita permissão de administrador
def solicitar_administrador():
    if not verificar_administrador():
        shell_execute = ctypes.windll.shell32.ShellExecuteW
        shell_execute.restype = ctypes.c_void_p
        resultado = shell_execute(
            None,
            "runas",
            sys.executable,
            subprocess.list2cmdline(sys.argv),
            None,
            1
        )
        if not resultado or resultado <= 32:
            raise OSError(f"Não foi possível iniciar como administrador (código {resultado}).")
        sys.exit(0)


# Verifica se o WinGet está disponível
def verificar_winget():
    try:
        subprocess.run(
            ["winget", "--version"],
            check=True,
            capture_output=True
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


# Exibe o menu
def exibir_menu():
    print("\n+----------------------------------+")
    print("|      INSTALADOR DE PROGRAMAS     |")
    print("+----------------------------------+")

    for numero, programa in programas.items():
        print(f"| {numero} - {programa[0]:<29}|")

    print("| 0 - Sair                         |")
    print("+----------------------------------+")
    print("Digite um ou mais números separados por vírgula (exemplo: 1,2).\n")


# Instala um programa
def instalar_programa(nome, id_programa):
    print(f"\nInstalando {nome}...")

    resultado = subprocess.run([
        "winget",
        "install",
        "--id",
        id_programa,
        "--exact",
        "--accept-package-agreements",
        "--accept-source-agreements"
    ])

    if resultado.returncode == 0:
        print(f"{nome} instalado com sucesso!")
        return True
    else:
        print(f"Falha ao instalar {nome}.")
        return False


# Função principal
def main():

    solicitar_administrador()

    print("\nPrivilégios de administrador confirmados.")

    if not verificar_winget():
        print("\nERRO: WinGet não foi encontrado.")
        input("\nPressione ENTER para sair...")
        return

    while True:
        exibir_menu()
        escolha = input("Escolha: ").strip()

        if escolha == "0":
            print("\nPrograma encerrado.")
            return

        resultados = []

        for numero in escolha.split(","):
            numero = numero.strip()

            if numero in programas:
                nome, id_programa = programas[numero]
                sucesso = instalar_programa(nome, id_programa)
                resultados.append((nome, sucesso))
            else:
                print(f"\nOpção inválida: {numero}")

        if resultados:
            print("\n+-------------- RESUMO -------------+")
            for nome, sucesso in resultados:
                status = "SUCESSO" if sucesso else "FALHA"
                print(f"| {nome}: {status}")
            print("+-----------------------------------+")

        while True:
            instalar_outro = input("\nDeseja instalar outro programa? (s/n): ").strip().lower()
            if instalar_outro in ("s", "n"):
                break
            print("Digite 's' para sim ou 'n' para não.")

        if instalar_outro == "n":
            print("\n+----------------------------------+")
            print("| 0 - Sair                         |")
            print("+----------------------------------+")
            print("Programa encerrado.")
            break

    input("\nPressione ENTER para encerrar...")


if __name__ == "__main__":
    main()