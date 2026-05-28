# Projeto Algorítimos e Lógica de Progração - P1
# Author: Pedro Arthur Maciel Albuquerque

users = []
animals = []
milk_stock = []
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
                        aprice_str = input("Preço de venda (R$): ").strip()
                        raw_status = input("Status: ").strip()
                        raw_status_lower = raw_status.lower()
                        raw_status_lower = raw_status_lower.replace('ú', 'u').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('ó', 'o').replace('é', 'e')
                        if raw_status_lower == 'disponivel para venda':
                            astatus = 'Disponível para venda'
                        else:
                            astatus = raw_status
                        duplicate_id = False
                        j = 0
                        while j < len(animals):
                            if animals[j][2] == aid:
                                duplicate_id = True
                                break
                            j = j + 1
                        if duplicate_id:
                            print('Já existe um animal com este ID.')
                        else:
                            v_weight = True
                            dot_c = 0
                            if aweight == "" or aweight == ".": v_weight = False
                            k = 0
                            while k < len(aweight):
                                char = aweight[k]
                                if char == ".": dot_c = dot_c + 1
                                elif not char.isdigit():
                                    v_weight = False
                                    break
                                k = k + 1
                            if dot_c > 1: v_weight = False

                            # Validação manual preço animal
                            v_aprice = True
                            dot_c = 0
                            if aprice_str == "" or aprice_str == ".": v_aprice = False
                            else:
                                k = 0
                                while k < len(aprice_str):
                                    if aprice_str[k] == ".": dot_c = dot_c + 1
                                    elif not aprice_str[k].isdigit(): v_aprice = False; break
                                    k = k + 1
                                if dot_c > 1: v_aprice = False

                            if v_weight and v_aprice:
                                animals.append([logged_in, atype, aid, aweight, astatus, float(aprice_str)])
                                print('Animal cadastrado com preço de R$ ' + aprice_str)
                            else:
                                print('Peso ou Preço inválido.')

                elif subchoice == '2':
                    aid = input("ID do animal: ").strip()
                    found = False
                    for animal in animals:
                        if animal[2] == aid:
                            print("Tipo: " + animal[1] + ", Status: " + animal[4])
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
                        if animal[2] == aid:
                            animal[4] = normalized_status
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
                        if animals[i][2] == aid:
                            animals.pop(i)
                            removed = True
                            break
                        else:
                            i = i + 1
                    if removed:
                        print("Removido!")
                    else:
                        print("Animal não encontrado.")

                elif subchoice == '5':
                    if len(animals) == 0:
                        print('Nenhum animal cadastrado.')
                    else:
                        print('\n***** Lista de Animais *****')
                        i = 0
                        while i < len(animals):
                            # Mostrar apenas animais do ADM logado
                            if animals[i][0] == logged_in:
                                print("Tipo: " + animals[i][1] + ", Peso: " + animals[i][3] + " kg, Status: " + animals[i][4] + ", Preço: R$ " + str(animals[i][5]))
                            i = i + 1

                else:
                    print("Opção inválida.")

            elif choice == '2':
                print("\n***** Gerenciar Produção *****")
                print("1. Adicionar Leite")
                print("2. Adicionar Produto Derivado")
                print("3. Listar Produtos e Leite")
                subchoice = input("Escolha: ").strip()

                if subchoice == '1':
                    liters_str = input("Litros de leite: ").strip()
                    mprice_str = input("Preço por litro (R$): ").strip()
                    v_liters = True
                    dot_c = 0
                    if liters_str == "" or liters_str == ".": v_liters = False
                    k = 0
                    while k < len(liters_str):
                        char = liters_str[k]
                        if char == ".": dot_c = dot_c + 1
                        elif not char.isdigit():
                            v_liters = False
                            break
                        k = k + 1
                    if dot_c > 1: v_liters = False

                    v_mprice = True
                    dot_c = 0
                    if mprice_str == "" or mprice_str == ".": v_mprice = False
                    else:
                        k = 0
                        while k < len(mprice_str):
                            if mprice_str[k] == ".": dot_c = dot_c + 1
                            elif not mprice_str[k].isdigit(): v_mprice = False; break
                            k = k + 1
                        if dot_c > 1: v_mprice = False

                    if v_liters and v_mprice:
                        liters = float(liters_str)
                        mprice = float(mprice_str)
                        if liters > 0:
                            found = False
                            i = 0
                            while i < len(milk_stock):
                                if milk_stock[i][0] == logged_in:
                                    milk_stock[i][1] = milk_stock[i][1] + liters
                                    milk_stock[i][2] = mprice # Atualiza preço
                                    found = True
                                    break
                                i = i + 1
                            if not found:
                                milk_stock.append([logged_in, liters, mprice])
                            print("Estoque de leite atualizado!")
                        else:
                            print('Quantidade deve ser maior que zero.')
                    else:
                        print('Valores inválidos.')

                elif subchoice == '2':
                    name = input("Nome do produto: ").strip()
                    units_str = input("Quantidade de unidades: ").strip()
                    w_per_unit_str = input("Peso por unidade (kg): ").strip()
                    price_str = input("Preço de venda (R$ por kg): ").strip()
                    derived = input("É derivado de leite? (s/n): ").strip().lower()
                    
                    # Validação manual de todas as entradas
                    v_all = True
                    
                    # Valida unidades (inteiro)
                    if units_str == "": v_all = False
                    else:
                        k = 0
                        while k < len(units_str):
                            if not units_str[k].isdigit(): v_all = False; break
                            k = k + 1
                    
                    # Valida peso e preço (float)
                    for val_str in [w_per_unit_str, price_str]:
                        dot_c = 0
                        if val_str == "" or val_str == ".": v_all = False; break
                        k = 0
                        while k < len(val_str):
                            if val_str[k] == ".": dot_c = dot_c + 1
                            elif not val_str[k].isdigit(): v_all = False; break
                            k = k + 1
                        if dot_c > 1: v_all = False; break
                    
                    if v_all:
                        units = int(units_str)
                        w_unit = float(w_per_unit_str)
                        price = float(price_str)
                        total_weight = units * w_unit
                        
                        can_add = True
                        milk_total = 0.0
                        
                        if derived == 's':
                            m_unit_str = input("Litros de leite por unidade: ").strip()
                            # Validação manual leite
                            v_m = True
                            dot_c = 0
                            if m_unit_str == "" or m_unit_str == ".": v_m = False
                            else:
                                k = 0
                                while k < len(m_unit_str):
                                    if m_unit_str[k] == ".": dot_c = dot_c + 1
                                    elif not m_unit_str[k].isdigit(): v_m = False; break
                                    k = k + 1
                                if dot_c > 1: v_m = False
                            
                            if v_m:
                                m_unit = float(m_unit_str)
                                milk_total = units * m_unit
                                # Verificar estoque
                                found = False
                                i = 0
                                while i < len(milk_stock): 
                                    if milk_stock[i][0] == logged_in: 
                                        if milk_stock[i][1] >= milk_total:
                                            milk_stock[i][1] = milk_stock[i][1] - milk_total
                                            found = True
                                        else:
                                            print('Leite insuficiente para produzir ' + str(units) + ' unidades.')
                                            can_add = False
                                        break
                                    i = i + 1
                                if not found and milk_total > 0:
                                    print('Não há leite para produzir.')
                                    can_add = False
                            else:
                                print('Quantidade de leite inválida.')
                                can_add = False

                        if can_add:
                            products.append([logged_in, name, total_weight, price, int(derived == 's'), milk_total])
                            print("Produção concluída: " + str(total_weight) + " kg de " + name + " adicionados!")
                    else:
                        print('Entradas inválidas. Use apenas números.')

                elif subchoice == '3':
                    print("\n***** Estoque de Produção (Seu) *****")
                    # Leite
                    found_milk = False
                    i = 0
                    while i < len(milk_stock):
                        if milk_stock[i][0] == logged_in:
                            print("Leite: " + str(milk_stock[i][1]) + " L (Preço: R$ " + str(milk_stock[i][2]) + "/L)")
                            found_milk = True
                            break
                        i = i + 1
                    if not found_milk:
                        print("Leite: 0 L")
                    
                    # Produtos
                    print("Produtos:")
                    found_prod = False
                    i = 0
                    while i < len(products):
                        if products[i][0] == logged_in:
                            d_str = ""
                            if products[i][4] == 1:
                                d_str = " (Derivado)"
                            print("- " + products[i][1] + ": " + str(products[i][2]) + " kg, R$ " + str(products[i][3]) + d_str)
                            found_prod = True
                        i = i + 1
                    if not found_prod:
                        print("- Nenhum produto cadastrado.")

                else:
                    print("Opção inválida.")

            elif choice == '3':
                print("\n***** Relatório *****")
                animal_count = 0
                i = 0
                while i < len(animals):
                    if animals[i][0] == logged_in:
                        animal_count = animal_count + 1
                    i = i + 1
                print("Total de animais: " + str(animal_count))
                milk_amount = 0
                i = 0
                while i < len(milk_stock):
                    if milk_stock[i][0] == logged_in:
                        milk_amount = milk_amount + milk_stock[i][1]
                    i = i + 1
                print("Estoque de leite: " + str(milk_amount) + " L")
                total_prod_weight = 0
                i = 0
                while i < len(products):
                    if products[i][0] == logged_in:
                        total_prod_weight = total_prod_weight + products[i][2]
                    i = i + 1
                print("Peso total de produtos: " + str(total_prod_weight) + " kg")
                total_revenue = 0
                i = 0
                while i < len(purchases):
                    if purchases[i][4] == logged_in and len(purchases[i]) > 5:
                        total_revenue = total_revenue + (purchases[i][2] * purchases[i][5])
                    i = i + 1
                print("Receita Total (Produtos, Animais e Leite): R$ " + "{:.2f}".format(total_revenue))

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
            print("3. Histórico de Compras e Retiradas")
            print("4. Logout")
            choice = input("Escolha uma opção: ").strip()

            if choice == '1':
                print("\n***** Estoque *****")
                total_milk = 0
                i = 0
                while i < len(milk_stock):
                    total_milk = total_milk + milk_stock[i][1]
                    print("- ADM: " + milk_stock[i][0] + " | Qtd: " + str(milk_stock[i][1]) + " L | Preço: R$ " + str(milk_stock[i][2]) + "/L")
                    i = i + 1
                print("Total de leite disponível: " + str(total_milk) + " L")
                print("Produtos disponíveis:")
                available_products = False
                i = 0
                while i < len(products):
                    if products[i][2] > 0:
                        available_products = True
                        print("- " + products[i][1] + " (ADM: " + products[i][0] + "): " + str(products[i][2]) + " kg, R$ " + str(products[i][3]))
                    i = i + 1
                if not available_products:
                    print("Nenhum produto disponível.")
                print("Animais disponíveis:")
                available_animals = False
                i = 0
                while i < len(animals):
                    status = animals[i][4].strip().lower()
                    status = status.replace('ú', 'u').replace('í', 'i').replace('ã', 'a').replace('ç', 'c').replace('ó', 'o').replace('é', 'e')
                    if status == 'disponivel para venda':
                        available_animals = True
                        print("- " + animals[i][1] + ", ID: " + animals[i][2] + " (ADM: " + animals[i][0] + ") - Preço: R$ " + str(animals[i][5]))
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
                        if products[i][2] > 0:
                            available_products = True
                            print("- " + products[i][1] + " (ADM: " + products[i][0] + "): " + str(products[i][2]) + " kg, R$ " + str(products[i][3]))
                        i = i + 1
                    if not available_products:
                        print('Nenhum produto disponível para compra.')
                    else:
                        name = input("Nome do produto: ").strip()
                        qty_str = input("Quantidade (kg): ").strip()
                        
                        # Validação manual float qty_str (verifica se é um número válido e maior que 0)
                        v_qty = True
                        dot_c = 0
                        if qty_str == "" or qty_str == ".": v_qty = False
                        k = 0
                        while k < len(qty_str):
                            if qty_str[k] == ".": dot_c = dot_c + 1
                            elif not qty_str[k].isdigit(): v_qty = False; break
                            k = k + 1
                        if dot_c > 1: v_qty = False

                        if v_qty:
                            qty = float(qty_str)
                            if qty <= 0:
                                print('Quantidade inválida.')
                            else:
                                # Listar vendedores para este produto
                                print("Vendedores disponíveis para " + name + ":")
                                i = 0
                                found_any = False
                                while i < len(products):
                                    if products[i][1] == name and products[i][2] >= qty:
                                        print("- " + products[i][0] + " | R$ " + str(products[i][3]) + "/kg")
                                        found_any = True
                                    i = i + 1
                                
                                if not found_any:
                                    print("Nenhum vendedor com estoque suficiente para este produto.")
                                else:
                                    target_adm = input("De qual vendedor deseja comprar? (Nome): ").strip()
                                    bought = False
                                    i = 0
                                    while i < len(products):
                                        if products[i][1] == name and products[i][0] == target_adm and products[i][2] >= qty:
                                            adm_name = products[i][0]
                                            price = products[i][3]
                                            
                                            print("Agende a retirada agora:")
                                            date = input("Data (DD/MM/AAAA): ").strip()
                                            time = input("Horário (HH:MM): ").strip()
                                            
                                            # Validação de Data Manual
                                            v_date = True
                                            d_parts = date.split('/')
                                            t_parts = time.split(':')
                                            if len(d_parts) != 3 or len(t_parts) != 2:
                                                v_date = False
                                            else:
                                                # Checar se partes são numéricas manualmente
                                                v_num = True
                                                for part in [d_parts[0], d_parts[1], d_parts[2], t_parts[0], t_parts[1]]:
                                                    if part == "": v_num = False; break
                                                    if not part.isdigit(): v_num = False; break
                                                
                                                if v_num:
                                                    dd = int(d_parts[0]); mm = int(d_parts[1]); yy = int(d_parts[2])
                                                    hh = int(t_parts[0]); mn = int(t_parts[1])
                                                    if yy < 2026 or (yy == 2026 and mm < 5) or (yy == 2026 and mm == 5 and dd < 11): v_date = False
                                                    if mm < 1 or mm > 12 or dd < 1 or dd > 31: v_date = False
                                                    if (mm == 4 or mm == 6 or mm == 9 or mm == 11) and dd > 30: v_date = False
                                                    if mm == 2 and dd > 29: v_date = False
                                                    if mm == 2 and dd == 29 and not (yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0)): v_date = False
                                                    if hh < 0 or hh > 23 or mn < 0 or mn > 59: v_date = False
                                                else:
                                                    v_date = False
                                            
                                            if v_date:
                                                products[i][2] = products[i][2] - qty
                                                purchases.append([logged_in, name, qty, 'produto', adm_name, price])
                                                schedules.append([logged_in, name, qty, 'produto', date, time])
                                                print("Compra e agendamento realizados!")
                                                bought = True
                                            else:
                                                print("Data/hora inválida ou retroativa. Compra cancelada.")
                                                bought = True # prevent not found message
                                            break
                                        i = i + 1
                                if not bought:
                                    print("Produto insuficiente ou não encontrado.")
                        else:
                            print('Quantidade inválida.')

                elif subchoice == '2':
                    available_animals = False
                    i = 0
                    while i < len(animals):
                        if animals[i][4] == 'Disponível para venda':
                            available_animals = True
                            print("- " + animals[i][1] + ", ID: " + animals[i][2] + " (ADM: " + animals[i][0] + ")")
                        i = i + 1
                    if not available_animals:
                        print('Nenhum animal disponível para venda.')
                    else:
                        aid = input("ID do animal: ").strip()
                        bought = False
                        i = 0
                        while i < len(animals):
                            if animals[i][2] == aid and animals[i][4] == 'Disponível para venda':
                                print("Agende a retirada agora:")
                                date = input("Data (DD/MM/AAAA): ").strip()
                                time = input("Horário (HH:MM): ").strip()
                                v_date = True
                                d_parts = date.split('/')
                                t_parts = time.split(':')
                                if len(d_parts) != 3 or len(t_parts) != 2: v_date = False
                                else:
                                    v_num = True
                                    for part in [d_parts[0], d_parts[1], d_parts[2], t_parts[0], t_parts[1]]:
                                        if part == "": v_num = False; break
                                        if not part.isdigit(): v_num = False; break
                                    
                                    if v_num:
                                        dd = int(d_parts[0]); mm = int(d_parts[1]); yy = int(d_parts[2])
                                        hh = int(t_parts[0]); mn = int(t_parts[1])
                                        if yy < 2026 or (yy == 2026 and mm < 5) or (yy == 2026 and mm == 5 and dd < 11): v_date = False
                                        if mm < 1 or mm > 12 or dd < 1 or dd > 31: v_date = False
                                        if (mm == 4 or mm == 6 or mm == 9 or mm == 11) and dd > 30: v_date = False
                                        if mm == 2 and dd > 29: v_date = False
                                        if mm == 2 and dd == 29 and not (yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0)): v_date = False
                                        if hh < 0 or hh > 23 or mn < 0 or mn > 59: v_date = False
                                    else:
                                        v_date = False
                                
                                if v_date:
                                    animals[i][4] = 'Vendido'
                                    # Grava o preço definido pelo ADM
                                    purchases.append([logged_in, aid, 1, 'animal', animals[i][0], animals[i][5]])
                                    schedules.append([logged_in, aid, 1, 'animal', date, time])
                                    print("Compra e agendamento realizados! Preço: R$ " + str(animals[i][5]))
                                    bought = True
                                else:
                                    print("Data/hora inválida ou retroativa. Compra cancelada.")
                                    bought = True
                                break
                            i = i + 1
                        if not bought:
                            print("Animal não disponível.")

                elif subchoice == '3':
                    total_milk = 0
                    i = 0
                    while i < len(milk_stock):
                        total_milk = total_milk + milk_stock[i][1]
                        i = i + 1
                    if total_milk <= 0:
                        print('Nenhum leite disponível para compra.')
                    else:
                        qty_str = input("Quantidade (L): ").strip()
                        
                        # Validação manual float qty_str
                        v_qty = True
                        dot_c = 0
                        if qty_str == "" or qty_str == ".": v_qty = False
                        k = 0
                        while k < len(qty_str):
                            if qty_str[k] == ".": dot_c = dot_c + 1
                            elif not qty_str[k].isdigit(): v_qty = False; break
                            k = k + 1
                        if dot_c > 1: v_qty = False

                        if v_qty:
                            qty = float(qty_str)
                            if qty <= 0 or qty > total_milk:
                                print('Quantidade inválida ou superior ao estoque.')
                            else:
                                print("Agende a retirada agora:")
                                date = input("Data (DD/MM/AAAA): ").strip()
                                time = input("Horário (HH:MM): ").strip()
                                v_date = True
                                d_parts = date.split('/')
                                t_parts = time.split(':')
                                if len(d_parts) != 3 or len(t_parts) != 2: v_date = False
                                else:
                                    v_num = True
                                    for part in [d_parts[0], d_parts[1], d_parts[2], t_parts[0], t_parts[1]]:
                                        if part == "": v_num = False; break
                                        if not part.isdigit(): v_num = False; break

                                    if v_num:
                                        dd = int(d_parts[0]); mm = int(d_parts[1]); yy = int(d_parts[2])
                                        hh = int(t_parts[0]); mn = int(t_parts[1])
                                        if yy < 2026 or (yy == 2026 and mm < 5) or (yy == 2026 and mm == 5 and dd < 11): v_date = False
                                        if mm < 1 or mm > 12 or dd < 1 or dd > 31: v_date = False
                                        if (mm == 4 or mm == 6 or mm == 9 or mm == 11) and dd > 30: v_date = False
                                        if mm == 2 and dd > 29: v_date = False
                                        if mm == 2 and dd == 29 and not (yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0)): v_date = False
                                        if hh < 0 or hh > 23 or mn < 0 or mn > 59: v_date = False
                                    else:
                                        v_date = False
                                
                                if v_date:
                                    # Listar vendedores de leite
                                    print("Vendedores de Leite disponíveis:")
                                    i = 0
                                    while i < len(milk_stock):
                                        if milk_stock[i][1] > 0:
                                            print("- ADM: " + milk_stock[i][0] + " | Qtd: " + str(milk_stock[i][1]) + " L | Preço: R$ " + str(milk_stock[i][2]) + "/L")
                                        i = i + 1
                                    
                                    target_adm = input("De qual vendedor deseja comprar? (Nome): ").strip()
                                    
                                    # Processar compra do vendedor escolhido
                                    found_adm = False
                                    i = 0
                                    while i < len(milk_stock):
                                        if milk_stock[i][0] == target_adm:
                                            if milk_stock[i][1] >= qty:
                                                price_l = milk_stock[i][2]
                                                purchases.append([logged_in, 'Leite', qty, 'leite', target_adm, price_l])
                                                schedules.append([logged_in, 'Leite', qty, 'leite', date, time])
                                                milk_stock[i][1] = milk_stock[i][1] - qty
                                                print('Compra de leite do ADM ' + target_adm + ' realizada!')
                                                found_adm = True
                                            else:
                                                print('O ADM ' + target_adm + ' não possui leite suficiente.')
                                                found_adm = True # Encontrou o ADM, mas estoque falhou
                                            break
                                        i = i + 1
                                    
                                    if not found_adm:
                                        print('Vendedor não encontrado.')
                                else:
                                    print("Data/hora inválida ou retroativa. Compra cancelada.")
                        else:
                            print('Quantidade inválida.')

                else:
                    print("Opção inválida.")

            elif choice == '3':
                print("\n***** Histórico de Compras *****")
                has_history = False
                i = 0
                while i < len(purchases):
                    if purchases[i][0] == logged_in:
                        print("- " + purchases[i][3] + ": " + str(purchases[i][1]) + ", Qtd: " + str(purchases[i][2]) + ", Vendedor: " + purchases[i][4])
                        has_history = True
                    i = i + 1
                if not has_history:
                    print('Nenhuma compra registrada.')
                print('\n***** Retiradas Agendadas *****')
                has_schedules = False
                i = 0
                while i < len(schedules):
                    if schedules[i][0] == logged_in:
                        print("- " + schedules[i][3] + ": " + str(schedules[i][1]) + ", Qtd: " + str(schedules[i][2]) + ", Data: " + schedules[i][4] + " " + schedules[i][5])
                        has_schedules = True
                    i = i + 1
                if not has_schedules:
                    print('Nenhum agendamento de retirada.')

            elif choice == '4':
                logged_in = None
                user_type = None
                print("Logout realizado.")

            else:
                print("Opção inválida.")
