# E-Learning (Projeto de POO)

## Sobre o Projeto
Este projeto foi feito em `Python` como um exercício prático de **Programação Orientada a Objetos**. É uma simulação de console completa, demonstra a interação entre diferentes objetos e usuários (Alunos e Instrutores) em um ambiente de cursos online.

---

## TO-DO
- inserir novas informações do curso (nível e categorias) na visualização dos cursos
- implementar strategy no menu dos alunos
- implementar forum do curso para os alunos (visualizar e adicionar post)
- implementar chat

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

## Padrões de Projeto

Foram implementados alguns padrões de projeto para melhor qualidade de código.

### Criacionais

- **Singleton**: instâncias únicas para o gerenciador de cursos e para os gerenciadores de conteúdo.
- **Factory Method**: fábrica para os gerenciadores de conteúdo, visto que temos vários tipos de conteúdo.
- **Builder**: construtor versátil para os cursos.

### Comportamentais

- **Strategy**: padrão utilizado no menu do Instrutor.

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
