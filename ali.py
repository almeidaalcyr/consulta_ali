import urllib.request
import json


produtoID = 1005002442302894
produtoID = str(produtoID)
endereco = "https://pt.aliexpress.com/item/"
endereco += produtoID + ".html"

item = 0
cor = ""

reqHttp = urllib.request.FancyURLopener({})
f = reqHttp.open(endereco)
pagina = f.read()

pagina = pagina.split(b'window.runParams')[1]
pagina = pagina.split(b'data: ')[1]
pagina = pagina.decode('utf-8')

produtoDescricao = ""

cont = 0

for i in pagina:
    produtoDescricao += i
    if i == "{":
        cont += 1
    elif i == "}":
        cont -= 1
        if cont == 0:
            break
        
# Salva json em arquivo
JsonArquivo = open(produtoID + ".json",'w')
JsonArquivo.write(produtoDescricao)
JsonArquivo.close()

Json = json.loads(produtoDescricao)

titulo = Json["titleModule"]["subject"]
print(titulo, end="\n\n")

# Imprime skuProp
# for itemNoSku0 in range(len(Json["skuModule"]["productSKUPropertyList"][0]["skuPropertyValues"])):
#     itemNoSku0Id = Json["skuModule"]["productSKUPropertyList"][0]["skuPropertyValues"][itemNoSku0]["propertyValueId"]
#     itemNoSku0Descricao = Json["skuModule"]["productSKUPropertyList"][0]["skuPropertyValues"][itemNoSku0]["propertyValueDefinitionName"]
#     print(itemNoSku0Id,"\t", itemNoSku0Descricao)
    
# for itemNoSku1 in range(len(Json["skuModule"]["productSKUPropertyList"][1]["skuPropertyValues"])):
#     itemNoSku1Id = Json["skuModule"]["productSKUPropertyList"][1]["skuPropertyValues"][itemNoSku1]["propertyValueId"]
#     itemNoSku1Descricao = Json["skuModule"]["productSKUPropertyList"][1]["skuPropertyValues"][itemNoSku1]["propertyValueDefinitionName"]
#     print(itemNoSku1Id,"\t", itemNoSku1Descricao)

for itemNo in range(len(Json["skuModule"]["skuPriceList"])):
    descricao = Json["skuModule"]["skuPriceList"][itemNo]["skuAttr"]
    descricao0 = descricao.split("#")[1].split(";")[0]
    descricao1 = descricao.split("#")[2].split(";")[0]
    
    prodIds = Json["skuModule"]["skuPriceList"][itemNo]["skuPropIds"]
    prodId0 = prodIds.split(",")[0]
    prodId1 = prodIds.split(",")[1]
    
    precoAtivo = Json["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuActivityAmount"]["value"]
    preco = Json["skuModule"]["skuPriceList"][itemNo]["skuVal"]["skuAmount"]["value"]
    qtd = Json["skuModule"]["skuPriceList"][itemNo]["skuVal"]["availQuantity"]
    if qtd > 0:
        print(itemNo, "\t", precoAtivo,"\t",preco,"\t",prodId0,"\t",prodId1," ",descricao0,"\t", descricao1)
