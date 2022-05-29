import urllib.request
import json
import time
from Arquivo import Arquivo

class Consulta_aliexpress:
    def __init__(self, produtoId):
        self.produtoId = str(produtoId)
        self.jsonProduto = self.__carregaJson()
        self.qtdAtributos = len(self.jsonProduto["skuModule"]["productSKUPropertyList"])

    def __carregaJson(self):
        if Arquivo.getUltimaAlteracao(self.produtoId+".json") < time.time() - Arquivo.dia:
            print("Baixando arquivo")
            endereco = "https://pt.aliexpress.com/item/"
            endereco += self.produtoId + ".html"

            reqHttp = urllib.request.FancyURLopener({})
            f = reqHttp.open(endereco)
            html = f.read()

            html = html.split(b'window.runParams')[1]
            html = html.split(b'data: ')[1]
            html = html.decode('utf-8')

            Json = ""
            cont = 0

            for i in html:
                Json += i
                if i == "{":
                    cont += 1
                elif i == "}":
                    cont -= 1
                    if cont == 0:
                        break

            self.salvaArquivo(Json, self.produtoId, ".json")

        else:
            Json = self.carregaArquivo()

        Json = json.loads(Json)
        return Json

    def getTitulo(self):
        return self.jsonProduto["titleModule"]["subject"]

    def carregaArquivo(self):
        arquivo = open(self.produtoId+".json",'r')
        return arquivo.read()


    def salvaArquivo(self, conteudo, nome, formato):
        arquivo = open(nome + formato,'w')
        arquivo.write(conteudo)
        arquivo.close()

    def consultaPreco(self, atributo0, atributo1 = -1):
        for itemNo in range(len(self.jsonProduto["skuModule"]["skuPriceList"])):
            prodIds = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuPropIds"]
            prodId0 = prodIds.split(",")[0]

            prodId1 = prodIds.split(",")[1] if self.qtdAtributos > 2 else -1

            if str(prodId0) == str(atributo0) and str(prodId1) == str(atributo1):
                descricao = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuAttr"]
                descricao0 = descricao.split("#")[1].split(";")[0]

                descricao1 = descricao.split("#")[2].split(";")[0] if self.qtdAtributos > 2 else -1

                precoAtivo = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuActivityAmount"]["value"]
                preco = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuAmount"]["value"]
                qtd = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["availQuantity"]
                if qtd > 0:
                    return (itemNo, precoAtivo, preco, prodId0, prodId1, descricao0, descricao1)
                else:
                    print("Produto sem estoque")
                    return
                break

        print("produto não encontrado")
        return

    def listaOpcoes(self):
        opcoes = []
        for itemNo in range(len(self.jsonProduto["skuModule"]["skuPriceList"])):
            descricao = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuAttr"]
            descricao0 = descricao.split("#")[1].split(";")[0]

            descricao1 = descricao.split("#")[2].split(";")[0] if self.qtdAtributos > 2 else -1

            prodIds = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuPropIds"]
            prodId0 = prodIds.split(",")[0]

            prodId1 = prodIds.split(",")[1] if self.qtdAtributos > 2 else -1

            precoAtivo = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuActivityAmount"]["value"]
            preco = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuAmount"]["value"]
            qtd = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["availQuantity"]
            if qtd > 0:
                opcoes.append((itemNo, precoAtivo, preco, prodId0, prodId1, descricao0, descricao1))
        return opcoes

    def getAtributos(self, ordemItem):
        prodIds = self.jsonProduto["skuModule"]["skuPriceList"][ordemItem]["skuPropIds"]
        atributo0 = int(prodIds.split(",")[0])
        atributo1 = int(prodIds.split(",")[1]) if self.qtdAtributos > 2 else -1

        return (atributo0, atributo1)

# cel = Consulta_aliexpress(1005002442302894)
# cel.listaOpcoes()
# item = 7
# cel.consultaPreco(cel.getAtributos(item)[0],cel.getAtributos(item)[1])
