import textwrap
USUARIOS = [] 
CONTAS = []   
AGENCIA_PADRAO = "0001"
NUMERO_CONTA_SEQUENCIAL = 1 
LIMITE_SAQUES = 3


def menu():
    """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
    menu_texto = """
    ================ MENU ================
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto)).lower()
def filtrar_usuario(cpf, usuarios):
    """Busca um usuário na lista pelo CPF (identificador único)."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def cadastrar_usuario(usuarios):
    """Permite o cadastro de um novo cliente no sistema."""
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf, 
        "endereco": endereco
    })
    
    print("\n=== Usuário cadastrado com sucesso! ===")
def criar_conta(agencia, numero_conta, usuarios, contas):
    """Cria uma nova conta e a associa a um CPF de usuário existente."""
    cpf = input("Informe o CPF do usuário para associar a conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        nova_conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": cpf, 
            "saldo": 0,
            "limite": 500,
            "extrato": "",
            "numero_saques": 0,
            "limite_saques": LIMITE_SAQUES
        }
        contas.append(nova_conta)
        print(f"\n=== Conta criada com sucesso! ===")
        print(f"Agência: {agencia} | Conta: {numero_conta} | Titular: {usuario['nome']}")
        return nova_conta
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None


def listar_contas(contas, usuarios):
    """Lista todas as contas cadastradas com informações do titular."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n============== CONTAS CADASTRADAS ==============")
    for conta in contas:
        usuario = filtrar_usuario(conta['usuario'], usuarios) 
        nome_usuario = usuario['nome'] if usuario else "CPF Não Encontrado"

        linha = f"""\
            Agência:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{nome_usuario}
        """
        print("-" * 42)
        print(textwrap.dedent(linha))
    print("================================================")
    

def recuperar_conta_usuario(usuarios, contas):
    """Pede o CPF, encontra o usuário e permite selecionar uma de suas contas para a operação."""
    cpf = input("Informe o CPF do titular da conta: ")
    
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado! @@@")
        return None

    contas_usuario = [conta for conta in contas if conta['usuario'] == cpf]

    if not contas_usuario:
        print("\n@@@ Usuário não possui contas cadastradas! @@@")
        return None

    conta_selecionada = None
    
    if len(contas_usuario) == 1:
        conta_selecionada = contas_usuario[0]
        print(f"\nConta {conta_selecionada['numero_conta']} de {usuario['nome']} selecionada automaticamente.")
        
    else:
        print("\nContas disponíveis:")
        for idx, conta in enumerate(contas_usuario):
            print(f"[{idx+1}] Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Saldo: R$ {conta['saldo']:.2f}")
        
        while True:
            try:
                escolha = int(input("Escolha o número da conta para operar: ")) - 1
                if 0 <= escolha < len(contas_usuario):
                    conta_selecionada = contas_usuario[escolha]
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    return conta_selecionada
def depositar(conta, valor):
    """Realiza um depósito na conta."""
    if valor > 0:
        conta['saldo'] += valor
        conta['extrato'] += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


def sacar(conta, valor):
    """Realiza um saque na conta, com validações de limite e saques."""
    excedeu_saldo = valor > conta['saldo']
    excedeu_limite = valor > conta['limite']
    excedeu_saques = conta['numero_saques'] >= conta['limite_saques']

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {conta['limite']:.2f}. @@@")

    elif excedeu_saques:
        print(f"\n@@@ Operação falhou! Número máximo de saques diários excedido ({conta['limite_saques']}). @@@")

    elif valor > 0:
        conta['saldo'] -= valor
        conta['extrato'] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta['numero_saques'] += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


def exibir_extrato(conta):
    """Exibe o extrato da conta e o saldo atual."""
    print("\n================ EXTRATO ================")
    print("Agência:", conta['agencia'])
    print("Conta:", conta['numero_conta'])
    print("-" * 35)
    
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print("-" * 35)
    print(f"Saldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")
def main():
    """Função principal que gerencia o fluxo do sistema bancário."""
    global NUMERO_CONTA_SEQUENCIAL 
    
    while True:
        opcao = menu()

        if opcao == "nu":
            cadastrar_usuario(USUARIOS)

        elif opcao == "nc":
            if not USUARIOS:
                print("\n@@@ É necessário cadastrar um usuário antes de criar uma conta. @@@")
                continue
                
            nova_conta = criar_conta(AGENCIA_PADRAO, NUMERO_CONTA_SEQUENCIAL, USUARIOS, CONTAS)
            if nova_conta:
                NUMERO_CONTA_SEQUENCIAL += 1 

        elif opcao == "lc":
            listar_contas(CONTAS, USUARIOS)
            
        elif opcao in ("d", "s", "e"):
            conta_selecionada = recuperar_conta_usuario(USUARIOS, CONTAS)
            
            if not conta_selecionada:
                continue

            if opcao == "d":
                try:
                    valor = float(input("Informe o valor do depósito: "))
                    depositar(conta_selecionada, valor)
                except ValueError:
                    print("\n@@@ Valor inválido. Informe um número. @@@")

            elif opcao == "s":
                try:
                    valor = float(input("Informe o valor do saque: "))
                    sacar(conta_selecionada, valor)
                except ValueError:
                    print("\n@@@ Valor inválido. Informe um número. @@@")

            elif opcao == "e":
                exibir_extrato(conta_selecionada)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário. Volte sempre!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()