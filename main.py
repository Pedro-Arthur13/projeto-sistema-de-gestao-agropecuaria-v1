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
        
        # Login
        if choice == '1':
            username = input("Usuário: ").strip()
            password = input("Senha: ").strip()
            found = False
            for user in users:
                if user['username'] == username and user['password'] == password:
                    logged_in = username
                    user_type = user['type']
                    found = True
                    print(f"Bem-vindo, {username} ({user_type})!")
                    break
            if not found:
                print("Usuário ou senha inválidos.")
        
        # Register new user
        elif choice == '2':
            username = input("Novo usuário: ").strip()
            password = input("Senha: ").strip()
            utype = input("Tipo (ADM/CLIENTE): ").strip().upper()
            if utype in ['ADM', 'CLIENTE']:
                users.append({'username': username, 'password': password, 'type': utype})
                print("Usuário cadastrado com sucesso!")
            else:
                print("Tipo inválido. Use ADM ou CLIENTE.")
        
        # Exit
        elif choice == '3':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida.")
    
    else:
        if user_type == 'ADM':
            print(f"\n***** Menu ADM - {logged_in} *****")
            print("1. Gerenciar Rebanho")
            print("2. Gerenciar Produção e Derivados")
            print("3. Relatório")
            print("4. Logout")
            choice = input("Escolha uma opção: ").strip()
            
            # Manage Herd
            if choice == '1':
                print("\n***** Gerenciar Rebanho *****")
                print("1. Cadastrar Animal")
                print("2. Buscar Animal")
                print("3. Atualizar Animal")
                print("4. Remover Animal")
                subchoice = input("Escolha: ").strip()
                
                if subchoice == '1':
                    atype = input("Tipo (Bovino de Leite, Caprino, Ovino, Suíno/Leitão): ").strip()
                    aid = input("ID (brinco/número): ").strip()
                    astatus = input("Status: ").strip()
                    animals.append({'type': atype, 'id': aid, 'status': astatus})
                    print("Animal cadastrado!")
                
                elif subchoice == '2':
                    aid = input("ID do animal: ").strip()
                    found = False
                    for animal in animals:
                        if animal['id'] == aid:
                            print(f"Tipo: {animal['type']}, Status: {animal['status']}")
                            found = True
                            break
                    if not found:
                        print("Animal não encontrado.")
                
                elif subchoice == '3':
                    aid = input("ID do animal: ").strip()
                    new_status = input("Novo status: ").strip()
                    for animal in animals:
                        if animal['id'] == aid:
                            animal['status'] = new_status
                            print("Atualizado!")
                            break
                    else:
                        print("Animal não encontrado.")
                
                elif subchoice == '4':
                    aid = input("ID do animal: ").strip()
                    for i, animal in enumerate(animals):
                        if animal['id'] == aid:
                            del animals[i]
                            print("Removido!")
                            break
                    else:
                        print("Animal não encontrado.")
                
                else:
                    print("Opção inválida.")
            
            elif choice == '2':
                # Manage Production
                print("\n***** Gerenciar Produção *****")
                print("1. Adicionar Leite")
                print("2. Adicionar Produto Derivado")
                subchoice = input("Escolha: ").strip()
                
                if subchoice == '1':
                    liters = float(input("Litros de leite: "))
                    milk_stock += liters
                    print(f"Estoque de leite: {milk_stock} L")
                
                elif subchoice == '2':
                    name = input("Nome do produto: ").strip()
                    weight = float(input("Peso (kg): "))
                    value = float(input("Valor de venda: "))
                    products.append({'name': name, 'weight': weight, 'value': value})
                    print("Produto adicionado!")
                
                else:
                    print("Opção inválida.")
            
            # ADM: Report
            elif choice == '3':
                print("\n***** Relatório *****")
                print(f"Total de animais: {len(animals)}")
                print(f"Estoque de leite: {milk_stock} L")
                total_prod_weight = sum(p['weight'] for p in products)
                print(f"Peso total de produtos: {total_prod_weight} kg")
            
            elif choice == '4':
                logged_in = None
                user_type = None
                print("Logout realizado.")
            
            else:
                print("Opção inválida.")
        
        # Client menu
        else:  
            print(f"\n***** Menu Cliente - {logged_in} *****")
            print("1. Visualizar Estoque")
            print("2. Efetuar Compra")
            print("3. Agendar Retirada")
            print("4. Histórico de Compras")
            print("5. Logout")
            choice = input("Escolha uma opção: ").strip()
            
            # View stock
            if choice == '1':
                
                print("\n***** Estoque *****")
                print(f"Leite disponível: {milk_stock} L")
                print("Produtos:")
                for p in products:
                    print(f"- {p['name']}: {p['weight']} kg, R$ {p['value']}")
                print("Animais disponíveis:")
                for a in animals:
                    if a['status'] == 'disponível para venda':
                        print(f"- {a['type']}, ID: {a['id']}")
            
            # Buy
            elif choice == '2':
                print("\n***** Efetuar Compra *****")
                print("1. Comprar Produto")
                print("2. Comprar Animal")
                subchoice = input("Escolha: ").strip()
                
                # Buy product
                if subchoice == '1':
                    name = input("Nome do produto: ").strip()
                    qty = float(input("Quantidade (kg): "))
                    for p in products:
                        if p['name'] == name and p['weight'] >= qty:
                            p['weight'] -= qty
                            purchases.append({'client': logged_in, 'item': name, 'quantity': qty, 'type': 'produto'})
                            print("Compra realizada!")
                            break
                    else:
                        print("Produto insuficiente ou não encontrado.")
                # Buy animal
                elif subchoice == '2':
                    aid = input("ID do animal: ").strip()
                    for i, a in enumerate(animals):
                        if a['id'] == aid and a['status'] == 'disponível para venda':
                            del animals[i]
                            purchases.append({'client': logged_in, 'item': aid, 'quantity': 1, 'type': 'animal'})
                            print("Compra realizada!")
                            break
                    else:
                        print("Animal não disponível.")
                
                else:
                    print("Opção inválida.")
            
            # Schedule pickup
            elif choice == '3':
                item = input("Item para retirada (leite/produto/animal): ").strip()
                date = input("Data (DD/MM/AAAA): ").strip()
                time = input("Horário: ").strip()
                schedules.append({'client': logged_in, 'item': item, 'date': date, 'time': time})
                print("Agendamento realizado!")
            
            # Purchase history
            elif choice == '4':
                print("\n***** Histórico de Compras *****")
                for pur in purchases:
                    if pur['client'] == logged_in:
                        print(f"- {pur['type']}: {pur['item']}, Qtd: {pur['quantity']}")
            # Logout
            elif choice == '5':
                logged_in = None
                user_type = None
                print("Logout realizado.")
            
            else:
                print("Opção inválida.")

