from selenium import webdriver
import pandas as pd
import  os

def formatacao(df, chave):
    df[chave] = df[chave].str.replace('.', '')
    df[chave] = df[chave].str.replace(',', '')
    df[chave] = df[chave].str.replace('%', '')

    df[chave] = df[chave].astype(float)
    df[chave] = df[chave] / 100


diretorio_atual = os.getcwd()
pd.set_option('display.max_columns', None)

url = 'https://www.fundsexplorer.com.br/ranking'

driver = webdriver.Chrome(executable_path=f'{diretorio_atual}/chromedriver/chromedriver')

driver.get(url)

# time.sleep(5)
driver.execute_script("""
var elems = document.querySelectorAll('.default-fiis-table__container__table th, .default-fiis-table__container__table td');
for (var i = 0; i < elems.length; i++) {
    elems[i].style.display = 'table-cell';
}
""")

html = driver.page_source
driver.quit()

dados = pd.read_html(html)[0]

dadosdf1 = dados[0:11]

itens = ['Preço Atual (R$)', 'P/VP', 'Último Dividendo', 'Volatilidade', 'DY (12M) Acumulado', 'Liquidez Diária (R$)']

for i in itens:
    formatacao(dados, i)

dados = dados.drop(["Tax. Performance", "Tax. Gestão", "Tax. Administração"], axis=1)

dados_filtrados = dados.loc[(dados['DY (12M) Acumulado'] > 12) & (dados['Liquidez Diária (R$)'] > 300000) & (dados['P/VP'] < 0.8)]

print(type(dados_filtrados))

dados_filtrados.to_excel('/home/eduardo/AnaliseFIIs/planilhateste.xlsx')
