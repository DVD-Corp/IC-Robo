import tkinter as tk
from tkinter import ttk, messagebox

DIRECOES = {
    1: (0, 1),
    2: (1, 1),
    3: (1, 0),
    4: (1, -1),
    5: (0, -1),
    6: (-1, -1),
    7: (-1, 0),
    8: (-1, 1),
}

NOMES_MOVIMENTOS = {
    1: "Cima",
    2: "Diagonal Superior Direita",
    3: "Direita",
    4: "Diagonal Inferior Direita",
    5: "Baixo",
    6: "Diagonal Inferior Esquerda",
    7: "Esquerda",
    8: "Diagonal Superior Esquerda",
}


def sinal(valor):
    """Determina o sentido do movimento."""
    if valor > 0:
        return 1
    elif valor < 0:
        return -1
    return 0


def encontrar_comando(dx, dy):
    """Encontra o comando correspondente à direção."""
    direcao = (sinal(dx), sinal(dy))
    for comando, movimento in DIRECOES.items():
        if movimento == direcao:
            return comando
    return None


def gerar_sequencia(xo, yo, xd, yd):
    """Gera a sequência de movimentos até o destino."""
    x, y = xo, yo
    sequencia = []

    while x != xd or y != yd:
        diferenca_x = xd - x
        diferenca_y = yd - y

        comando = encontrar_comando(diferenca_x, diferenca_y)
        if comando is None:
            break

        movimento_x, movimento_y = DIRECOES[comando]
        x += movimento_x
        y += movimento_y

        sequencia.append(comando)

    return sequencia

# Interface Gráfica

