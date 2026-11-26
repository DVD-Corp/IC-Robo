# 🐙 Guia Básico de Git e GitHub para a Equipe (Do Zero!)

Bem-vindos ao repositório do projeto **IC-Robo**! Este guia foi feito pensando em quem **nunca usou Git ou GitHub antes**. Aqui você vai entender o que eles são e como baixar o projeto, fazer alterações no código do robô e enviar sua parte sem medo de quebrar o trabalho dos colegas.

---

## 1. O que são Git e GitHub? (Sem complicação)

Imagine que estamos escrevendo o código do robô e, em vez de ficar enviando arquivos pelo WhatsApp como `Interface_Planejador_v2_final_agora_vai.py`, temos um **histórico inteligente na nuvem**:

- **Git:** É o programa instalado no seu computador que tira "fotos" (chamadas de **commits**) do projeto sempre que você termina uma alteração. Se algo der errado, dá para voltar no tempo!
- **GitHub:** É o site na internet ([github.com/DVD-Corp/IC-Robo](https://github.com/DVD-Corp/IC-Robo)) onde essa pasta do projeto fica guardada para toda a equipe acessar.
- **GitHub Project (Nosso Quadro de Tarefas):** Funciona exatamente como o **Trello**. Fica em [github.com/orgs/DVD-Corp/projects/3](https://github.com/orgs/DVD-Corp/projects/3) com as colunas:
  - **Todo** (A fazer)
  - **In Progress** (Fazendo)
  - **Done** (Concluído)

---

## 2. Primeiros Passos (Só precisa fazer uma única vez)

1. **Crie sua conta no GitHub:**
   Acesse [github.com](https://github.com/) e crie uma conta gratuita (se já tiver, basta fazer login). Passe seu nome de usuário para o grupo para ser adicionado com permissão no projeto.
2. **Escolha como prefere usar no seu computador:**
   Você pode usar **com interface visual (clicando em botões)** ou **pelo terminal/VS Code**. Para quem está começando do zero, o aplicativo visual **GitHub Desktop** é o caminho mais fácil!

---

## 3. Caminho A: Usando o GitHub Desktop (Mais Fácil — Sem Comandos!)

O **GitHub Desktop** é um aplicativo oficial com botões visuais para você não precisar decorar comandos de terminal.

### Passo 1: Instalar e entrar na conta
1. Baixe e instale em: [desktop.github.com](https://desktop.github.com/)
2. Abra o programa, clique em **Sign in to GitHub.com** e faça login na sua conta.

### Passo 2: Baixar o projeto para o seu PC (`Clone`)
1. No GitHub Desktop, clique em **File** $\rightarrow$ **Clone repository...**
2. Vá na aba **URL** e cole:
   ```text
   https://github.com/DVD-Corp/IC-Robo.git
   ```
3. Escolha em qual pasta do seu computador quer salvar e clique em **Clone**.
4. Pronto! Todos os PDFs e o código Python (`src/Interface_PlanejadorRobô2.py`) já estarão numa pasta normal no seu computador.

### Passo 3: O ciclo do dia a dia (3 cliques)
Sempre que for mexer no código do robô (no VS Code, PyCharm, IDLE ou CoppeliaSim):

1. **🔄 Antes de começar a programar (`Fetch / Pull`):**
   Abra o GitHub Desktop e clique no botão **Fetch origin** (no topo). Se aparecer **Pull origin**, clique nele! Isso traz para o seu PC tudo de novo que seus colegas enviaram.
2. **💻 Programe normalmente:**
   Abra a pasta do projeto no seu editor, altere os arquivos ou adicione códigos novos e salve (`Ctrl + S`).
3. **📸 Salve e envie para o grupo (`Commit` + `Push`):**
   - Volte no GitHub Desktop. Ele vai mostrar na esquerda todos os arquivos que você alterou.
   - No canto inferior esquerdo, escreva uma frase curta dizendo o que você fez (ex.: *"Adiciona classe CelulaAmbiente"*).
   - Clique no botão azul **Commit to master**.
   - Em seguida, clique em **Push origin** (no topo) para enviar para a nuvem!

---

## 4. Caminho B: Usando Comandos no Terminal / VS Code

Se você já instalou o [Git](https://git-scm.com/downloads) e prefere rodar comandos no terminal do VS Code ou PowerShell, você só precisa conhecer **5 comandos**:

### 1️⃣ Baixar o projeto pela primeira vez (`git clone`)
Abra o terminal na pasta onde quer guardar o projeto e rode:
```bash
git clone https://github.com/DVD-Corp/IC-Robo.git
cd IC-Robo
```

### 2️⃣ Atualizar seu computador antes de começar (`git pull`)
Sempre rode isso **antes** de começar a programar no dia, para baixar o que os colegas fizeram:
```bash
git pull
```

### 3️⃣ Ver o que você alterou (`git status`)
Mostra quais arquivos foram modificados ou criados:
```bash
git status
```

### 4️⃣ Preparar e salvar suas alterações (`git add` e `git commit`)
```bash
# 1. Prepara todos os arquivos alterados
git add .

# 2. Cria um ponto salvo com uma mensagem explicando o que fez
git commit -m "Descreva aqui o que voce fez"
```

### 5️⃣ Enviar para o GitHub (`git push`)
Envia suas alterações salvas para o site do GitHub:
```bash
git push
```

---

## 5. Dicionário Rápido (Para não se perder nos nomes)

| Termo | O que significa na prática? |
| :--- | :--- |
| **Repositório (Repo)** | É a pasta do nosso projeto (`IC-Robo`) guardada no GitHub. |
| **Clone (Clonar)** | Baixar o repositório do GitHub para o seu computador pela primeira vez. |
| **Pull (Puxar)** | Atualizar a sua pasta local com as novidades que alguém do grupo subiu no GitHub. |
| **Commit** | Salvar um pacote de alterações com uma mensagem dizendo o que mudou. |
| **Push (Empurrar)** | Enviar os seus *commits* do seu computador para o site do GitHub. |
| **Branch (Ramo)** | Uma "linha do tempo" do código. A nossa linha principal se chama **`master`**. |

---

## 6. Três Regras de Ouro para a Equipe 🏆

1. **Sempre dê `Pull` antes de começar:** Antes de editar qualquer arquivo, atualize o projeto (`Pull`) para não trabalhar em cima de uma versão antiga.
2. **Escreva mensagens claras no `Commit`:** Em vez de escrever *"teste"* ou *"mudança"*, escreva *"Cria classe CNAPmax"* ou *"Corrige movimento diagonal no simulador"*.
3. **Avise no grupo / Mova o card no Project:** Quando pegar uma tarefa no nosso [Quadro do Projeto](https://github.com/orgs/DVD-Corp/projects/3), mova o card para **In Progress**, e quando fizer o `Push`, mova para **Done**!
