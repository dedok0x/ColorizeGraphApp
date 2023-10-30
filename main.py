import customtkinter

colors = ["red", "orange", "yellow", "green", "blue", "purple", "rose", "brown", "black"]
colors = {i: colors[i] for i in range(len(colors))}
class Vertex:
    def __init__(self, name, x=0, y=0, color_num=0):
        self.name = name
        self.color = colors[color_num]
        self.radius = 10
        self.x = x
        self.y = y
class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.graph = {}
        self.vertices = []
        self.edges = []

        self.field = customtkinter.CTkCanvas(self, bg="#404040")
        self.field.grid(row=0, column=0, sticky="nesw")
        self.label1 = customtkinter.CTkLabel(self, text=self.graph)
        self.label1.grid(row=1, column=0, sticky="ew")
    def clearField(self):
        self.field.delete("all")

    def add_vertex(self):
        vertex_num = len(self.graph)
        vertex_name = chr(65 + vertex_num)  # преобразуем номер вершины в символ латинского алфавита
        self.vertices.append(Vertex(vertex_name))
        self.graph[self.vertices[vertex_num].name] = []  # добавляем новую вершину в список связности
        self.label1.configure(text=self.graph)
    def add_edge(self):
        pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ColorizeGraphApp")
        self.geometry("640x640")
        self.grid_columnconfigure((0, 1), weight=1)

        self.add_btn = customtkinter.CTkButton(self, text="Добавить вершину", command=self.add_btn_click)
        self.add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nesw", rowspan=2)

        self.connect_btn = customtkinter.CTkButton(self, text="Связать вершины", command=self.connect_btn_click)
        self.connect_btn.grid(row=0, column=1, padx=0, pady=5, sticky="ew", columnspan=1)

        self.connected_entry = customtkinter.CTkEntry(self, placeholder_text="Вершина 1")
        self.connected_entry.grid(row=1, column=1, pady=5, sticky="sw", columnspan=1)

        self.connected_with_entry = customtkinter.CTkEntry(self, placeholder_text="Вершина 2")
        self.connected_with_entry.grid(row=1, column=1, pady=5, sticky="se", columnspan=1)

        self.my_frame = GraphFrame(master=self)
        self.my_frame.grid_rowconfigure(0, minsize=500)
        self.my_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)

        self.colorize_btn = customtkinter.CTkButton(self, text="Раскрасить граф", command=self.colorizeGraph)
        self.colorize_btn.grid(row=4, column=0, pady=5, sticky="ew", columnspan=2)

        self.clear_btn = customtkinter.CTkButton(self, text="Очистить поле", command=self.clear_btn_click)
        self.clear_btn.grid(row=5, column=0, pady=5, sticky="ew", columnspan=2)

    def add_btn_click(self):
        self.my_frame.add_vertex()

    def connect_btn_click(self):

        if (self.connected_with_entry.get(), self.connected_entry.get() in self.my_frame.graph.keys()) \
                and (self.connected_with_entry.get() not in self.my_frame.graph[self.connected_entry.get()]):
            if self.connected_with_entry.get() == self.connected_entry.get():
                self.my_frame.graph[self.connected_entry.get()].append(self.connected_with_entry.get())
            else:
                self.my_frame.graph[self.connected_entry.get()].append(self.connected_with_entry.get())
                self.my_frame.graph[self.connected_with_entry.get()].append(self.connected_entry.get())
        self.my_frame.label1.configure(text=self.my_frame.graph)

    def colorizeGraph(self):
        pass

    def clear_btn_click(self):
        self.my_frame.clearField()
        self.my_frame.graph = {}
        self.my_frame.vertices = []
        self.my_frame.edges = []
        self.my_frame.label1.configure(text=self.my_frame.graph)

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
    app.mainloop()

if __name__ == "__main__":
    main()
