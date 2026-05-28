# Sistema de Gestão Agropecuária

## Descrição do Problema

Este projeto consiste no desenvolvimento de um **Sistema de Gestão Agropecuária (Fazenda Sertão)** executado em terminal, com foco no uso de **estruturas básicas de programação**, como listas e estruturas de repetição.

O sistema possui dois tipos de usuários:

* **Administrador (ADM)**
  Responsável pela gestão da fazenda, incluindo:

  * controle do rebanho
  * produção de leite
  * produtos derivados
  * vendas

* **Cliente**
  Responsável por:

  * visualizar estoque
  * realizar compras
  * agendar retirada de produtos, leite ou animais

---

## Objetivo

Aplicar conceitos fundamentais de programação utilizando:

* listas
* estruturas condicionais
* estruturas de repetição
  sem uso de recursos avançados como funções, dicionários ou orientação a objetos.

---

## Funcionalidades do Sistema

### R1 - Login

* Login com usuário e senha
* Diferenciação entre ADM e CLIENTE

---

### Funcionalidades do Administrador (ADM)

#### R2 - Gerenciar Rebanho

* Cadastrar animal
* Buscar animal
* Atualizar status
* Remover animal
* Listar animais

**Dados armazenados:**

* Tipo
* ID (brinco/número)
* Peso
* Status

---

#### R3 - Gerenciar Produção e Derivados

* Adicionar leite ao estoque (em litros)
* Cadastrar produtos derivados:

  * Nome
  * Peso (kg)
  * Valor de venda

---

#### R4 - Tema Livre (Implementado)

* Relatório geral contendo:

  * Total de animais
  * Estoque de leite
  * Peso total de produtos
  * Receita de vendas

---

### Funcionalidades do Cliente

#### R5 - Efetuar Compra

* Comprar:

  * Produtos
  * Animais
  * Leite
* Atualiza o estoque automaticamente

---

#### R6 - Agendar Retirada

* Agendamento de retirada com:

  * Data
  * Horário
* Para:

  * leite
  * produtos
  * animais

---

#### R7 - Tema Livre (Implementado)

* Histórico de compras
* Visualização de retiradas agendadas

---

### R8 - Cadastro de Usuários

* Cadastro com definição de tipo:

  * ADM
  * CLIENTE

---

### R9 - Navegabilidade

* Sistema baseado em **loop principal (`while True`)**
* Menus interativos
* Não encerra inesperadamente

---

# Estruturas Utilizadas no Código

## Tipos de Dados

* `int`
* `float`
* `str`
* `bool`
* `None`

---

## Estruturas de Dados

### Listas

Utilizadas como principal forma de armazenamento:

```python
users = []
animals = []
products = []
purchases = []
schedules = []
```

---

### Listas dentro de listas

Utilizadas como “registros”:

```python
users.append([username, password, utype])
animals.append([tipo, id, peso, status])
```

---

## Estruturas de Repetição

* `while`

  * loop principal
  * percorrer listas com índice

* `for`

  * percorrer listas diretamente

---

## Estruturas Condicionais

* `if`
* `elif`
* `else`

---

## Funções Utilizadas (Built-in)

* `input()`
* `print()`
* `len()`
* `int()`
* `float()`
* `str()`

---

## Métodos de String

* `.strip()`
* `.lower()`
* `.upper()`
* `.replace()`
* `.split()`
* `.isdigit()`
* `.count()`
* `.format()`

---

## Operações com Listas

* `append()`
* `del`
* acesso por índice (`lista[i]`)

---

## Controle de Fluxo

* `break`

---

## Operadores Utilizados

### Aritméticos

* `+`, `-`

### Comparação

* `==`, `!=`, `<`, `>`, `<=`, `>=`

### Lógicos

* `and`, `or`

---

## Restrições Respeitadas

O código **não utiliza**:

* funções (`def`)
* dicionários (`dict`)
* conjuntos (`set`)
* classes (POO)
* bibliotecas externas (`import`)
* `match/case`
* recursão
* manipulação de arquivos

---

# Conclusão

O sistema foi desenvolvido seguindo rigorosamente os requisitos da atividade, utilizando apenas **estruturas básicas de Python**, com foco em:

* lógica de programação
* manipulação de listas
* controle de fluxo
* interação via terminal

Apesar das limitações impostas (sem funções ou estruturas avançadas), o sistema atende aos requisitos funcionais propostos e apresenta uma solução completa para o problema.

