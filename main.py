# Projeto Algorítimos e Lógica de Progração - P1
# Author: Pedro Arthur Maciel Albuquerque

users = []
animals = []
milk_stock = 0
products = []
purchases = []
schedules = []

logged_in = None
user_type = None

while True:
    if logged_in is None:
        print("\n***** Sistema de Gestão Agropecuária - Agropesca Jacaré *****")
        print("1. Login")
        print("2. Cadastrar Usuário")
        print("3. Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == '1':
            username = input("Usuário: ").strip()
            password = input("Senha: ").strip()
            found = False
            for user in users:
                if user[0] == username and user[1] == password:
                    logged_in = username
                    user_type = user[2]
                    print("Bem-vindo, " + username + " (" + user_type + ")!")
                    found = True
                    break
            if not found:
                print("Usuário ou senha inválidos.")

        elif choice == '2':
            username = input("Novo usuário: ").strip()
            password = input("Senha: ").strip()
            utype = input("Tipo (ADM/CLIENTE): ").strip().upper()
            if utype == 'ADM' or utype == 'CLIENTE':
                users.append([username, password, utype])
                print("Usuário cadastrado com sucesso!")
            else:
                print("Tipo inválido. Use ADM ou CLIENTE.")

        elif choice == '3':
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

    else:
        if user_type == 'ADM':
            print("\n***** Menu ADM - " + logged_in + " *****")
            print("1. Gerenciar Rebanho")
            print("2. Gerenciar Produção e Derivados")
            print("3. Relatório")
            print("4. Logout")
            choice = input("Escolha uma opção: ").strip()

            if choice == '1':
                print("\n***** Gerenciar Rebanho *****")
                print("1. Cadastrar Animal")
                print("2. Buscar Animal")
                print("3. Atualizar Animal")
                print("4. Remover Animal")
                print("5. Listar todos os animais")
                subchoice = input("Escolha: ").strip()

                if subchoice == '1':
                    raw_type = input("Tipo (Bovino de Leite, Caprino, Ovino, Suíno/Leitão): ").strip().lower()
                    raw_type = raw_type.replace('ú', 'u').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('ó', 'o').replace('é', 'e')
                    if raw_type == 'bovino de leite':
                        atype = 'Bovino de Leite'
                    elif raw_type == 'caprino':
                        atype = 'Caprino'
                    elif raw_type == 'ovino':
                        atype = 'Ovino'
                    elif raw_type == 'suino/leitão' or raw_type == 'suino/leitao' or raw_type == 'suino leitão' or raw_type == 'suino leitao' or raw_type == 'suino' or raw_type == 'leitão' or raw_type == 'leitao':
                        atype = 'Suíno/Leitão'
                    else:
                        print('Tipo de animal inválido. Use Bovino de Leite, Caprino, Ovino ou Suíno/Leitão.')
                        atype = None

                    if atype is not None:
                        aid = input("ID (brinco/número): ").strip()
                        aweight = input("Peso (kg): ").strip()
                        raw_status = input("Status: ").strip()
                        raw_status_lower = raw_status.lower()
                        raw_status_lower = raw_status_lower.replace('ú', 'u').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('ó', 'o').replace('é', 'e')
                        if raw_status_lower == 'disponivel para venda':
                            astatus = 'Disponível para venda'
                        else:
                            astatus = raw_status
                        animals.append([atype, aid, aweight, astatus])
                        print('Animal cadastrado!')

                elif subchoice == '2':
                    aid = input("ID do animal: ").strip()
                    found = False
                    for animal in animals:
                        if animal[1] == aid:
                            print("Tipo: " + animal[0] + ", Status: " + animal[3])
                            found = True
                            break
                    if not found:
                        print("Animal não encontrado.")

                elif subchoice == '3':
                    aid = input("ID do animal: ").strip()
                    new_status = input("Novo status: ").strip()
                    new_status_lower = new_status.lower()
                    new_status_lower = new_status_lower.replace('ú', 'u').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('ó', 'o').replace('é', 'e')
                    if new_status_lower == 'disponivel para venda':
                        normalized_status = 'Disponível para venda'
                    else:
                        normalized_status = new_status
                    found = False
                    for animal in animals:
                        if animal[1] == aid:
                            animal[3] = normalized_status
                            print('Atualizado!')
                            found = True
                            break
                    if not found:
                        print('Animal não encontrado.')

                elif subchoice == '4':
                    aid = input("ID do animal: ").strip()
                    removed = False
                    i = 0
                    while i < len(animals):
                        if animals[i][1] == aid:
                            del animals[i]
                            print("Removido!")
                            removed = True
                            break
                        i = i + 1
                    if not removed:
                        print("Animal não encontrado.")

                elif subchoice == '5':
                    if len(animals) == 0:
                        print('Nenhum animal cadastrado.')
                    else:
                        print('\n***** Lista de Animais *****')
                        i = 0
                        while i < len(animals):
                            animal = animals[i]
                            print("Tipo: " + animal[0] + ", Peso: " + animal[2] + " kg, Status: " + animal[3])
                            i = i + 1

                else:
                    print("Opção inválida.")

            elif choice == '2':
                print("\n***** Gerenciar Produção *****")
                print("1. Adicionar Leite")
                print("2. Adicionar Produto Derivado")
                subchoice = input("Escolha: ").strip()

                if subchoice == '1':
                    liters_str = input("Litros de leite: ").strip()
                    ok = True
                    if liters_str == '':
                        ok = False
                    if ok:
                        if liters_str.count('-') > 0 or liters_str.count('.') > 1:
                            ok = False
                    i = 0
                    while ok and i < len(liters_str):
                        ch = liters_str[i]
                        if ch != '.' and (ch < '0' or ch > '9'):
                            ok = False
                        i = i + 1
                    if ok:
                        liters = float(liters_str)
                        if liters > 0:
                            milk_stock = milk_stock + liters
                            print("Estoque de leite: " + str(milk_stock) + " L")
                        else:
                            print('Quantidade deve ser maior que zero.')
                    else:
                        print('Valor inválido para litros.')

                elif subchoice == '2':
                    name = input("Nome do produto: ").strip()
                    weight_str = input("Peso (kg): ").strip()
                    value_str = input("Valor de venda: ").strip()
                    ok = True
                    if weight_str == '' or value_str == '':
                        ok = False
                    if ok:
                        if weight_str.count('-') > 0 or weight_str.count('.') > 1 or value_str.count('-') > 0 or value_str.count('.') > 1:
                            ok = False
                    i = 0
                    # Validação manual para garantir que o valor seja um número positivo, permitindo apenas um ponto decimal
                    while ok and i < len(weight_str):
                        ch = weight_str[i]
                        if ch != '.' and (ch < '0' or ch > '9'):
                            ok = False
                        i = i + 1
                    i = 0
                    # Fazemos outro while para o value_str, pois o peso e o valor são validados separadamente
                    while ok and i < len(value_str):
                        ch = value_str[i]
                        if ch != '.' and (ch < '0' or ch > '9'):
                            ok = False
                        i = i + 1
                    if ok:
                        weight = float(weight_str)
                        value = float(value_str) 
                        if weight > 0 and value >= 0:
                            products.append([name, weight, value])
                            print("Produto adicionado!")
                        else:
                            print('Peso deve ser maior que zero e valor não pode ser negativo.')
                    else:
                        print('Valor inválido para peso ou valor.')

                else:
                    print("Opção inválida.")

            elif choice == '3':
                print("\n***** Relatório *****")
                print("Total de animais: " + str(len(animals)))
                print("Estoque de leite: " + str(milk_stock) + " L")
                total_prod_weight = 0
                i = 0
                while i < len(products):
                    total_prod_weight = total_prod_weight + products[i][1]
                    i = i + 1
                print("Peso total de produtos: " + str(total_prod_weight) + " kg")
                total_revenue = 0
                i = 0
                while i < len(purchases):
                    pur = purchases[i]
                    if pur[3] == 'produto':
                        j = 0
                        while j < len(products):
                            if products[j][0] == pur[1]:
                                total_revenue = total_revenue + pur[2] * products[j][2]
                                break
                            j = j + 1
                    i = i + 1
                print("Receita total de produtos vendidos: R$ " + "{:.2f}".format(total_revenue))

            elif choice == '4':
                logged_in = None
                user_type = None
                print("Logout realizado.")

            else:
                print("Opção inválida.")

        else:
            print("\n***** Menu Cliente - " + logged_in + " *****")
            print("1. Visualizar Estoque")
            print("2. Efetuar Compra")
            print("3. Agendar Retirada de Leite")
            print("4. Agendar Retirada de Compras")
            print("5. Histórico de Compras")
            print("6. Logout")
            choice = input("Escolha uma opção: ").strip()

            if choice == '1':
                print("\n***** Estoque *****")
                print("Leite disponível: " + str(milk_stock) + " L")
                print("Produtos disponíveis:")
                available_products = False
                i = 0
                while i < len(products):
                    if products[i][1] > 0:
                        available_products = True
                        print("- " + products[i][0] + ": " + str(products[i][1]) + " kg, R$ " + str(products[i][2]))
                    i = i + 1
                if not available_products:
                    print("Nenhum produto disponível.")
                print("Animais disponíveis:")
                available_animals = False
                i = 0
                while i < len(animals):
                    status = animals[i][3].strip().lower()
                    status = status.replace('ú', 'u').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('ó', 'o').replace('é', 'e')
                    if status == 'disponivel para venda':
                        available_animals = True
                        print("- " + animals[i][0] + ", ID: " + animals[i][1])
                    i = i + 1
                if not available_animals:
                    print("Nenhum animal disponível para venda.")

            elif choice == '2':
                print("\n***** Efetuar Compra *****")
                print("1. Comprar Produto")
                print("2. Comprar Animal")
                print("3. Comprar Leite")
                subchoice = input("Escolha: ").strip()

                if subchoice == '1':
                    available_products = False
                    i = 0
                    while i < len(products):
                        if products[i][1] > 0:
                            available_products = True
                            print("- " + products[i][0] + ": " + str(products[i][1]) + " kg, R$ " + str(products[i][2]))
                        i = i + 1
                    if not available_products:
                        print('Nenhum produto disponível para compra.')
                    else:
                        name = input("Nome do produto: ").strip()
                        qty_str = input("Quantidade (kg): ").strip()
                        ok = True
                        if qty_str == '':
                            ok = False
                        if ok:
                            if qty_str.count('-') > 0 or qty_str.count('.') > 1:
                                ok = False
                        j = 0
                        while ok and j < len(qty_str):
                            ch = qty_str[j]
                            if ch != '.' and (ch < '0' or ch > '9'):
                                ok = False
                            j = j + 1
                        if ok:
                            qty = float(qty_str)
                        else:
                            qty = -1
                        if qty <= 0:
                            print('Quantidade inválida.')
                        else:
                            bought = False
                            i = 0
                            while i < len(products):
                                if products[i][0] == name and products[i][1] >= qty:
                                    products[i][1] = products[i][1] - qty
                                    purchases.append([logged_in, name, qty, 'produto'])
                                    print("Compra realizada!")
                                    bought = True
                                    break
                                i = i + 1
                            if not bought:
                                print("Produto insuficiente ou não encontrado.")

                elif subchoice == '2':
                    available_animals = False
                    i = 0
                    while i < len(animals):
                        if animals[i][3] == 'Disponível para venda':
                            available_animals = True
                            print("- " + animals[i][0] + ", ID: " + animals[i][1])
                        i = i + 1
                    if not available_animals:
                        print('Nenhum animal disponível para venda.')
                    else:
                        aid = input("ID do animal: ").strip()
                        bought = False
                        i = 0
                        while i < len(animals):
                            if animals[i][1] == aid and animals[i][3] == 'Disponível para venda':
                                animals[i][3] = 'Vendido'
                                purchases.append([logged_in, aid, 1, 'animal'])
                                print("Compra realizada!")
                                bought = True
                                break
                            i = i + 1
                        if not bought:
                            print("Animal não disponível.")

                elif subchoice == '3':
                    if milk_stock <= 0:
                        print('Nenhum leite disponível para compra.')
                    else:
                        qty_str = input("Quantidade de leite (L): ").strip()
                        ok = True
                        if qty_str == '':
                            ok = False
                        if ok:
                            if qty_str.count('-') > 0 or qty_str.count('.') > 1:
                                ok = False
                        j = 0
                        while ok and j < len(qty_str):
                            ch = qty_str[j]
                            if ch != '.' and (ch < '0' or ch > '9'):
                                ok = False
                            j = j + 1
                        if ok:
                            qty = float(qty_str)
                        else:
                            qty = -1
                        if qty <= 0:
                            print('Quantidade inválida.')
                        elif qty > milk_stock:
                            print('Não há leite suficiente disponível.')
                        else:
                            milk_stock = milk_stock - qty
                            purchases.append([logged_in, 'Leite', qty, 'leite'])
                            print('Compra de leite realizada!')

                else:
                    print("Opção inválida.")

            elif choice == '3':
                if milk_stock <= 0:
                    print('Nenhum leite disponível para retirada.')
                else:
                    qty_str = input("Quantidade de leite a retirar (máximo " + str(milk_stock) + " L): ").strip()
                    ok = True
                    if qty_str == '':
                        ok = False
                    if ok:
                        if qty_str.count('-') > 0 or qty_str.count('.') > 1:
                            ok = False
                    j = 0
                    while ok and j < len(qty_str):
                        ch = qty_str[j]
                        if ch != '.' and (ch < '0' or ch > '9'):
                            ok = False
                        j = j + 1
                    if ok:
                        qty_to_withdraw = float(qty_str)
                    else:
                        qty_to_withdraw = -1
                    if qty_to_withdraw <= 0 or qty_to_withdraw > milk_stock:
                        print('Quantidade inválida.')
                    else:
                        date = input("Data (DD/MM/AAAA): ").strip()
                        time = input("Horário (HH:MM): ").strip()
                        valid_date = True
                        parts = date.split('/')
                        time_parts = time.split(':')
                        if len(parts) != 3 or len(time_parts) != 2:
                            valid_date = False
                        else:
                            i = 0
                            while valid_date and i < len(parts):
                                if parts[i] == '':
                                    valid_date = False
                                else:
                                    j = 0
                                    while j < len(parts[i]):
                                        ch = parts[i][j]
                                        if ch < '0' or ch > '9':
                                            valid_date = False
                                        j = j + 1
                                i = i + 1
                            i = 0
                            while valid_date and i < len(time_parts):
                                if time_parts[i] == '':
                                    valid_date = False
                                else:
                                    j = 0
                                    while j < len(time_parts[i]):
                                        ch = time_parts[i][j]
                                        if ch < '0' or ch > '9':
                                            valid_date = False
                                        j = j + 1
                                i = i + 1
                            if valid_date:
                                day = int(parts[0])
                                month = int(parts[1])
                                year = int(parts[2])
                                hour = int(time_parts[0])
                                minute = int(time_parts[1])
                                if year < 1 or month < 1 or month > 12 or day < 1 or day > 31:
                                    valid_date = False
                                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                                    valid_date = False
                                if (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
                                    valid_date = False
                                if month == 2:
                                    if day > 29:
                                        valid_date = False
                                    elif day == 29:
                                        if (year % 4 != 0) or (year % 100 == 0 and year % 400 != 0):
                                            valid_date = False
                        if not valid_date:
                            print('Data ou horário inválido. Use formato DD/MM/AAAA e HH:MM.')
                        else:
                            schedules.append([logged_in, 'Leite', qty_to_withdraw, 'leite', date, time])
                            print('Agendamento de retirada de leite realizado!')

            elif choice == '4':
                client_purchases = []
                i = 0
                while i < len(purchases):
                    if purchases[i][0] == logged_in and purchases[i][3] != 'leite':
                        client_purchases.append(purchases[i])
                    i = i + 1
                if len(client_purchases) == 0:
                    print('Você não tem compras de produtos ou animais registradas para agendar retirada.')
                else:
                    print('Compras disponíveis para retirada:')
                    index = 0
                    while index < len(client_purchases):
                        pur = client_purchases[index]
                        print(str(index + 1) + ". " + pur[3] + ": " + str(pur[1]) + ", Qtd: " + str(pur[2]))
                        index = index + 1
                    choice_str = input('Escolha o número da compra: ').strip()
                    if choice_str.isdigit():
                        choice_index = int(choice_str)
                    else:
                        choice_index = -1
                    if choice_index < 1 or choice_index > len(client_purchases):
                        print('Opção inválida.')
                    else:
                        selected = client_purchases[choice_index - 1]
                        qty_str = input("Quantidade a retirar (máximo " + str(selected[2]) + "): ").strip()
                        ok = True
                        if qty_str == '':
                            ok = False
                        if ok:
                            if qty_str.count('-') > 0 or qty_str.count('.') > 1:
                                ok = False
                        j = 0
                        while ok and j < len(qty_str):
                            ch = qty_str[j]
                            if ch != '.' and (ch < '0' or ch > '9'):
                                ok = False
                            j = j + 1
                        if ok:
                            qty_to_withdraw = float(qty_str)
                        else:
                            qty_to_withdraw = -1
                        if qty_to_withdraw <= 0 or qty_to_withdraw > selected[2]:
                            print('Quantidade inválida.')
                        else:
                            date = input("Data (DD/MM/AAAA): ").strip()
                            time = input("Horário (HH:MM): ").strip()
                            valid_date = True
                            parts = date.split('/')
                            time_parts = time.split(':')
                            if len(parts) != 3 or len(time_parts) != 2:
                                valid_date = False
                            else:
                                i = 0
                                while valid_date and i < len(parts):
                                    if parts[i] == '':
                                        valid_date = False
                                    else:
                                        j = 0
                                        while j < len(parts[i]):
                                            ch = parts[i][j]
                                            if ch < '0' or ch > '9':
                                                valid_date = False
                                            j = j + 1
                                    i = i + 1
                                i = 0
                                while valid_date and i < len(time_parts):
                                    if time_parts[i] == '':
                                        valid_date = False
                                    else:
                                        j = 0
                                        while j < len(time_parts[i]):
                                            ch = time_parts[i][j]
                                            if ch < '0' or ch > '9':
                                                valid_date = False
                                            j = j + 1
                                    i = i + 1
                                if valid_date:
                                    day = int(parts[0])
                                    month = int(parts[1])
                                    year = int(parts[2])
                                    hour = int(time_parts[0])
                                    minute = int(time_parts[1])
                                    if year < 1 or month < 1 or month > 12 or day < 1 or day > 31:
                                        valid_date = False
                                    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                                        valid_date = False
                                    if (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
                                        valid_date = False
                                    if month == 2:
                                        if day > 29:
                                            valid_date = False
                                        elif day == 29:
                                            if (year % 4 != 0) or (year % 100 == 0 and year % 400 != 0):
                                                valid_date = False
                            if not valid_date:
                                print('Data ou horário inválido. Use formato DD/MM/AAAA e HH:MM.')
                            else:
                                schedules.append([logged_in, selected[1], qty_to_withdraw, selected[3], date, time])
                                print('Agendamento realizado!')

            elif choice == '5':
                print("\n***** Histórico de Compras *****")
                has_history = False
                i = 0
                while i < len(purchases):
                    if purchases[i][0] == logged_in:
                        print("- " + purchases[i][3] + ": " + str(purchases[i][1]) + ", Qtd: " + str(purchases[i][2]))
                        has_history = True
                    i = i + 1
                if not has_history:
                    print('Nenhuma compra registrada.')
                print('\n***** Retiradas Agendadas *****')
                has_schedules = False
                i = 0
                while i < len(schedules):
                    if schedules[i][0] == logged_in:
                        print("- " + schedules[i][3] + ": " + str(schedules[i][1]) + ", Qtd: " + str(schedules[i][2]) + ", " + schedules[i][4] + " " + schedules[i][5])
                        has_schedules = True
                    i = i + 1
                if not has_schedules:
                    print('Nenhum agendamento de retirada.')

            elif choice == '6':
                logged_in = None
                user_type = None
                print("Logout realizado.")

            else:
                print("Opção inválida.")
