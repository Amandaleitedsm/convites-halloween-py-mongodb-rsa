# 🎃 Projeto: Convites Secretos para a Festa de Halloween

## 🕸️ Descrição Geral

Este projeto é um **aplicativo em Python com interface gráfica (Tkinter)** que gerencia os **convidados de uma festa de Halloween**.  
O sistema armazena os nomes dos convidados em texto simples, mas **protege e-mails e telefones com criptografia RSA assimétrica**, garantindo a confidencialidade dos dados.

Os dados são salvos em um **banco MongoDB**, e o acesso à lista de convidados é protegido por uma **charada temática de Halloween**.  
Somente quem acertar a charada pode visualizar e manipular as informações.

---

## 🧠 Funcionalidades Principais

### 🧩 1. Tela de Charada
- O usuário precisa **acertar uma charada de Halloween** (“abóbora”) para acessar o sistema.
- Interface com tema escuro e elementos estilizados para o clima da festa.

### 📜 2. Tela de Lista de Convidados
- Exibe uma tabela (`Treeview`) com os convidados e seus dados.
- E-mails e telefones são **armazenados criptografados**, e descriptografados apenas para exibição.
- É possível **filtrar** convidados pelo nome ou status de RSVP.

### ✍️ 3. CRUD Completo
- **Adicionar** novos convidados (criptografando e-mail e telefone automaticamente).  
- **Atualizar** dados (mantendo os dados protegidos se não forem modificados).  
- **Deletar** convidados selecionados.  
- **Limpar** os campos de entrada rapidamente.

---

## 🔐 Estrutura de Dados no MongoDB

Cada documento armazenado segue este formato:

```json
{
  "name": "Carlos",
  "email": "<ciphertext>",
  "phone": "<ciphertext>",
  "rsvp": "SIM"
}
````

* `name`: armazenado em texto plano
* `email`: criptografado com RSA
* `phone`: criptografado com RSA
* `rsvp`: resposta de presença (“SIM”, “NÃO” ou “TALVEZ”)

---

## ⚙️ Tecnologias Utilizadas

* **Python 3.x**
* **Tkinter** → Interface gráfica
* **Pymongo** → Conexão com o MongoDB
* **Cryptography (RSA)** → Criptografia dos dados sensíveis
* **BSON / ObjectId** → Identificação única de registros

---

## 🧩 Principais Funções

### 🔸 `encrypt(text)`

Criptografa o texto usando a **chave pública RSA**:

```python
def encrypt(text):
    return public_key.encrypt(
        text.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
    )
```

### 🔸 `decrypt(ciphertext)`

Descriptografa o texto com a **chave privada RSA**.
Se o dado não puder ser decriptado, mostra o ícone “🔒 Dado protegido”.

### 🔸 `tela_charada()`

Cria a tela inicial com uma charada temática.
Se o usuário acertar (“abóbora”), é levado para a lista de convidados.

### 🔸 `tela_lista()`

Cria a interface principal do sistema:

* Tabela com todos os convidados.
* Campos para busca, adição, edição e exclusão.
* Combobox para filtrar por RSVP.
* Botões para as operações CRUD.

### 🔸 `carregar_dados()`

Busca os dados no MongoDB aplicando filtros e atualiza a tabela (`Treeview`).

### 🔸 `adicionar_convidado()`

Insere um novo convidado no banco após criptografar os campos sensíveis.

### 🔸 `atualizar_convidado()`

Atualiza apenas os campos modificados, **mantendo os dados criptografados** caso não tenham sido alterados.

### 🔸 `deletar_convidado()`

Remove o convidado selecionado após confirmação.

---

## 💻 Como Executar

### 1. Instale os pacotes necessários

No terminal:

```bash
pip install pymongo cryptography
```

### 2. Configure o MongoDB

Certifique-se de que o **MongoDB esteja em execução** localmente na porta padrão (`mongodb://localhost:27017/`).

Crie um banco e uma coleção automaticamente (o código faz isso se não existirem):

```
Banco: Projeto4bim_Halloween
Coleção: convites_halloween
```

### 3. Execute o programa

Salve o código como `app.py` e execute:

```bash
python app.py
```

### 4. Resolva a charada 🎃

Na tela inicial, digite:

```
abóbora
```

ou

```
abobora
```

para acessar a lista secreta.

---

## 🧡 Detalhes Visuais

* Tema escuro com detalhes em **laranja**, **bege** e **tons de marrom**.
* Fonte decorativa para o clima de Halloween.
* Animações visuais com `Frame` e `Label` para dar destaque à charada.

---

## 🧪 Segurança

* Utiliza **RSA assimétrico** (2048 bits).
* Apenas o servidor que possui a **chave privada** consegue decriptar os dados.
* Mesmo que o banco de dados seja exposto, e-mails e telefones permanecerão **ilegíveis**.

---

## 👻 Autoria

Desenvolvido por **Amanda Leite**
Projeto do **4º Bimestre – Aplicações com Banco de Dados e Criptografia (Python + MongoDB)**
Tema: **Halloween 🎃**

---

## 🪄 Licença

Este projeto é de uso acadêmico e pode ser adaptado livremente para fins de estudo ou demonstração.

```

---
