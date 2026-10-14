# RentSmart - Sistema de Orçamento de Locação da R.M Imóveis

import csv
1
TAXA_CONTRATUAL = 2000.00
MAX_PARCELAS = 5
VALOR_GARAGEM = 300.00          
VALOR_PACOTE_ESTUDIO = 250.00   
VALOR_VAGA_EXTRA_ESTUDIO = 60.00
DESCONTO_SEM_CRIANCAS = 0.05   

class Imovel:
    def __init__(self, tipo, aluguel_base):
        self.tipo = tipo
        self.aluguel_base = aluguel_base
        self.quartos = 1
        self.itens = []

    def calcular_aluguel(self):
        
        self.itens = [("Aluguel-base (" + self.tipo + ")", self.aluguel_base)]
        return self.aluguel_base

class Apartamento(Imovel):
    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas

    def calcular_aluguel(self):
        total = super().calcular_aluguel()

        if self.quartos == 2:
            total += 200.00
            self.itens.append(("Adicional de 2 quartos", 200.00))

        if self.tem_garagem:
            total += VALOR_GARAGEM
            self.itens.append(("Vaga de garagem", VALOR_GARAGEM))

      
        if not self.tem_criancas:
            desconto = total * DESCONTO_SEM_CRIANCAS
            total -= desconto
            self.itens.append(("Desconto de 5% (sem crianças)", -desconto))

        return total

class Casa(Imovel):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_aluguel(self):
        total = super().calcular_aluguel()

        if self.quartos == 2:
            total += 250.00
            self.itens.append(("Adicional de 2 quartos", 250.00))

        if self.tem_garagem:
            total += VALOR_GARAGEM
            self.itens.append(("Vaga de garagem", VALOR_GARAGEM))

        return total
  
class Estudio(Imovel):
    def __init__(self, quer_pacote, vagas_extras):
        super().__init__("Estúdio", 1200.00)
        self.quer_pacote = quer_pacote
        self.vagas_extras = vagas_extras

    def calcular_aluguel(self):
        total = super().calcular_aluguel()

        if self.quer_pacote:
            total += VALOR_PACOTE_ESTUDIO
            self.itens.append(("Pacote de estacionamento (2 vagas)", VALOR_PACOTE_ESTUDIO))

            if self.vagas_extras > 0:
                valor_extras = self.vagas_extras * VALOR_VAGA_EXTRA_ESTUDIO
                total += valor_extras
                texto = "Vagas adicionais (" + str(self.vagas_extras) + " x R$ 60,00)"
                self.itens.append((texto, valor_extras))

        return total

class Orcamento:
    def __init__(self, imovel, parcelas):
        self.imovel = imovel
        self.parcelas = parcelas
        self.aluguel_mensal = 0.0
        self.valor_parcela = 0.0

    def calcular(self):
        self.aluguel_mensal = self.imovel.calcular_aluguel()
        self.valor_parcela = TAXA_CONTRATUAL / self.parcelas

    def mostrar_resumo(self):
        print()
        print("=" * 50)
        print("        RESUMO DO ORÇAMENTO - R.M IMÓVEIS")
        print("=" * 50)
        print("Imóvel:", self.imovel.tipo, "-", self.imovel.quartos, "quarto(s)")
        print("-" * 50)
        print("COMO O ALUGUEL MENSAL FOI FORMADO:")
        for descricao, valor in self.imovel.itens:
            print(" ", descricao.ljust(38), formatar(valor).rjust(10))
        print("-" * 50)
        print("  ALUGUEL MENSAL".ljust(40), formatar(self.aluguel_mensal).rjust(10))
        print()
        print("TAXA CONTRATUAL (cobrada à parte do aluguel):")
        print("  Valor total:", formatar(TAXA_CONTRATUAL))
        print("  Parcelamento:", self.parcelas, "x de", formatar(self.valor_parcela))
        print("=" * 50)

    def gerar_csv(self, nome_arquivo):
        acumulado = 0.0
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel", "Parcela_Taxa", "Total_do_Mes", "Total_Acumulado"])

            for mes in range(1, 13):
                if mes <= self.parcelas:
                    parcela_taxa = self.valor_parcela
                else:
                    parcela_taxa = 0.0

                total_mes = self.aluguel_mensal + parcela_taxa
                acumulado += total_mes

                escritor.writerow([
                    mes,
                    "%.2f" % self.aluguel_mensal,
                    "%.2f" % parcela_taxa,
                    "%.2f" % total_mes,
                    "%.2f" % acumulado,
                ])

        print("Arquivo CSV gerado:", nome_arquivo)


def formatar(valor):
    texto = "{:,.2f}".format(valor)
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    if valor < 0:
        return "- R$ " + texto.replace("-", "")
    return "R$ " + texto


def perguntar_numero(pergunta, minimo, maximo):
    while True:
        resposta = input(pergunta).strip()
        if resposta.isdigit():
            numero = int(resposta)
            if minimo <= numero <= maximo:
                return numero
        print("  Entrada inválida! Digite um número de", minimo, "a", maximo)


def perguntar_sim_nao(pergunta):

    while True:
        resposta = input(pergunta + " (s/n): ").strip().lower()
        if resposta == "s":
            return True
        if resposta == "n":
            return False
        print("  Entrada inválida! Digite apenas s ou n.")

# PROGRAMA PRINCIPAL
def main():
    print("=== RentSmart - R.M Imóveis  ===")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    escolha = perguntar_numero("Escolha o tipo de imóvel: ", 1, 3)

    if escolha == 1:
        quartos = perguntar_numero("Quantos quartos (1 ou 2)? ", 1, 2)
        garagem = perguntar_sim_nao("Deseja vaga de garagem?")
        criancas = perguntar_sim_nao("Possui crianças?")
        imovel = Apartamento(quartos, garagem, criancas)

    elif escolha == 2:
        quartos = perguntar_numero("Quantos quartos (1 ou 2)? ", 1, 2)
        garagem = perguntar_sim_nao("Deseja vaga de garagem?")
        imovel = Casa(quartos, garagem)

    else:
        pacote = perguntar_sim_nao("Deseja o pacote de estacionamento (2 vagas por R$ 250,00)?")
        extras = 0
        if pacote:
            extras = perguntar_numero("Quantas vagas adicionais (R$ 60,00 cada, 0 a 10)? ", 0, 10)
        imovel = Estudio(pacote, extras)

    parcelas = perguntar_numero("Taxa contratual em quantas parcelas (1 a 5)? ", 1, MAX_PARCELAS)

    orcamento = Orcamento(imovel, parcelas)
    orcamento.calcular()
    orcamento.mostrar_resumo()
    orcamento.gerar_csv("projecao_12_meses.csv")


main()
