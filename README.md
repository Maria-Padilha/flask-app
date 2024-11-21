# **Sistema de Cadastro de Eventos**

Este é um sistema completo de cadastro, pesquisa, edição, exclusão e exportação de dados relacionados a eventos. Ele foi desenvolvido utilizando **Flask**, **SQLite**, **HTML**, **CSS** e **Bootstrap** para oferecer uma interface simples e funcional.

---

## **🚀 Funcionalidades**

- **Tela Principal**: Página inicial com links para todas as funcionalidades principais.
- **Cadastro de Eventos**: Formulário para cadastrar eventos com sete campos obrigatórios.
- **Pesquisa de Eventos**: Busca eventos cadastrados pelo nome e exibe resultados em uma tabela organizada.
- **Edição e Exclusão**: Permite editar ou excluir registros diretamente da página de pesquisa.
- **Exibição Completa**: Página separada que exibe todos os eventos cadastrados no sistema.
- **Upload de Arquivos**: Importação de dados em formatos CSV, JSON ou Excel para o banco de dados.
- **Exportação de Dados**: Exporta os dados cadastrados em formato Excel (.xlsx) para download.

---

## **🛠 Tecnologias Utilizadas**

### **Backend (Python)**
- **Flask**: Framework principal para criar as rotas e controlar a aplicação.
- **SQLAlchemy**: ORM para manipulação do banco de dados SQLite.
- **Pandas**: Biblioteca para leitura de arquivos (CSV, JSON, Excel) e manipulação de dados.
- **OpenPyXL**: Para exportar os dados para arquivos Excel (.xlsx).

### **Frontend (HTML e CSS)**
- **HTML**: Estrutura das páginas (cadastro, pesquisa, exibição, upload e exportação).
- **CSS**: Estilização personalizada para deixar a interface amigável e responsiva.
- **Bootstrap**: Framework CSS para facilitar a criação de layouts modernos e responsivos.

---

## **📂 Estrutura do Projeto**

```plaintext
.
├── app.py                # Arquivo principal da aplicação Flask
├── instance/             # Diretório contendo o banco de dados
|   ├── eventos.db        # Banco de dados SQLite
├── templates/            # Diretório contendo arquivos HTML
│   ├── index.html        # Página inicial
│   ├── cadastro.html     # Tela de cadastro
│   ├── pesquisa.html     # Tela de pesquisa
│   ├── editar.html       # Tela de edição
│   ├── upload.html       # Tela de upload de arquivos
│   ├── exibir.html       # Página para exibir todos os eventos
├── static/               # Diretório para arquivos CSS
│   ├── styles.css        # Estilo personalizado do sistema
├── README.md             # Documentação do projeto
