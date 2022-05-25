#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:18:53 2022

@author: alcyr
"""

import pathlib

class Arquivo:
    def getDataCriacao(arquivo):
        file = pathlib.Path(arquivo)
        print(file.stat())
        
Arquivo.getDataCriacao("ali.py")