# E-Learning (Projeto de POO)

## Sobre o Projeto
Este projeto foi feito em `Python` como um exercício prático de **Programação Orientada a Objetos**. É uma simulação de console completa, demonstra a interação entre diferentes objetos e usuários (Alunos e Instrutores) em um ambiente de cursos online.

## Funcionalidades

O sistema foi desenvolvido para cobrir os requisitos essenciais de uma plataforma de E-learning, com foco na lógica de backend e na interação entre os objetos.

### Implementadas

* **Course Creation and Management:** Instrutores podem criar, atualizar e gerenciar seus próprios cursos online.
* **Content Access Control:** A lógica garante que instrutores só possam gerenciar seus próprios cursos e que alunos só interajam com os cursos nos quais estão matriculados.
* **Student Enrollment and Tracking:** O sistema gerencia as matrículas dos alunos e rastreia seu progresso de forma individual e persistente durante a execução.
* **Video Streaming (Simulação):** Permite adicionar conteúdos do tipo "Vídeo" ou "PDF" e simula a abertura dos arquivos correspondentes.
* **Certification and Badging:** Ao concluir um curso, o aluno pode emitir um certificado de conclusão, que é salvo como um arquivo `.txt`.
* **Interactive Learning Tools:** Instrutores podem criar quizzes interativos, que os alunos podem responder para testar seus conhecimentos.
* **Payment and Subscription Management (Simulação):** O sistema simula um fluxo de pagamento para cursos pagos antes de liberar o acesso ao aluno.
* **Analytics and Reporting:** A plataforma fornece relatórios detalhados sobre o desempenho dos alunos e o engajamento nos cursos, tanto para a visão do aluno quanto para a do instrutor.
* **Discussion Forums and Chat:** A interação via FORUM foi implementada. A interação via CHAT está sendo trabalhada.

### Não Implementadas

* **Mobile Compatibility:** Sendo uma aplicação de console, não possui interface gráfica.
* **Discussion Forums and Chat:** A funcionalidade de interação entre usuários via CHAT ainda não foi implementada.

---

## Padrões de Projeto Implementados

Este projeto implementa **10 padrões de projeto** para demonstrar conceitos avançados de **Projeto de Software** e melhorar a qualidade do código. Cada padrão foi aplicado em contextos reais e práticos do sistema de E-Learning.

### 📦 Criacionais (3/3)

#### **Singleton** - `src/singleton_metaclass.py`
- **Problema**: Garantir uma única instância de gerenciadores de conteúdo para evitar duplicação e desperdício de recursos
- **Solução**: Metaclasse que controla criação de instâncias únicas
- **Implementação**: 
    - Metaclasse: `SingletonABCMeta` (para classes abstratas e seus filhos) e `SingletonMeta`(para as demais)
    - Singletons: `GerenciadorConteudo`, `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario`
  - Client: `AddContentStrategy` em `src/menus/course_management_strategies.py`
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos

#### **Factory Method** - `src/functions/instructor_functions/gerenciador_conteudo.py`
- **Problema**: Criar e adicionar diferentes tipos de conteúdo (Texto, Externo, Questionario) aos cursos sem acoplar o código
- **Solução**: Interface abstrata para criação de conteúdo e cadeia de validações implementada pelas classes concretas
- **Implementação**: 
    - Creator abstrato: `GerenciadorConteudo` (obriga a implementação do `factory_method` e `validation_chain` e usa-os no `adicionar`, para inserir novos conteúdos)
    - Creator concretos: `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario`
  - Client: `AddContentStrategy` em `src/menus/course_management_strategies.py`
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos

#### **Builder** - `src/functions/instructor_functions/course_builder.py`
- **Problema**: Criar objetos `Course` complexos com muitos parâmetros opcionais de forma clara
- **Solução**: Classe de construtor com métodos fluentes (retornam o próprio objeto) e validação dos dados mínimos necessários
- **Implementação**: 
    - Builder: `CourseBuilder`
    - Product: `Course`
    - Client (utilização): `src/functions/instructor_functions/criar_curso.py`
- **Uso no projeto**: Quando um instrutor deseja criar um curso novo


### 🔄 Comportamentais (4/3)

#### **Strategy** - `src/menus/`
- **Problema**: Construção de menus com diversas opções sem usar várias condicionais
- **Solução**: Interface para padronizar as ações dos menus e classe de contexto para adicionar ações, exibir menu e executar estratégia (ação) escolhida
- **Implementação**: 
  - Context: `MenuManager`
  - Strategy abstrata (interface): `MenuActionStrategy`
  - Strategy concretas: Classes de estratégia em `strategies.py`, `exit_strategy.py`, `course_management_strategies.py`, `instructor_strategies.py` e `student_strategies.py`
  - Client: `course_management_menu`, `student_menu` e `instructor_menu` em `src/menus/`
