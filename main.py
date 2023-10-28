import customtkinter

class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ColorizeGraphApp")
        self.geometry("640x640")
        self.grid_columnconfigure((0, 1), weight=1)

        self.add_btn = customtkinter.CTkButton(self, text="Добавить вершину", command=self.add_btn_click)
        self.add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nesw", rowspan=2)

        self.connected_entry = customtkinter.CTkEntry(self, placeholder_text="Вершина 1")
        self.connected_entry.grid(row=1, column=1, pady=5, sticky="sw", columnspan=1)

        self.connected_with_entry = customtkinter.CTkEntry(self, placeholder_text="Вершина 2")
        self.connected_with_entry.grid(row=1, column=1, pady=5, sticky="se", columnspan=1)

        self.connect_btn = customtkinter.CTkButton(self, text="Связать вершины", command=self.connect_btn_click)
        self.connect_btn.grid(row=0, column=1, padx=0, pady=5, sticky="ew", columnspan=1)

        self.my_frame = GraphFrame(master=self)
        self.my_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)

        self.connect_btn = customtkinter.CTkButton(self, text="Раскрасить граф", command=self.colorizeGraph)
        self.connect_btn.grid(row=4, column=0, pady=5, sticky="ew", columnspan=2)


    def add_btn_click(self):
        pass

    def connect_btn_click(self):
        pass

    def colorizeGraph(self):
        pass

def greedy_coloring(graph):
    def get_neighbors(vertex, graph):
        return graph[vertex]

    def get_color(vertex, color_map, graph):
        used_colors = set()
        for neighbor in get_neighbors(vertex, graph):
            if neighbor in color_map:
                used_colors.add(color_map[neighbor])
        for color in range(len(graph)):
            if color not in used_colors:
                return color
        return 0

    color_map = {}
    for vertex in graph:
        color_map[vertex] = get_color(vertex, color_map, graph)
    return color_map

def main():
    app = App()

    graph = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B", "D"],
        "D": ["D"]
    }
    color_map = greedy_coloring(graph)
    print(color_map)

    app.mainloop()

if __name__ == "__main__":
    main()
