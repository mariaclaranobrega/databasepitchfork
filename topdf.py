from fpdf import FPDF
from grafico_media_genero import media_generos
from leituras import anos_melhores, media_str, anos_acima_media, str_melhores_artistas, artistas_reviravolta


class PDF(FPDF):
    def header(self):
        self.image(r'static/images/download (1).png', 10, 8, 30)
        self.set_font('Arial', 'B', size=13)
        self.set_margins(15, 3, 15)
        self.ln(20)
        # Mover para direita
        self.cell(180, 5, "Pitchfork", align='C')
        self.ln(10)

    def footer(self):
        # 1,5cm do final
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Contar as páginas
        self.cell(0, 10, 'Página ' + str(self.page_no()) + f'/{self.alias_nb_pages()}', 0, 0, 'R')

    def titulo(self, titulo):
        self.set_font('arial', size=14)
        self.multi_cell(0, 10, str(titulo).capitalize(), 0, align='C')
        self.ln()

    def corpo(self, conteudo):
        self.set_font('arial', size=12)
        self.multi_cell(180, 5, conteudo, 0, 1)


# Criar instância da classe
pdf = PDF()
pdf.add_page()
pdf.ln(15)
pdf.corpo("\tA revista norte-americana Pitchfork reune mais de 18.000 reviews sobre o campo da música, desde 1999. "
          "todos estes registros então divididos em categorias de géneros musicais. Abaixo podemos ver quais géneros "
          "possuem mais e menos registros.")
pdf.ln(5)
pdf.image(r'static/images/grafico_generos.png', w=140, x=30)
pdf.corpo(f"\tEntre estes dados, foi calculada uma média de {int(media_generos)} registros por género musical. "
          f"Abaixo vemos a "
          f"quantidade de registros em cada género.")
pdf.image(r'static/images/generos_registos.png', w=180)
pdf.corpo(f"\tAo longo dos anos, analisamos uma crescente em relação às pontuações dos artistas. De 1999 a 2016, "
          f"{sum(anos_melhores.values())} artistas alcançaram a pontuação máxima. Com pontuação média de {media_str}, "
          f"os anos que obtiveram maior destaque nas pontuações máximas foram {anos_acima_media}.")
pdf.ln(8)
pdf.image(r'static/images/anos_melhores.png', w=180)
pdf.ln(8)
pdf.corpo(f"\tNos anos em que a pontuação média foi acima da média geral, os artistas que atingiram pontuação máxima, "
          f"foram:")
pdf.ln(5)
pdf.corpo(f"{str_melhores_artistas}")
pdf.ln(8)
pdf.corpo(f"\tEm anos anteriores, alguns destes artistas obtiveram pontuação abaixo da média geral ({media_str}),"
          f"e na sequência, alavancaram suas carreiras até alcançar a pontuação máxima em anos seguintes. São eles:")
pdf.ln(5)

for grupo in artistas_reviravolta:
    pdf.multi_cell(180, 5, f'{str(grupo[0]).replace("[","").replace("]","")}\n{str(grupo[1]).replace("[","").replace("]","")}\n{str(grupo[2]).replace("[","").replace("]","")}',align='C')
    pdf.ln(8)

pdf.output("primeiro_pdf.pdf")


