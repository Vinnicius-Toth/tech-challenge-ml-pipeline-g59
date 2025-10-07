def gerar_lista_anomes(anos_disponiveis, meses_disponiveis, anomes_list=[]):
    for ano in anos_disponiveis:
        for mes in meses_disponiveis:
            anomes_list.append(f"{ano}{mes.value}")
    return anomes_list