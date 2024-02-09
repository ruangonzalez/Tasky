# lista de tarefas com flet
import flet as ft
import sqlite3

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
            background=ft.colors.LIME_ACCENT_200,
            on_background=ft.colors.PURPLE_700,
            surface=ft.colors.PURPLE_200,
            on_surface=ft.colors.PURPLE_700,
            surface_tint=ft.colors.LIME_ACCENT_200,
            surface_variant=ft.colors.BROWN_400,
            on_surface_variant=ft.colors.PURPLE_700,
            primary=ft.colors.PURPLE_400,
            on_primary=ft.colors.LIME_ACCENT_200,
            primary_container=ft.colors.LIME_ACCENT_200,
            on_primary_container=ft.colors.PURPLE_400,
            outline=ft.colors.LIME_ACCENT_700,
            )
        )
        self.page.window_width = 350
        self.page.window_height = 450
        self.page.window_resizable = False
        self.page.window_always_on_top = True
        self.page.title = "Tasky"
        self.task = ""
        self.view = "all"
        self.db_execute("CREATE TABLE IF NOT EXISTS tasks(name, status)")
        self.results = self.db_execute("SELECT * FROM tasks")        
        self.main_page()
        
    
    def db_execute(self, query, params = []):
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall()
    
    def checked(self, e):
        is_checked = e.control.value
        label = e.control.label
        
        if is_checked:
            self.db_execute('UPDATE tasks SET status = "complete" WHERE name = ?', params=[label])
        else:
            self.db_execute('UPDATE tasks SET status = "incomplete" WHERE name = ?', params=[label])
            
        if self.view == "all":
            self.results = self.db_execute("SELECT * FROM tasks")
        else: 
            self.results = self.db_execute("SELECT * FROM tasks WHERE status = ?", params=[self.view])
        self.update_task_list()
        
    def tasks_container(self):
        return ft.Container(
            height=self.page.height == 0.8,
            content = ft.Column(
                controls = [
                    ft.Checkbox(label=res[0]
                                ,on_change = self.checked
                                , value = True if res[1] == 'complete' else False,
                                )
                    for res in self.results if res
                ]
            )
        )
        
    def set_value(self, e):
            self.task = e.control.value
        
    def add(self, e, input_task):
        name = self.task
        status = "incomplete"
        
        if name:
            self.db_execute(query="INSERT INTO tasks VALUES(?,?)", params=[name, status])
            input_task.value = ""
            self.results = self.db_execute("SELECT * FROM tasks")
            self.update_task_list()
        
    def remove_task(self, e):
        self.db_execute('DELETE FROM tasks WHERE status = "complete"')
        self.results = self.db_execute("SELECT * FROM tasks")
        self.update_task_list()
        
    def update_task_list(self):
        tasks = self.tasks_container()
        self.page.controls.pop()
        self.page.add(tasks)
        self.page.update()
        
    def tabs_changed(self, e):
        if e.control.selected_index == 0:
            self.results = self.db_execute("SELECT * FROM tasks")
            self.view = "all"
        elif e.control.selected_index == 1:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "incomplete"')
            self.view = "incomplete"
        else:
            self.results = self.db_execute('SELECT * FROM tasks WHERE status = "complete"')
            self.view = "complete"
        
        self.update_task_list()
        
    
    def main_page(self):
        input_task = ft.TextField(hint_text = "Qual a sua tarefa?",bgcolor=ft.colors.WHITE, expand=True, on_change=self.set_value,)
        input_bar = ft.Row(
            controls=[
                input_task,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=lambda e: self.add(e, input_task)
                )
            ] 
        )
        
       
        
        tabs = ft.Tabs(
            selected_index=0,
            tab_alignment=ft.TabAlignment.CENTER,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="Todas"),
                ft.Tab(text="Pendentes"),
                ft.Tab(text="Concluídas",)   
            ]
  
        )
        
        tasks = self.tasks_container()
        remove_task = ft.FloatingActionButton(icon=ft.icons.DELETE, on_click=self.remove_task)
        self.page.add(input_bar,remove_task,tabs, tasks,)
        
ft.app(target=ToDo)  
        