- **Uso no projeto**: Todos os menus do sistema

#### **State** - `src/models/forum.py`
- **Problema**: Comportamento de posts do fórum muda drasticamente baseado no estado (Draft, Published, Closed)
- **Solução**: Interface para padronizar os estados do post, permitindo diferentes comportamentos para métodos de comportamento do post
- **Implementação**: 
  - Context: `ForumPost`
  - State: `PostState`
  - Concrete States: `Draft`, `Published`, `Closed`
  - Client: `adicionar_post` em `src/functions/student_functions/adicionar_post.py`
- **Uso no projeto**: Ao criar e interagir com posts do fórum

#### **Chain of Responsibility** - `src/functions/instructor_functions/content_validation.py`
- **Problema**: Validações complexas de conteúdo com múltiplas regras
- **Solução**: Cadeia de handlers (validadores) que processam sequencialmente até encontrar erro ou completar
- **Implementação**: 
  - Handler: `Handler`
  - Concrete Handlers: `TitleLengthValidation`, `FileFormatValidation`, etc.
  - Client: `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario` em `src/functions/instructor_functions/gerenciador_conteudo.py`
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos

#### **Template Method** - `src/functions/instructor_functions/gerenciador_conteudo.py` (intimamente relacionado com o Factory Method)
- **Problema**: Diferentes formas de criar conteúdo e uma cadeia de validação correspondente
- **Solução**: Algoritmo padrão para adição de conteúdos, que utiliza passos variáveis para cada tipo de conteúdo
- **Implementação**:
  - **AbstractClass**: `GerenciadorConteudo`, que declara os passos (`factory_method` e `validation_chain`) do algoritmo/template method (`adicionar`)
  - **ConcreteClasses**: `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario`, que implementam os passos conforme o tipo de conteúdo, mas não sobrescrevem o algoritmo/template method
  - Client: `AddContentStrategy` em `src/menus/course_management_strategies.py`
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos


### 🔧 Estruturais (3/3)

#### **Adapter** - `src/functions/instructor_functions/magic_validation.py`
- **Problema**: Biblioteca `python-magic` (usada para validar o tipo real de um arquivo) tem interface incompatível com a interface de validador do projeto (`Handler`) 
- **Solução**: Adaptador para usar a biblioteca externa com a interface esperada pelos validadores
- **Implementação**: 
  - Target: `Handler` (interface de validadores)
  - Adaptee: `SimpleMagicValidation` (classe criada para usar a biblioteca externa)
  - Adapter: `MagicPythonValidationAdapter` (conecta interfaces)
  - Client: método `validation_chain` de `GerenciadorExterno` em `src/functions/instructor_functions/gerenciador_conteudo.py`
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo externo aos seus cursos


#### **Decorator** - `src/logging/strategy_logging_decorator`
- **Problema**: Adicionar logs das opções de menu seleciondas pelos usuários sem alterar cada uma das classes de Strategy
- **Solução**: Criar um decorador para guardar o opção selecionada pelo usuário e depois executar a função
- **Implementação**:
  - Component: `MenuActionStrategy` (interface para todas as opções de menu)
  - Concrete Components: Todas as opções de menu (classes que herdam `MenuActionStrategy`)
  - Base Decorator: `BaseDecoratorStrategy`
  - Concrete Decorator: `LoggingDecoratorStrategy`
  - Client: `course_management_menu`, `student_menu` e `instructor_menu` em `src/menus/`
- **Uso no projeto**: Quando o usuário seleciona opções que podem alterar os dados do sistema

#### **Facade** - `src/analytics`
- **Problema**: Subssistema de geração de relatórios complexo
- **Solução**: Criar uma fachada que simplifique a interação com o subssistema
- **Implementação**:
  - Facade: `AnalyticsFacade`
  - Subssistemas complexos: `CourseAnalyticsCalculator`, `StudentProgressClaculator`, `RerportGenerator`
  - Client: `ReportStrategy` e `PerformanceStrategy` em `src/menus/course_management_strategies.py`
- **Uso no projeto**: Ao gerar relatórios do curso e individuais (para aluno)

---

## Tratamento de Exceções

