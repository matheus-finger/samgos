import tkinter as tk
from tkinter import messagebox

class GeneAnnotatorApp:
    def __init__(self, root):
        self.root = root
        self.initUI()

        # Dicionário para rastrear as cores de fundo aplicadas em regiões específicas
        self.region_colors = {}

    def initUI(self):
        self.root.title("SAMGOS - Sistema de Anotação de Sequências de Genes e Outras Sequências")
        self.root.geometry("1300x650")

        self.titulo_label = tk.Label(self.root, text="Título da anotação:")
        self.titulo_label.pack()

        self.titulo_text = tk.Text(self.root, height=1, width=80)
        self.titulo_text.pack()

        # Espaço entre o título e os botões de cores
        space_label = tk.Label(self.root, text="", height=1)
        space_label.pack()

        self.color_frame = tk.Frame(self.root)
        self.color_frame.pack()

        colors = {"Região promotora": "lightblue", "Éxon": "lightgreen", "Íntron": "lightcoral", "Outro": "lightgray", "Sem Cor de Fundo": "white"}

        for color_name, color_value in colors.items():
            color_button = tk.Button(self.color_frame, text=color_name, bg=color_value, command=lambda c=color_value: self.apply_background_color(c))
            color_button.pack(side=tk.LEFT, padx=5)

        self.sequence_label = tk.Label(self.root, text="Sequência Genética:")
        self.sequence_label.pack()

        self.sequence_text = tk.Text(self.root, height=10, width=100)
        self.sequence_text.pack()

        self.dictionary_text = tk.Text(self.root, height=10, width=40)
        self.dictionary_text.pack()

        # Espaço entre a sequência e o botão de salvar
        space_label = tk.Label(self.root, text="", height=1)
        space_label.pack()

        self.save_button = tk.Button(self.root, text="Salvar Anotação", command=self.save_annotation)
        self.save_button.pack()

    def update_dictionary_text(self):
        self.dictionary_text.delete("1.0", tk.END)  # Limpa o conteúdo atual
        for (start, end), color in self.region_colors.items():
            self.dictionary_text.insert(tk.END, f"Start: {start}, End: {end}, Color: {color}\n")
    
    def remove_background_color(self, start, end):
        for color in self.sequence_text.tag_names():
            self.sequence_text.tag_remove(color, start, end)
    
    def apply_background_color(self, selected_color):
        sel_start = self.sequence_text.index(tk.SEL_FIRST)
        sel_end = self.sequence_text.index(tk.SEL_LAST)

        if sel_start and sel_end:
            # Mantém uma lista das regiões que serão atualizadas
            regions_to_update = []

            # Percorre as cores de fundo existentes
            for (start, end), color in list(self.region_colors.items()):
                if not (sel_end < start or sel_start > end):
                    # Calcula a interseção entre a seleção e a cor existente
                    intersection_start = max(start, sel_start)
                    intersection_end = min(end, sel_end)

                    # Verifica se a interseção é válida (não vazia)
                    if intersection_start <= intersection_end:
                        # Remove a entrada antiga do dicionário
                        if not (start > intersection_start and end < intersection_end):
                            print("Removendo:")
                            print((start,end))
                            del self.region_colors[(start, end)]
                        else:
                            print("Splitando:")
                            print((start,end))
                            intersect_numero = int(intersection_start[2:]) - 1
                            intersect_numero = "1." + str(intersect_numero)
                            intersect_numero2 = int(intersection_end[2:]) + 1
                            intersect_numero2 = "1." + str(intersect_numero2)
                            self.region_colors[(start, intersect_numero)] = color
                            self.region_colors[(intersect_numero2, end)] = color
                            del self.region_colors[(start, end)]
                            

                        # Divide a região em três partes: antes da interseção, interseção e depois da interseção
                        if start < intersection_start:
                            intersect_numero = int(intersection_start[2:]) - 1
                            intersect_numero = "1." + str(intersect_numero)
                            self.region_colors[(start, intersect_numero)] = color
                        if end > intersection_end:
                            intersect_numero = int(intersection_end[2:]) + 1
                            intersect_numero = "1." + str(intersect_numero)
                            self.region_colors[(intersect_numero, end)] = color
            
            # Remove a cor anterior

            for tag in self.sequence_text.tag_names():
                self.sequence_text.tag_remove(tag, sel_start, sel_end)

            # Aplica a nova cor de fundo na região selecionada
            self.sequence_text.tag_configure(selected_color, background=selected_color)
            self.sequence_text.tag_add(selected_color, sel_start, sel_end)

            # Atualiza o dicionário com a nova cor
            self.region_colors[(sel_start, sel_end)] = selected_color
            
            # Atualiza o texto do dicionário
            self.update_dictionary_text()

    def save_annotation(self):
        titulo = self.titulo_text.get("1.0", "end-1c")
        sequence = self.sequence_text.get("1.0", "end-1c")

        if titulo and sequence:
            formatted_text = f"Título da Anotação: {titulo}\nSequência: {sequence}\n"

            for (start, end), color in self.region_colors.items():
                formatted_text += f"Trecho colorido ({color}): {self.sequence_text.get(start, end)}\n"

            # Substitui "gene_annotations.txt" pelo título + extensão .txt
            file_name = f"{titulo}.txt"

            with open(file_name, "w") as f:
                f.write(formatted_text)
            messagebox.showinfo("Anotação Salva", "Anotação salva com sucesso!")
        else:
            messagebox.showerror("Erro", "Preencha o título e a sequência antes de salvar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneAnnotatorApp(root)
    root.mainloop()
