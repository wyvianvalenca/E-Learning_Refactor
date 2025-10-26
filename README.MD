# E-Learning (Projeto de POO)

## Sobre o Projeto
Este projeto foi feito em `Python` como um exercício prático de **Programação Orientada a Objetos**. É uma simulação de console completa, demonstra a interação entre diferentes objetos e usuários (Alunos e Instrutores) em um ambiente de cursos online.

---

## TO-DO

### Funcional
- [x] inserir novas informações do curso (nível e categorias) na visualização dos cursos
- [ ] permitir edição e publicação de posts em rascunho (alunos)
- [ ] implementar forum do curso para os alunos (visualizar e adicionar post)
- [ ] implementar chat

### Padrões
- [x] refatorar criacao de curso com builder
- [x] implementar strategy no menu dos alunos
- [x] implementar state no forum (open, closed, deleted)
- [x] implementar chain of responsability para criação de conteudos
- [x] implementar adapter
- [ ] definir 2 padrões estruturais para adicionar

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

Este projeto implementa **7 padrões de projeto** para demonstrar conceitos avançados de **Projeto de Software** e melhorar a qualidade do código. Cada padrão foi aplicado em contextos reais e práticos do sistema de E-Learning.

### 📦 Criacionais (3/3)

#### **Singleton** - `src/singleton_metaclass.py`
- **Problema**: Garantir uma única instância de gerenciadores de conteúdo para evitar duplicação e desperdício de recursos
- **Solução**: Metaclasse que controla criação de instâncias únicas
- **Implementação**: 
    - Metaclasse: `SingletonABCMeta` (para classes abstratas e seus filhos) e `SingletonMeta`(para as demais)
    - Singletons: `GerenciadorConteudo`, `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario`
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos

#### **Factory Method** - `src/functions/instructor_functions/gerenciador_conteudo.py`
- **Problema**: Criar e adicionar diferentes tipos de conteúdo (Texto, Externo, Questionario) aos cursos sem acoplar o código
- **Solução**: Interface abstrata para criação de conteúdo e cadeia de validações implementada pelas classes concretas
- **Implementação**: 
    - Creator abstrato: `GerenciadorConteudo` (obriga a implementação do `factory_method` e `validation_chain` e usa-os no `adicionar`, para inserir novos conteúdos)
    - Creator concretos: `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario`
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
- **Uso no projeto**: Todos os menus do sistema

#### **State** - `src/models/models.py`
- **Problema**: Comportamento de posts do fórum muda drasticamente baseado no estado (Draft, Published, Closed)
- **Solução**: Interface para padronizar os estados do post, permitindo diferentes comportamentos para métodos de comportamento do post
- **Implementação**: 
  - Context: `ForumPost`
  - State: `PostState`
  - Concrete States: `Draft`, `Published`, `Closed`
- **Uso no projeto**: Ao criar e interagir com posts do fórum

#### **Chain of Responsibility** - `src/functions/instructor_functions/content_validation.py`
- **Problema**: Validações complexas de conteúdo com múltiplas regras
- **Solução**: Cadeia de handlers (validadores) que processam sequencialmente até encontrar erro ou completar
- **Implementação**: 
  - Handler: `Handler`
  - Concrete Handlers: `TitleLengthValidation`, `FileFormatValidation`, etc.
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos

#### **Template Method** - `src/functions/instructor_functions/gerenciador_conteudo.py` (intimamente relacionado com o Factory Method)
- **Problema**: Diferentes formas de criar conteúdo e uma cadeia de validação correspondente
- **Solução**: Algoritmo padrão para adição de conteúdos, que utiliza passos variáveis para cada tipo de conteúdo
- **Implementação**:
  - **AbstractClass**: `GerenciadorConteudo`, que declara os passos (`factory_method` e `validation_chain`) do algoritmo/template method (`adicionar`)
  - **ConcreteClasses**: `GerenciadorExterno`, `GerenciadorTexto` e `GerenciadorQuestionario`, que implementam os passos conforme o tipo de conteúdo, mas não sobrescrevem o algoritmo/template method
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo aos seus cursos

### 🔧 Estruturais (1/3)

#### **Adapter** - `src/functions/instructor_functions/magic_validation.py`
- **Problema**: Biblioteca `python-magic` (usada para validar o tipo real de um arquivo) tem interface incompatível com a interface de validador do projeto (`Handler`) 
- **Solução**: Adaptador para usar a biblioteca externa com a interface esperada pelos validadores
- **Implementação**: 
  - Target: `Handler` (interface de validadores)
  - Adaptee: `SimpleMagicValidation` (classe criada para usar a biblioteca externa)
  - Adapter: `MagicPythonValidationAdapter` (conecta interfaces)
- **Uso no projeto**: Quando um instrutor deseja adicionar conteúdo externo aos seus cursos

## Estrutura do Código

O projeto foi organizado de forma modular para seguir o **Princípio da Responsabilidade Única**, onde cada arquivo possui uma responsabilidade clara.

```
/ (pasta raiz)
├── requirements.txt
├── main.py
├── inicial.py
├── dados_iniciais.py
├── data_base.py
├── singleton_metaclass.py
├── models/
│   └── models.py
├── aluno/
│   ├── funcoes_aluno.py
│   └── ... (um arquivo para cada ação do aluno)
├── instrutor/
│   ├── funcoes_instrutor.py
│   └── ... (um arquivo para cada ação do instrutor)
└── content/
    ├── video.mp4
    ├── pdf.pdf
    └── ... (arquivos de conteudo externo)
```

---

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

```bash
pip install -r requirements.txt
```

### Rode o código
```bash
python main.py

```

A aplicação será iniciada no console. Siga as instruções na tela para navegar pelos menus.
