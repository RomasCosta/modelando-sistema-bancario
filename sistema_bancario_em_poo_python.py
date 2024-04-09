#================= sistema bancário em poo =================
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap


#classe Cliente
class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


#classe Pessoa Fisica
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, cpf, endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf



    def __str__(self):
        return f"""

            Nome: {self.nome}
            Data Nasc: {self.data_nascimento}
            CPF: {self.cpf}
            
        """


#classe Conta
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico


    def sacar(self, valor):
        saldo = self.saldo
        saldo_insuficiente = valor > saldo
        
        if saldo_insuficiente:
            print("Erro ao sacar! Você não tem saldo suficiente")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True

        else:
            print("Erro o sacar! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")

        else:
            print("Operação falhou! O valor informado é inválido.")


        return True


#classe Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
                            
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
            Agência: {self.agencia}
            C/C: {self.numero}
            CPF: {self.cliente.cpf}
        """

#classe Historico
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({

                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
#                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        

        })


#interface Transacao
class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass



#classe saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        


#classe deposito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        pass

    @property
    def valor(self):
        return self._valor
    

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        


def menu():
    menu = """
    =================== Menu =========================
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [nc] - Nova conta
    [lc] - Listar contas
    [lu] - Listar usuários
    [nu] - Novo usuário
    [q] - Sair
    ===================================================

     => """
    return input(menu)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None



def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return

    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
         print("Cliente não encontrado")
         return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)


    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return


    print("\n============== EXTRATO ==============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = ("Não foram realizadas movimentações")
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\nR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\nR${conta.saldo:.2f}")
    print("========================================")



def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro - nro - bairro - cidade/sigla estado: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)


    clientes.append(cliente)


    print("\nCliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, criação de conta interrompida!")
        return

    conta = ContaCorrente.nova_conta( numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso")


def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))
      

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_clientes(clientes)

        elif opcao == "q":
            break

        

main()




    
