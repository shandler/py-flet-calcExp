import flet as ft
from flet import Text, TextField, Row, Slider, ElevatedButton, ResponsiveRow, Column
import random
import re
import sqlite3

def operacao(a, s, b):
    if s == '+':
        return float(a) + float(b)
    elif s == '-':
        return float(a) - float(b)
    elif s == '*':
        return float(a) * float(b)
    elif s == '/':
        return float(a) / float(b)

def resolve(expressao):
    tokens = re.findall(r'\d+|\S', expressao)
    historico = []
    while len(tokens) != 1:
        op = operacao(tokens[0],tokens[1],tokens[2])
        historico.append(tokens[0]+' '+tokens[1]+' '+tokens[2]+' = '+str(op))
        for i in range(3):
            del tokens[0]
        tokens.insert(0,str(op))
    return float(tokens[0]), historico

def gerar_expressao(num_numeros=3):
    while True:
        if num_numeros < 2:
            raise ValueError("O número de números na expressão deve ser pelo menos 2.")
        numeros = [str(random.randint(1, 10)) for _ in range(num_numeros)]
        operadores = random.choices("+-*/", k=num_numeros - 1)
        expressao = f"{numeros[0]}"
        for i in range(num_numeros - 1):
            expressao += f" {operadores[i]} {numeros[i + 1]}"
        numero,_ = resolve(expressao)
        if (numero // 1 == numero):  
            return expressao
        
def main(page):
    con = sqlite3.connect("mat_exp.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE historico(expresao, , score)")


    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    def slider_changed(e):
        quantidade.value = int(e.control.value)
        expressaoGerada.value = gerar_expressao(int(quantidade.value))
        page.update()

    def text_changed(e):
         expressaoGerada.value = gerar_expressao(int(quantidade.value))
         page.update()

    # def gerar(e):
    #     # expressaoGerada.value = gerar_expressao(int(quantidade.value))
    #     page.update()

    def resolveExp(e):
        resultado.value, hist = resolve(expressaoGerada.value)
        tmp_text = ''
        for item in hist:
            tmp_text += '{}\n'.format(item)
        resolucao.value = tmp_text
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("Calcula Expressão"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Gerar Expressão"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )
    
    separacao = Text("")
    expressaoGerada = TextField(label="Resolva a Expressão", autofocus=True)
    quantidade = TextField(label="Quantidade de Números", width=200, on_change=text_changed)
    mudaquant = Slider(min=1, max=20, divisions=20, label="{value}", on_change=slider_changed)
    #geraExpressao = ElevatedButton("Gerar Expressão", on_click=gerar, data=0)
    resolveExpressao = ElevatedButton("Resolve Expressão", on_click=resolveExp, data=0)
    resultado = Text(
            "Resultado",
            size=50,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_700,
            weight=ft.FontWeight.BOLD,
            italic=True,
    )
    resolucao = TextField(
            label="Resolução da Expressão",
            multiline=True,
            
            min_lines=1,
            max_lines=15, expand=True
    )
    page.add(
        ResponsiveRow([
            Column(col={"sm": 12}, controls=[separacao])
        ]),
        ResponsiveRow([
            Column(col={"sm": 12}, controls=[expressaoGerada])
        ]),
        ResponsiveRow([
            Column(col={"sm": 6}, controls = [quantidade]),
            Column(col={"sm": 6}, controls = [mudaquant]),
            # Column(col={"sm": 4}, controls = [geraExpressao])   
        ]),
        ResponsiveRow([
            Column(col={"sm": 6}, controls = [resolveExpressao]),
            Column(col={"sm": 6}, controls = [resultado])                                 
        ]),
        ResponsiveRow([
            Column(col={"sm": 12}, controls = [resolucao])
        ]),
        ResponsiveRow([
            Column(col={"sm": 12}, controls=[separacao])
        ])
    )

ft.app(target=main)