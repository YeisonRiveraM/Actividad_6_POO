import tkinter as tk
from tkinter import messagebox

CONTACT_FILE = "contacts.txt"

class CreateContact:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

        tk.Label(self.frame, text="Nombre").grid(row=0, column=0)
        tk.Label(self.frame, text="Número").grid(row=1, column=0)

        self.name = tk.Entry(self.frame)
        self.phone = tk.Entry(self.frame)
        self.name.grid(row=0, column=1)
        self.phone.grid(row=1, column=1)

        tk.Button(self.frame, text="Guardar", command=self.save).grid(row=2, columnspan=2)

    def save(self):
        nombre = self.name.get()
        numero = self.phone.get()
        nuevo_contacto = f"{nombre},{numero}"

        try:
            with open(CONTACT_FILE, "r") as file:
                contactos = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            contactos = []

        if nuevo_contacto in contactos:
            messagebox.showwarning("Duplicado", "El contacto ya existe")
        else:
            with open(CONTACT_FILE, "a") as file:
                file.write(nuevo_contacto + "\n")
            messagebox.showinfo("Guardado", "Contacto guardado exitosamente")


class ReadContacts:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

        tk.Label(self.frame, text="Nombre a buscar").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        tk.Button(self.frame, text="Buscar", command=self.search).grid(row=1, columnspan=2)

        self.result_label = tk.Label(self.frame, text="", fg="blue")
        self.result_label.grid(row=2, columnspan=2)

    def search(self):
        name_to_find = self.name_entry.get()
        found = False

        try:
            with open(CONTACT_FILE, "r") as file:
                for line in file:
                    nombre, numero = line.strip().split(",")
                    if nombre == name_to_find:
                        self.result_label.config(text=f"Número: {numero}")
                        found = True
                        break

            if not found:
                self.result_label.config(text="Contacto no encontrado", fg="red")

        except FileNotFoundError:
            self.result_label.config(text="No hay contactos aún", fg="red")


class UpdateContact:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

        tk.Label(self.frame, text="Nombre a actualizar").grid(row=0, column=0)
        tk.Label(self.frame, text="Nuevo número").grid(row=1, column=0)

        self.old_name = tk.Entry(self.frame)
        self.new_phone = tk.Entry(self.frame)
        self.old_name.grid(row=0, column=1)
        self.new_phone.grid(row=1, column=1)

        tk.Button(self.frame, text="Actualizar", command=self.update).grid(row=2, columnspan=2)

    def update(self):
        name = self.old_name.get()
        phone = self.new_phone.get()
        updated = False

        try:
            with open(CONTACT_FILE, "r") as file:
                lines = file.readlines()

            with open(CONTACT_FILE, "w") as file:
                for line in lines:
                    nombre, telefono = line.strip().split(",")
                    if nombre == name:
                        file.write(f"{nombre},{phone}\n")
                        updated = True
                    else:
                        file.write(line)

            if updated:
                messagebox.showinfo("Actualizado", "Contacto actualizado")
            else:
                messagebox.showwarning("No encontrado", "No se encontró el contacto")
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de contactos no encontrado")

class DeleteContact:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

        tk.Label(self.frame, text="Nombre a eliminar").grid(row=0, column=0)
        self.name = tk.Entry(self.frame)
        self.name.grid(row=0, column=1)

        tk.Button(self.frame, text="Eliminar", command=self.delete).grid(row=1, columnspan=2)

    def delete(self):
        name = self.name.get()
        deleted = False

        try:
            with open(CONTACT_FILE, "r") as file:
                lines = file.readlines()

            with open(CONTACT_FILE, "w") as file:
                for line in lines:
                    if not line.startswith(name + ","):
                        file.write(line)
                    else:
                        deleted = True

            if deleted:
                messagebox.showinfo("Eliminado", "Contacto eliminado")
            else:
                messagebox.showwarning("No encontrado", "Contacto no encontrado")
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de contactos no encontrado")

# Ventana principal
def main():
    root = tk.Tk()
    root.title("Agenda de Contactos")

    tk.Label(root, text="Seleccione una operación CRUD").pack()

    tk.Button(root, text="Crear", command=lambda: show_frame(CreateContact)).pack(fill="x")
    tk.Button(root, text="Leer", command=lambda: show_frame(ReadContacts)).pack(fill="x")
    tk.Button(root, text="Actualizar", command=lambda: show_frame(UpdateContact)).pack(fill="x")
    tk.Button(root, text="Eliminar", command=lambda: show_frame(DeleteContact)).pack(fill="x")

    def show_frame(frame_class):
        for widget in root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        frame_class(root)

    root.mainloop()

if __name__ == "__main__":
    main()
