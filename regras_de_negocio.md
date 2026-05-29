# Sistema de Gestão Agropecuária - Agropesca Jacaré

Este projeto é um sistema interativo em terminal desenvolvido para a gestão de rebanhos, produção de derivados e comércio agropecuário da **Fazenda Agropesca Jacaré**. O sistema foi construído seguindo **restrições acadêmicas rigorosas**, utilizando apenas estruturas e lógica de programação básica em Python.

---

## Regras de Negócio

O sistema é dividido entre duas funções de usuários (**Administradores** e **Clientes**), possuindo regras estritas de segurança, validação de dados e isolamento de informações.

### 1. Cadastro, Autenticação e Segurança
* **Identificação Única por E-mail:** O e-mail é o identificador único de cada usuário e não pode ser duplicado no sistema.
* **Validação de Formato de E-mail:** O cadastro exige que o e-mail inserido passe por uma validação manual caractere por caractere para garantir o formato correto (`algo@algo.algo`):
  * Deve conter exatamente um símbolo `@`.
  * Deve conter pelo menos um caractere antes do `@`.
  * Deve conter um ponto (`.`) posicionado após o `@`.
  * Deve haver pelo menos um caractere entre o `@` e o `.`.
  * Deve haver pelo menos um caractere depois do último `.`.
* **Separação de Papéis:** Os usuários cadastram-se como `ADM` (Administrador) ou `CLIENTE`, o que define seus menus e permissões de acesso.

---

### 2. Regras do Administrador (ADM)

#### A. Gerenciamento de Rebanho & Isolamento de Dados
* **Geração Automática de Prefixo Único:** Para evitar que um administrador manipule ou exclua animais de outros administradores, cada ADM recebe um prefixo único baseado no seu nome de cadastro:
  * Exemplo: O primeiro "Miguel" registrado recebe o prefixo `m`. O segundo "Miguel" (ou "Miguel Francisco") receberá `mi` ou `mf`, garantindo a exclusão de ambiguidades.
* **Namespace nos Animais:** Sempre que um ADM cadastra um animal com um ID numérico (ex: brinco `13`), o sistema salva o ID concatenando o prefixo daquele ADM (ex: `m13`).
* **Proteção Contra Alterações Indevidas:** Operações de busca, atualização de status e remoção de animais solicitam o ID simplificado, mas aplicam implicitamente o prefixo do ADM logado. Isso impossibilita que um administrador altere o animal `mf13` se seu próprio prefixo for `m`.
* **Tipos de Animais Permitidos:** O sistema apenas aceita animais do tipo: `Bovino de Leite`, `Caprino`, `Ovino` ou `Suíno/Leitão` (com tratamento de acentuação).
* **Validação de Peso e Preço:** O peso (kg) e o preço de venda (R$) são validados caractere por caractere para garantir que são números decimais positivos e válidos.

#### B. Produção e Derivados
* **Estoque de Leite:** O leite é adicionado ao estoque em litros junto ao preço de venda por litro correspondente.
* **Produção de Derivados:** O ADM pode cadastrar produtos derivados de leite. Se o produto for marcado como derivado (`s`), o sistema exige a quantidade de leite necessária por unidade e realiza o abate automático do estoque de leite desse ADM. A produção é interrompida caso não haja leite suficiente.
* **Privacidade de Estoque:** Um ADM só visualiza e gerencia os seus próprios produtos e estoque de leite.

#### C. Relatórios Financeiros
* O ADM tem acesso a um relatório em tempo real que contabiliza:
  * O total de animais sob sua gerência.
  * Seu estoque atual de leite.
  * O peso total de seus produtos.
  * A **Receita Total** acumulada a partir das compras realizadas pelos clientes em cima dos seus animais, litros de leite e produtos derivados.

---

### 3. Regras do Cliente

#### A. Visualização de Estoque
* O cliente tem uma visão transparente do estoque geral da fazenda, listando:
  * O estoque de leite disponível e o preço de cada ADM vendedor.
  * A lista de produtos disponíveis por quilo e o respectivo ADM vendedor.
  * Animais disponíveis para venda, exibindo seus IDs completos (com prefixo do respectivo ADM).

#### B. Fluxo de Compra e Abate de Estoque
* Clientes podem comprar **Leite**, **Produtos** ou **Animais**.
* **Seleção do Vendedor:** Nas compras de leite e produtos, o cliente escolhe o vendedor utilizando o **e-mail** do respectivo ADM.
* **Abate Automático:** A quantidade comprada é deduzida imediatamente do estoque do ADM vendedor. Na compra de um animal, o status do animal é alterado de `"Disponível para venda"` para `"Vendido"`.

#### C. Validação Estrita de Agendamento de Retirada
Toda compra exige o agendamento de uma data (`DD/MM/AAAA`) e hora (`HH:MM`) válidos. A validação é feita manualmente:
* **Prevenção de Datas Retroativas:** Não são aceitos agendamentos com datas anteriores ao dia **11/05/2026**.
* **Validação de Calendário Real:**
  * O mês deve estar entre `01` e `12`.
  * O dia deve ser coerente com o mês correspondente (meses de 30 ou 31 dias).
  * **Ano Bissexto:** Validação manual do dia `29 de fevereiro` para anos bissextos baseada na regra matemática de divisibilidade por 4, 100 e 400.
  * O horário deve estar no intervalo válido (horas entre `00` e `23`, minutos entre `00` e `59`).

#### D. Histórico e Retiradas
* O cliente possui um painel exclusivo onde pode visualizar seu histórico completo de compras com o nome do item, quantidade e vendedor, além de uma lista de todas as suas retiradas agendadas.

---

## Restrições Técnicas Adotadas (Regras Acadêmicas)

Para fins de avaliação acadêmica de lógica de programação, o código respeita estritamente o banimento de recursos avançados. **O projeto não utiliza:**
1. **Funções personalizadas (`def`)** - toda a lógica é estruturada linearmente em blocos de decisão dentro do loop principal.
2. **Dicionários (`dict`) ou Conjuntos (`set`)** - todos os dados estruturados são armazenados em listas multidimensionais (listas dentro de listas).
3. **Bibliotecas externas ou nativas (`import`)** - nenhuma importação é feita (nem mesmo `datetime`, `re` ou `math`). Toda validação de data, hora e e-mail é feita através de matemática básica e loops.
4. **Orientação a Objetos (`class`)** - sem modelagem de classes ou objetos.
5. **Estrutura `match/case`** - controle feito estritamente por condicionais aninhadas `if/elif/else`.
6. **Mapeamento de arquivos** - toda a persistência dos dados é feita em memória durante o ciclo de execução do script.
