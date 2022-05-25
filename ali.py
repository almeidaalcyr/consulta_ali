import urllib.request
import json
import time
from Arquivo import Arquivo

class consulta_aliexpress:
    def __init__(self, produtoId):
        self.produtoId = str(produtoId)
        self.jsonProduto = self.carregaJson()
        
    def carregaJson(self):
        if Arquivo.getUltimaAlteracao(self.produtoId+".json") > time.time() - Arquivo.dia:
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
            Json = json.loads(Json)
            
        else:
            Json = self.carregaArquivo(self.produtoId+".json")
            
        return Json
    
    def carregaArquivo(self):
        arquivo = open(self.produtoId+".json",'r')
        return arquivo.buffer()
        
        
    def salvaArquivo(self, conteudo, nome, formato):
        arquivo = open(nome + formato,'w')
        arquivo.write(conteudo)
        arquivo.close()
    
    def consultaPreco(self, atributo0, atributo1):
        for itemNo in range(len(self.jsonProduto["skuModule"]["skuPriceList"])):
            
            prodIds = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuPropIds"]
            prodId0 = prodIds.split(",")[0]
            prodId1 = prodIds.split(",")[1]
            
            if prodId0 == str(atributo0) and prodId1 == str(atributo1):
                descricao = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuAttr"]
                descricao0 = descricao.split("#")[1].split(";")[0]
                descricao1 = descricao.split("#")[2].split(";")[0]
                
                precoAtivo = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuActivityAmount"]["value"]
                preco = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuAmount"]["value"]
                qtd = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["availQuantity"]
                if qtd > 0:
                    print(itemNo, "\t", precoAtivo,"\t",preco,"\t",prodId0,"\t",prodId1," ",
                          descricao0,"\t", descricao1)
                    return
                else:
                    print("Produto sem estoque")
                    return
                break
            
        print("produto não encontrado")
        return

    def listaOpcoes(self):
        for itemNo in range(len(self.jsonProduto["skuModule"]["skuPriceList"])):
            descricao = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuAttr"]
            descricao0 = descricao.split("#")[1].split(";")[0]
            descricao1 = descricao.split("#")[2].split(";")[0]

            prodIds = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuPropIds"]
            prodId0 = prodIds.split(",")[0]
            prodId1 = prodIds.split(",")[1]

            precoAtivo = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuActivityAmount"]["value"]
            preco = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuAmount"]["value"]
            qtd = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuVal"]["availQuantity"]
            if qtd > 0:
                print(itemNo, "\t", precoAtivo,"\t",preco,"\t",prodId0,"\t",prodId1," ",
                      descricao0,"\t", descricao1)

    def getAtributos(self, itemNo):
        prodIds = self.jsonProduto["skuModule"]["skuPriceList"][itemNo]["skuPropIds"]
        atributo0 = prodIds.split(",")[0]
        atributo1 = prodIds.split(",")[1]
        print((atributo0, atributo1))
        return (atributo0, atributo1)
        

cel = consulta_aliexpress(1005002442302894)
cel.carregaArquivo()
#cel.listaOpcoes()
#cel.consultaPreco(200003982, 29)
#cel.getAtributos(7)