# E-Learning (Projeto de POO)

## Sobre o Projeto
Este projeto foi feito em `Python` como um exercício prático de **Programação Orientada a Objetos**. É uma simulação de console completa, demonstra a interação entre diferentes objetos e usuários (Alunos e Instrutores) em um ambiente de cursos online.

---

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

### Não Implementadas

* **Mobile Compatibility:** Sendo uma aplicação de console, não possui interface gráfica.
* **Discussion Forums and Chat:** A funcionalidade de interação e comunidade entre usuários não foi implementada.

---

## Estrutura do Código

O projeto foi organizado de forma modular para seguir o **Princípio da Responsabilidade Única**, onde cada arquivo possui uma responsabilidade clara.

```
/ (pasta raiz)
├── main.py
├── inicial.py
├── dados_iniciais.py
├── data_base.py
├── models/
│   └── models.py
├── aluno/
│   ├── funcoes_aluno.py
│   └── ... (um arquivo para cada ação do aluno)
└── instrutor/
    ├── funcoes_instrutor.py
    └── ... (um arquivo para cada ação do instrutor)
```

---

## Como Rodar o Projeto

A execução é simples e não requer a instalação de pacotes externos.

1.  Certifique-se de que você tem o **Python 3** instalado.
2.  Navegue pelo seu terminal até a pasta raiz do projeto (a que contém o `main.py`).
3.  Execute o seguinte comando, no terminal:

    ```bash
    python main.py
    ```
4.  A aplicação será iniciada no console. Siga as instruções na tela para navegar pelos menus.
