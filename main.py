import customtkinter
import tkinter

colors = ["white", "red", "orange", "yellow", "green", "blue", "purple", "brown"]
colors = {i: colors[i] for i in range(len(colors))}


class Vertex:
    def __init__(self, name, x, y, radius=30, color_num=0):
        self.name = name
        self.color = colors[color_num]
        self.radius = radius
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2


class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.graph = {}
        self.vertices = {}
        self.edges = []
        self.color_map = {}

        self.field = customtkinter.CTkCanvas(self, bg="#404040")
        self.field.grid(row=0, column=0, sticky="nesw")
        self.label1 = customtkinter.CTkLabel(self, text=f"Граф: {self.graph}", font=("Arial", 14), text_color="white")
        self.label1.grid(row=1, column=0, sticky="ew")
        self.label2 = customtkinter.CTkLabel(self, text=f"Цвета: {self.color_map}", font=("Arial", 14), text_color="white")
        self.label2.grid(row=2, column=0, sticky="ew")

    def clear_field(self):
        self.field.delete("all")
        self.graph = {}
        self.color_map = {}
        self.vertices = {}
        self.edges = []
        self.label1.configure(text=self.graph)

    def add_vertex(self, event):
        vertex_name = chr(65 + len(self.graph))  # преобразуем номер вершины в символ латинского алфавита
        self.vertices[vertex_name] = Vertex(vertex_name, event.x, event.y)
        self.draw_vertex(self.vertices[vertex_name])
        self.graph[self.vertices[vertex_name].name] = []  # добавляем новую вершину в список связности

        self.field.unbind("<Button-1>")
        self.label1.configure(text=f"Граф: {self.graph}", font=("Arial", 14), text_color="white")
        self.label2.configure(text=f"Цвета: {self.color_map}", font=("Arial", 14), text_color="white")

    def add_edge(self, v1, v2):
        if (v1, v2 in self.graph.keys()) and (v2 not in self.graph[v1]):
            if v1 == v2:
                self.graph[v1].append(v2)
                self.edges.append(Edge(v1, v2))
                self.draw_edge(self.edges[-1])
            else:
                self.graph[v1].append(v2)
                self.graph[v2].append(v1)
                self.edges.append(Edge(v1, v2))
                self.draw_edge(self.edges[-1])

        self.label1.configure(text=f"Граф: {self.graph}", font=("Arial", 14), text_color="white")

    def draw_vertex(self, vertex: Vertex):
        x = vertex.x
        y = vertex.y
        r = vertex.radius
        color = vertex.color
        self.field.create_oval(x - r, y - r, x + r, y + r, fill=color)
        self.field.create_text(x-r//3, y-r//3, text=vertex.name, font=("Arial", 12, "bold"))

    def draw_edge(self, edge: Edge):
        x0, y0 = self.vertices[edge.v1].get()
        x1, y1 = self.vertices[edge.v2].get()
        if edge.v1 == edge.v2:
            self.field.create_oval(x0+10, y0+10, x0-60, y0-60, width=2)
        else:
            self.field.create_line(x0, y0, x1, y1, width=3)

    def colorize(self):
        self.field.delete("all")
        self.color_map = greedy_coloring(self.graph)

        for vertex in self.vertices.values():
            vertex.color = colors[self.color_map[vertex.name]]
            self.draw_vertex(vertex)
        for edge in self.edges:
            self.draw_edge(edge)

        self.label2.configure(text=f"Цвета: {self.color_map}", font=("Arial", 14), text_color="white")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ColorizeGraphApp")
        self.geometry("650x650")
        self.grid_columnconfigure((0, 1), weight=1)

        self.add_btn = customtkinter.CTkButton(self, text="Добавить вершину", command=self.add_btn_click)
        self.add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nesw", rowspan=2)

        self.connect_btn = customtkinter.CTkButton(self, text="Связать вершины", command=self.connect_btn_click)
        self.connect_btn.grid(row=0, column=1, padx=0, pady=5, sticky="ew", columnspan=1)

        self.connect_entry = customtkinter.CTkComboBox(self, values=[""])
        self.connect_entry.grid(row=1, column=1, pady=5, sticky="sw", columnspan=1)
        self.connect_with_entry = customtkinter.CTkComboBox(self, values=[""])
        self.connect_with_entry.grid(row=1, column=1, pady=5, sticky="se", columnspan=1)

        self.my_frame = GraphFrame(master=self)
        self.my_frame.grid_rowconfigure(0, minsize=500)
        self.my_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)

        self.colorize_btn = customtkinter.CTkButton(self, text="Раскрасить граф", command=self.colorize_graph)
        self.colorize_btn.grid(row=4, column=0, pady=5, sticky="ew", columnspan=2)

        self.clear_btn = customtkinter.CTkButton(self, text="Очистить поле", command=self.clear_btn_click)
        self.clear_btn.grid(row=5, column=0, pady=5, sticky="ew", columnspan=2)

    def add_btn_click(self):

        self.my_frame.label1.configure(text="Чтобы добавить вершину нажмите на поле", font=("Arial", 16, "bold"), text_color="yellow")
        self.my_frame.label2.configure(text="")
        self.my_frame.field.bind("<Button-1>", lambda event: self.my_frame.add_vertex(event))

    def connect_btn_click(self):
        v1 = self.connect_entry.get()
        v2 = self.connect_with_entry.get()
        if (v1, v2) in list(self.my_frame.graph):
            self.my_frame.label1.configure(text="Ошибка ввода. Поля пустые, либо не соответсвуют существующим вершинам",
                                           font=("Arial", 14, "bold"), text_color="red")
            self.my_frame.label2.configure(text="")
        else:
            self.my_frame.add_edge(v1, v2)

    def colorize_graph(self):
        self.my_frame.colorize()

    def clear_btn_click(self):
        self.my_frame.clear_field()


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