class SimuladorRoboApp:
    # Configurações do grid
    LIMITE = 10
    ESPACAMENTO = 26      # distância em pixels entre células
    MARGEM = 30           # margem interna do canvas
    LADO_ROBO = 18         # tamanho do quadrado do robô
    RAIO_PONTO = 2         # raio dos pontinhos (células disponíveis)
    VELOCIDADE_MS = 250    # intervalo entre passos da animação
    RAIO_TRILHA = 5        # raio dos marcadores do rastro
    COR_TRILHA = "#d9a7f2"  # cor do rastro 
    COR_LINHA_TRILHA = "#c084f5"

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Robô - Plano Cartesiano")
        self.root.configure(bg="#eef1f6")

        # Estado do robô
        self.xo = 0
        self.yo = 0
        self.xd = None
        self.yd = None
        self.pos_x = 0
        self.pos_y = 0
        self.sequencia = []
        self.indice_passo = 0
        self.animando = False
        self.job_animacao = None

        # Histórico do rastro (em coordenadas de grid) para permitir
        # redesenhar tudo corretamente quando a tela for redimensionada
        self.trilha_celulas = []
        self.trilha_segmentos = []

        # Tamanho de referência da última renderização do canvas,
        # usado para recalcular o espaçamento ao redimensionar
        self._largura_canvas = None
        self._altura_canvas = None

        # Deslocamento usado para manter o plano cartesiano sempre
        # centralizado dentro do canvas, mesmo quando ele não é quadrado
        self.offset_x = 0.0
        self.offset_y = 0.0

        self._montar_layout()
        self._desenhar_grid()
        self._desenhar_robo()

        # Torna o plano cartesiano responsivo ao tamanho da janela/canvas,
        # sem alterar nenhuma outra lógica do simulador
        self.canvas.bind("<Configure>", self._ao_redimensionar_canvas)

    
    # Layout
  
    def _montar_layout(self):
        container = tk.Frame(self.root, bg="#eef1f6")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        # Painel esquerdo: Canvas do plano cartesiano (responsivo)
        lado_canvas = 2 * self.LIMITE * self.ESPACAMENTO + 2 * self.MARGEM
        frame_canvas = tk.Frame(
            container, bg="white", bd=1, relief="solid",
            highlightbackground="#d0d5dd", highlightthickness=1
        )
        frame_canvas.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(
            frame_canvas, width=lado_canvas, height=lado_canvas,
            bg="#fbfbfd", highlightthickness=0
        )
        self.canvas.pack(padx=8, pady=8, fill="both", expand=True)

        # Painel direito: controles (largura fixa, não acompanha o resize)
        painel = tk.Frame(container, bg="#eef1f6", width=220)
        painel.pack(side="left", fill="y", padx=(16, 0))
        painel.pack_propagate(False)

        # Caixa de entrada de coordenadas
        caixa_entradas = tk.Frame(
            painel, bg="#f5f7fb", bd=1, relief="solid",
            highlightbackground="#d0d5dd", highlightthickness=1
        )
        caixa_entradas.pack(fill="x", pady=(0, 12))

        self.entry_xo = self._criar_campo(caixa_entradas, "Xo:", 0, 0)
        self.entry_yo = self._criar_campo(caixa_entradas, "Yo:", 0, 2)
        self.entry_xd = self._criar_campo(caixa_entradas, "Xd:", 1, 0)
        self.entry_yd = self._criar_campo(caixa_entradas, "Yd:", 1, 2)

        # Botões
        self.btn_executar = tk.Button(
            painel, text="▶  Executar", bg="#2f6fed", fg="white",
            activebackground="#2657c0", activeforeground="white",
            relief="flat", font=("Segoe UI", 10, "bold"),
            padx=10, pady=8, command=self.executar
        )
        self.btn_executar.pack(fill="x", pady=(0, 6))

        self.btn_parar = tk.Button(
            painel, text="■  Parar", bg="#f5f7fb", fg="#111827",
            relief="solid", bd=1, font=("Segoe UI", 10),
            padx=10, pady=8, command=self.parar
        )
        self.btn_parar.pack(fill="x", pady=(0, 6))

        self.btn_resetar = tk.Button(
            painel, text="↻  Resetar", bg="#f5f7fb", fg="#111827",
            relief="solid", bd=1, font=("Segoe UI", 10),
            padx=10, pady=8, command=self.resetar
        )
        self.btn_resetar.pack(fill="x", pady=(0, 16))

        # Informações do robô
        frame_info = tk.LabelFrame(
            painel, text="Informações do Robô", bg="#eef1f6",
            font=("Segoe UI", 10, "bold"), padx=10, pady=10
        )
        frame_info.pack(fill="x", pady=(0, 12))

        tk.Label(frame_info, text="Posição de origem:", bg="#eef1f6",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
        self.lbl_origem = tk.Entry(frame_info, width=14, state="readonly",
                                    justify="center")
        self.lbl_origem.grid(row=0, column=1, padx=(8, 0))

        tk.Label(frame_info, text="Posição de destino:", bg="#eef1f6",
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=4)
        self.lbl_destino = tk.Entry(frame_info, width=14, state="readonly",
                                     justify="center")
        self.lbl_destino.grid(row=1, column=1, padx=(8, 0))

        # Legenda
        frame_legenda = tk.LabelFrame(
            painel, text="Legenda", bg="#eef1f6",
            font=("Segoe UI", 10, "bold"), padx=10, pady=10
        )
        frame_legenda.pack(fill="x")

        linha_robo = tk.Frame(frame_legenda, bg="#eef1f6")
        linha_robo.pack(fill="x", pady=4, anchor="w")
        tk.Canvas(linha_robo, width=16, height=16, bg="#a020c0",
                  highlightthickness=0).pack(side="left")
        tk.Label(linha_robo, text="  Robô", bg="#eef1f6",
                 font=("Segoe UI", 9)).pack(side="left")

        linha_celula = tk.Frame(frame_legenda, bg="#eef1f6")
        linha_celula.pack(fill="x", pady=4, anchor="w")
        pontinho = tk.Canvas(linha_celula, width=16, height=16, bg="#eef1f6",
                              highlightthickness=0)
        pontinho.pack(side="left")
        pontinho.create_oval(6, 6, 10, 10, fill="black")
        tk.Label(linha_celula, text="  Célula disponível", bg="#eef1f6",
                 font=("Segoe UI", 9)).pack(side="left")

        linha_trilha = tk.Frame(frame_legenda, bg="#eef1f6")
        linha_trilha.pack(fill="x", pady=4, anchor="w")
        marcador_trilha = tk.Canvas(linha_trilha, width=16, height=16, bg="#eef1f6",
                                     highlightthickness=0)
        marcador_trilha.pack(side="left")
        marcador_trilha.create_oval(4, 4, 12, 12, fill="#d9a7f2", outline="")
        tk.Label(linha_trilha, text="  Rastro percorrido", bg="#eef1f6",
                 font=("Segoe UI", 9)).pack(side="left")

        # Barra de status (mostra o passo atual da animação)
        self.status_var = tk.StringVar(value="Pronto.")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var, bg="#dfe4ee",
            anchor="w", font=("Segoe UI", 9), padx=10, pady=4
        )
        status_bar.pack(fill="x", side="bottom")

    def _criar_campo(self, parent, rotulo, linha, coluna):
        tk.Label(parent, text=rotulo, bg="#f5f7fb",
                 font=("Segoe UI", 10)).grid(
            row=linha, column=coluna, sticky="e", padx=(10, 4), pady=10
        )
        entry = tk.Entry(parent, width=6, justify="center")
        entry.grid(row=linha, column=coluna + 1, padx=(0, 10), pady=10)
        return entry

    # Conversão de coordenadas do grid <-> canvas

    def _para_canvas(self, gx, gy):
        centro = self.MARGEM + self.LIMITE * self.ESPACAMENTO
        cx = self.offset_x + centro + gx * self.ESPACAMENTO
        cy = self.offset_y + centro - gy * self.ESPACAMENTO
        return cx, cy

    def _centro_celula_para_canvas(self, gx, gy):
        """Converte o índice de uma célula (não um ponto de grade) para o
        centro dessa célula no canvas — usado só para os pontinhos, que
        ficam no meio de cada quadrado, e não sobre as linhas/interseções
        por onde o robô se move."""
        cx, cy = self._para_canvas(gx, gy)
        return cx + self.ESPACAMENTO / 2, cy - self.ESPACAMENTO / 2

    # Desenho do grid, eixos e robô
 
    def _desenhar_grid(self):
        self.canvas.delete("grid", "eixo")

        # Pontinhos (células disponíveis) — ficam no centro de cada
        # quadrado da grade, não sobre as interseções das linhas.
        # Raio pequeno e fixo (não cresce junto com o espaçamento),
        # só encolhe um pouco se a célula ficar muito pequena.
        r = min(self.RAIO_PONTO, self.ESPACAMENTO * 0.12)
        r = max(r, 1)
        for gx in range(-self.LIMITE, self.LIMITE):
            for gy in range(-self.LIMITE, self.LIMITE):
                cx, cy = self._centro_celula_para_canvas(gx, gy)
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    fill="black", outline="", tags="grid"
                )

        # Linhas leves da grade (as bordas de cada célula) — sempre
        # desenhadas por cima do offset de centralização, cobrindo todo
        # o plano de -LIMITE a +LIMITE
        inicio = self.offset_x + self.MARGEM
        fim = self.offset_x + self.MARGEM + 2 * self.LIMITE * self.ESPACAMENTO
        inicio_v = self.offset_y + self.MARGEM
        fim_v = self.offset_y + self.MARGEM + 2 * self.LIMITE * self.ESPACAMENTO
        for i in range(2 * self.LIMITE + 1):
            pos_x = self.offset_x + self.MARGEM + i * self.ESPACAMENTO
            pos_y = self.offset_y + self.MARGEM + i * self.ESPACAMENTO
            self.canvas.create_line(pos_x, inicio_v, pos_x, fim_v, fill="#e5e7eb", tags="grid")
            self.canvas.create_line(inicio, pos_y, fim, pos_y, fill="#e5e7eb", tags="grid")

        # Eixos X e Y com setas
        cx0, cy0 = self._para_canvas(-self.LIMITE, 0)
        cx1, cy1 = self._para_canvas(self.LIMITE, 0)
        self.canvas.create_line(cx0, cy0, cx1, cy1, width=2, arrow="both", tags="eixo")

        cy0v, cx0v = self._para_canvas(0, -self.LIMITE)[1], self._para_canvas(0, -self.LIMITE)[0]
        px0, py0 = self._para_canvas(0, -self.LIMITE)
        px1, py1 = self._para_canvas(0, self.LIMITE)
        self.canvas.create_line(px0, py0, px1, py1, width=2, arrow="both", tags="eixo")

        self.canvas.create_text(cx1 + 12, cy1, text="X", font=("Segoe UI", 11, "bold"), tags="eixo")
        self.canvas.create_text(px1, py1 - 14, text="Y", font=("Segoe UI", 11, "bold"), tags="eixo")

        # Redesenha as linhas da grade atrás dos eixos/pontos
        self.canvas.tag_lower("grid")

    def _ao_redimensionar_canvas(self, event):
        """Recalcula o espaçamento da grade quando o canvas muda de tamanho
        (janela redimensionada), mantendo o plano cartesiano centralizado
        e proporcional, sem alterar nenhuma outra regra do simulador."""
        largura, altura = event.width, event.height

        if largura < 50 or altura < 50:
            return

        if (largura, altura) == (self._largura_canvas, self._altura_canvas):
            return
        self._largura_canvas, self._altura_canvas = largura, altura

        lado_disponivel = min(largura, altura)
        novo_espacamento = (lado_disponivel - 2 * self.MARGEM) / (2 * self.LIMITE)
        novo_espacamento = max(novo_espacamento, 4)  # nunca fica ilegível

        self.ESPACAMENTO = novo_espacamento

        # Centraliza o plano cartesiano (que é sempre um quadrado) dentro
        # do canvas, mesmo quando o canvas não é quadrado
        lado_grade = 2 * self.LIMITE * self.ESPACAMENTO + 2 * self.MARGEM
        self.offset_x = (largura - lado_grade) / 2
        self.offset_y = (altura - lado_grade) / 2

        self._desenhar_grid()
        self._redesenhar_trilha()
        self._desenhar_robo()

    def _desenhar_robo(self):
        self.canvas.delete("robo")
        cx, cy = self._para_canvas(self.pos_x, self.pos_y)
        lado = self.LADO_ROBO / 2
        self.canvas.create_rectangle(
            cx - lado, cy - lado, cx + lado, cy + lado,
            fill="#a020c0", outline="", tags="robo"
        )
        self.canvas.tag_raise("robo")

    def _limpar_trilha(self):
        self.canvas.delete("trilha")
        self.trilha_celulas = []
        self.trilha_segmentos = []

    def _marcar_trilha(self, gx, gy, registrar=True):
        """Desenha um marcador de rastro na célula (gx, gy)."""
        cx, cy = self._para_canvas(gx, gy)
        r = self.RAIO_TRILHA
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=self.COR_TRILHA, outline="", tags="trilha"
        )
        self.canvas.tag_raise("robo")
        if registrar:
            self.trilha_celulas.append((gx, gy))

    def _tracar_trilha(self, gx_origem, gy_origem, gx_destino, gy_destino, registrar=True):
        """Desenha o segmento de linha do rastro entre duas células vizinhas."""
        cx0, cy0 = self._para_canvas(gx_origem, gy_origem)
        cx1, cy1 = self._para_canvas(gx_destino, gy_destino)
        self.canvas.create_line(
            cx0, cy0, cx1, cy1, fill=self.COR_LINHA_TRILHA,
            width=3, tags="trilha"
        )
        self.canvas.tag_raise("robo")
        if registrar:
            self.trilha_segmentos.append((gx_origem, gy_origem, gx_destino, gy_destino))

    def _redesenhar_trilha(self):
        """Reconstrói o rastro na tela a partir do histórico guardado —
        usado depois que o canvas é redimensionado."""
        self.canvas.delete("trilha")
        for gx0, gy0, gx1, gy1 in self.trilha_segmentos:
            self._tracar_trilha(gx0, gy0, gx1, gy1, registrar=False)
        for gx, gy in self.trilha_celulas:
            self._marcar_trilha(gx, gy, registrar=False)
    
    # Ações dos botões

    def _ler_inteiro(self, entry, nome_campo):
        texto = entry.get().strip()
        if texto == "":
            raise ValueError(f"Preencha o campo {nome_campo}.")
        try:
            valor = int(texto)
        except ValueError:
            raise ValueError(f"O campo {nome_campo} deve ser um número inteiro.")
        if abs(valor) > self.LIMITE:
            raise ValueError(
                f"O campo {nome_campo} deve estar entre -{self.LIMITE} e {self.LIMITE}."
            )
        return valor

    def executar(self):
        if self.animando:
            return

        try:
            xo = self._ler_inteiro(self.entry_xo, "Xo")
            yo = self._ler_inteiro(self.entry_yo, "Yo")
            xd = self._ler_inteiro(self.entry_xd, "Xd")
            yd = self._ler_inteiro(self.entry_yd, "Yd")
        except ValueError as erro:
            messagebox.showwarning("Entrada inválida", str(erro))
            return

        self.xo, self.yo = xo, yo
        self.xd, self.yd = xd, yd
        self.pos_x, self.pos_y = xo, yo

        self._limpar_trilha()
        self._marcar_trilha(xo, yo)

        self._atualizar_info(f"({xo}, {yo})", f"({xd}, {yd})")
        self._desenhar_robo()

        self.sequencia = gerar_sequencia(xo, yo, xd, yd)
        self.indice_passo = 0

        if not self.sequencia:
            self.status_var.set("O robô já está na posição de destino.")
            return

        self.status_var.set(
            f"Executando... {len(self.sequencia)} passo(s) planejado(s)."
        )
        self.animando = True
        self._proximo_passo()

    def _proximo_passo(self):
        if not self.animando:
            return

        if self.indice_passo >= len(self.sequencia):
            self.animando = False
            self.status_var.set(
                f"Concluído! Posição final: ({self.pos_x}, {self.pos_y})"
            )
            return

        comando = self.sequencia[self.indice_passo]
        dx, dy = DIRECOES[comando]
        x_anterior, y_anterior = self.pos_x, self.pos_y
        self.pos_x += dx
        self.pos_y += dy
        self.indice_passo += 1

        self._tracar_trilha(x_anterior, y_anterior, self.pos_x, self.pos_y)
        self._marcar_trilha(self.pos_x, self.pos_y)
        self._desenhar_robo()
        self.status_var.set(
            f"Passo {self.indice_passo}/{len(self.sequencia)}: "
            f"{NOMES_MOVIMENTOS[comando]} -> ({self.pos_x}, {self.pos_y})"
        )

        self.job_animacao = self.root.after(self.VELOCIDADE_MS, self._proximo_passo)

    def parar(self):
        self.animando = False
        if self.job_animacao is not None:
            self.root.after_cancel(self.job_animacao)
            self.job_animacao = None
        self.status_var.set(f"Parado em ({self.pos_x}, {self.pos_y}).")

    def resetar(self):
        self.parar()
        self.pos_x, self.pos_y = 0, 0
        self.xo = self.yo = self.xd = self.yd = None
        self.sequencia = []
        self.indice_passo = 0

        for entry in (self.entry_xo, self.entry_yo, self.entry_xd, self.entry_yd):
            entry.delete(0, tk.END)

        self._limpar_trilha()
        self._atualizar_info("", "")
        self._desenhar_robo()
        self.status_var.set("Pronto.")

    def _atualizar_info(self, origem_txt, destino_txt):
        for lbl, txt in ((self.lbl_origem, origem_txt), (self.lbl_destino, destino_txt)):
            lbl.configure(state="normal")
            lbl.delete(0, tk.END)
            lbl.insert(0, txt)
            lbl.configure(state="readonly")

def main():
    root = tk.Tk()
    root.geometry("900x650")
    root.minsize(700, 500)
    root.resizable(True, True)
    app = SimuladorRoboApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()