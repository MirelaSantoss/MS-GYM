# Sistema de Gerenciamento de Academia

Projeto web desenvolvido em **Python e Flask** com o objetivo de criar uma plataforma para gerenciamento de uma academia.

O sistema está sendo desenvolvido seguindo uma organização baseada no padrão **MVC**, utilizando **Jinja2** para as interfaces e **Blueprints** para a organização das funcionalidades.

### Funcionalidades

* Sistema de login e autenticação
* Controle de acesso dos usuários
* Cadastro e gerenciamento de alunos
* Gerenciamento de professores
* Criação e gerenciamento de treinos
* Acesso dos alunos aos seus treinos
* Informações da academia

> Projeto em desenvolvimento. Novas funcionalidades serão adicionadas conforme a evolução do sistema.


### Integração SQLite (atividade prática)

O cadastro de usuários utiliza a biblioteca nativa `sqlite3`. A classe `Usuario`, em `app/models/usuario.py`, concentra conexão, criação da tabela, inserção, consulta e autenticação. O formulário `/cadastro` grava os dados e `/usuarios` exibe os registros com Jinja2. O arquivo `database.db` é criado na pasta principal do projeto ao iniciar o Flask.
