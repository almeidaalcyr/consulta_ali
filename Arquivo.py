#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:18:53 2022

@author: alcyr
"""

import pathlib
import os.path
import time

class Arquivo:
    minuto = 60
    hora = minuto * 60
    dia = hora * 24
    
    def getUltimaAlteracao(arquivo):
        if Arquivo.verificaArquivoExiste(arquivo) == True:
            arquivo = pathlib.Path(arquivo)
            return arquivo.stat().st_mtime
        else:
             #Se o arquivo não existe, retorna o tempo atual
             return 0
        
    def verificaArquivoExiste(arquivo):
        return os.path.isfile(arquivo)