A maioria das alterações feitas no código para tratar exceções encontram-se no commit [61dc2dc](https://github.com/wyvianvalenca/E-Learning_Refactor/commit/61dc2dcaf6301149b74def112b3d6e2e887f3c56)

### Entradas lidas com `questionary`

A maioria das exceções ocorre quando o usuário insere uma entrada que difere do esperado pelo programa. Com o uso da biblioteca `questionary`, pude realizar um tratamento melhor das entradas do usuário, pois ela permite inserir uma função para verificar a entrada, impedindo a gravação do dado até que tal função retorne `True`.

Foram usadas funções como `is_positive_number`, `text_has_2words`, entre outras, para validar as entradas do usuário. Todas as funções de validação estão em `src/validations.py`

Além disso, outra ação do usuário que pode atrapalhar o fluxo do sistema é o uso do Ctrl+C (interrupção por teclado). Nesses casos, todas as funções de input da biblioteca `questionary` capturam essa entrada e retornan `None`. Para evitar que o valor nulo quebre qualquer lógica da aplicação, as variáveis que recebem as entradas do usuário sempre são verificadas para o valor nulo e, caso o contenham, a operação é cancelada imediatamente.

#### Caso específico: Gerenciadores de Conteúdo em `src/functions/instructor_functions/gerenciador_conteudo.py`

Em relação ao tratamento da interrupção do usuário com Ctrl+C dentro da criação de conteúdo, precisamos criar um erro personalizado, por causa da estrutura do padrão criacional FACTORY METHOD aplicado.

As funções de `template_method` de cada criador concreto capturam as informações do usuário e fazem a criação de um novo conteúdo. Nesse processo, o usuário pode aplicar a interrupção por teclado (Ctrl+C) em algum dos inputs, o que retornaria o valor `None` para o programa. Para evitar isso, criamos uma excessão `CancelledByYserError` para indicar que o usuário deseja cancelar a operação. Ao pressionar Ctrl+C em qualquer um dos inputs desse processo, o sistema levanta a exceção personalizada.

Para tratar tal comportamento inesperado, na função `adicionar` (TEMPLATE METHOD), inserimos um bloco `try-except` que captura o erro personalizado e cancela toda a operação de criação e adição de conteúdos, evitando que erros apareçam para o usuário.

### Código legado

Algumas das funções do sistema não foram refatoradas e não implementaram a biblioteca `questionary`, para tais, utilizamos blocos `try-except`.

#### `executar` em `src/functions/student_functions/plataforma_do_curso.py` (a partir da linha 43)

Como a entrada é lida como texto e o programa espera um número, tentamos fazer o casting de tipos, e, caso a entrada contenha letras ou símbolos, um erro `ValueError` é levantado, o qual tratamos no bloco `except`.

Além disso, também tratamos a exceção `KeyboardInterrupt`, cancelando a operação caso o usuário pressione Ctrl+C.

#### `executar` em `src/functions/student_functions/inscrever_curso.py` (a partir da linha 15)

Tratamos a exceção `KeyboardInterrupt`, cancelando a operação caso o usuário pressione Ctrl+C.

#### `selecionar_curso_do_instrutor` em `src/functions/instructor_functions/dry.py` (a partir da linha 20)

Como a entrada é lida como texto e o programa espera um número, tentamos fazer o casting de tipos, e, caso a entrada contenha letras ou símbolos, um erro `ValueError` é levantado, o qual tratamos no bloco `except`.

### Validações de arquivos com bilbioteca externa `python-magic` (`src/functions/instructor_functions/magic_validations.py`)

Para validar os conteúdos externos (arquivos) que são inseridos no sistema, utilizamos uma biblioteca externa que verifica o tipo real do arquivo. Para evitar problemas com a inicialização dessa biblioteca, utilizamos excepts genéricos, visto que não conhecemos os erros específicos que podem ser levantados.

Entrtanto, salvamos e imprimimos na tela todas as exceções geradas pelas operações da biblioteca, para podermos identificá-los e tratá-los individualmente. Porém, até o momento, nenhum erro foi gerado pelo programa na validação de arquivos.

--

## Como Rodar o Projeto

A execução é simples. Recomendamos o uso de Ambiente Virtual Python para instalação dos pacotes externos.

### Clone o repositório e vá para a pasta do projeto
```bash
git clone https://github.com/wyvianvalenca/E-Learning_Refactor.git
cd E-Learning_Refactor
```

### Crie e ative um Ambiente Virtual
```
python3 -m venv venv
source venv/bin/activate
```

### Instale as dependencias do projeto
Esse projeto usa algumas bibliotecas externas:
- [rich](https://github.com/Textualize/rich)
- [questionary](https://github.com/tmbo/questionary)
- [python-magic](https://github.com/ahupp/python-magic)

```bash
pip install -r requirements.txt
```

### Rode o código
```bash
python main.py

```

A aplicação será iniciada no console. Siga as instruções na tela para navegar pelos menus.
