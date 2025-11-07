import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from bson import ObjectId


client = MongoClient("mongodb://localhost:27017/")
db = client["Projeto4bim_Halloween"]
convidados = db["convites_halloween"]

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

def encrypt(text):
    return public_key.encrypt(
        text.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None)
    )

def decrypt(ciphertext):
    try:
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        ).decode()
    except Exception:
        return "🔒 Dado protegido"

def tela_charada():
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#1c1c1c")

    frame_central = tk.Frame(root, bg="#1c1c1c")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_central, text="🎃 Convites secretos de Halloween 🎃",
             bg="#1c1c1c", fg="orange", font=("Arial Black", 22, "bold")).pack(pady=(0, 20))

    tk.Label(frame_central, text="Adivinhe a charada para acessar os dados confidenciais...",
             bg="#1c1c1c", fg="orange", font=("Poppins", 14, "bold")).pack(pady=(0, 30))

    pergaminho = tk.Frame(frame_central, bg="#f5deb3", bd=5, relief="ridge")
    pergaminho.pack(pady=20, padx=10)

    tk.Label(pergaminho,
            text="“Vim da terra, fico laranja e brilho por uma noite;\nesculpem meu rosto para que eu guie o caminho.”",
            bg="#f5deb3", fg="#3b2f2f",
            font=("Segoe Script", 14, "italic", "bold"),
            wraplength=600, justify="center").pack(padx=20, pady=20)

    resposta = tk.Entry(frame_central, font=("Arial", 14), width=30, justify="center")
    resposta.pack(pady=10)

    def verificar_resposta():
        if resposta.get().strip().lower() in ["abóbora", "abobora"]:
            tela_lista()
        else:
            messagebox.showerror("Errado!", "👻 Tente novamente...")

    tk.Button(frame_central, text="Responder", command=verificar_resposta,
              bg="orange", fg="black", font=("Arial", 12, "bold"),
              width=15).pack(pady=15)

def tela_lista():
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#252525")

    tk.Label(root, text="🎃 Lista Confidencial de Convidados 🎃",
             bg="#252525", fg="orange", font=("Arial Black", 22, "bold")).pack(pady=15)

    frame_filtro = tk.Frame(root, bg="#252525")
    frame_filtro.pack(pady=10)

    tk.Label(frame_filtro, text="Buscar:", bg="#252525", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
    entrada_busca = tk.Entry(frame_filtro, font=("Arial", 12), width=20)
    entrada_busca.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtro, text="RSVP:", bg="#252525", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=5)
    filtro_rsvp = ttk.Combobox(frame_filtro, values=["", "SIM", "NÃO", "TALVEZ"], width=10, font=("Arial", 11))
    filtro_rsvp.grid(row=0, column=3, padx=5)

    tk.Button(frame_filtro, text="Filtrar", command=lambda: carregar_dados(),
              bg="orange", fg="black", font=("Arial", 11, "bold"), width=12).grid(row=0, column=4, padx=8)

    tk.Button(frame_filtro, text="Listar Todos",
              command=lambda: (entrada_busca.delete(0, tk.END), filtro_rsvp.set(""), carregar_dados()),
              bg="orange", fg="black", font=("Arial", 11, "bold"), width=12).grid(row=0, column=5, padx=8)


    style = ttk.Style()
    style.configure("Treeview",
                    background="#2f2f2f",
                    foreground="white",
                    rowheight=28,
                    fieldbackground="#2f2f2f",
                    font=("Arial", 12))
    style.configure("Treeview.Heading",
                    background="#ff8c00",
                    foreground="black",
                    font=("Arial Black", 13, "bold"))
    style.map("Treeview", background=[("selected", "#ffa500")])

    tree = ttk.Treeview(root, columns=("Nome", "Email", "Telefone", "RSVP"), show="headings")
    for col in ("Nome", "Email", "Telefone", "RSVP"):
        tree.heading(col, text=col)
    tree.pack(pady=10, fill="both", expand=True)
    tree.tag_configure("linha", background="#303030")

    frame_add = tk.Frame(root, bg="#252525", bd=2, relief="groove", padx=15, pady=15)
    frame_add.pack(pady=15)

    def criar_label(entry_text, row):
        tk.Label(frame_add, text=entry_text, bg="#252525", fg="white", font=("Arial", 12)).grid(row=row, column=0, sticky="e", pady=5, padx=10)

    criar_label("Nome:", 0)
    nome_entry = tk.Entry(frame_add, font=("Arial", 12), width=30)
    nome_entry.grid(row=0, column=1, pady=5)

    criar_label("Email:", 1)
    email_entry = tk.Entry(frame_add, font=("Arial", 12), width=30)
    email_entry.grid(row=1, column=1, pady=5)

    criar_label("Telefone:", 2)
    phone_entry = tk.Entry(frame_add, font=("Arial", 12), width=30)
    phone_entry.grid(row=2, column=1, pady=5)

    criar_label("RSVP:", 3)
    rsvp_entry = ttk.Combobox(frame_add, values=["SIM", "NÃO", "TALVEZ"], width=28, font=("Arial", 12))
    rsvp_entry.grid(row=3, column=1, pady=5)

    selected_id = None  

    def carregar_dados():
        tree.delete(*tree.get_children())
        query = {}
        if entrada_busca.get():
            query["name"] = {"$regex": entrada_busca.get(), "$options": "i"}
        if filtro_rsvp.get():
            query["rsvp"] = filtro_rsvp.get()

        for c in convidados.find(query):
            email = decrypt(c["email"]) if isinstance(c["email"], (bytes, bytearray)) else c.get("email", "")
            phone = decrypt(c["phone"]) if isinstance(c["phone"], (bytes, bytearray)) else c.get("phone", "")
            tree.insert("", "end", iid=str(c["_id"]),
                        values=(c.get("name", ""), email, phone, c.get("rsvp", "")),
                        tags=("linha",))

    def limpar_campos():
        nome_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        rsvp_entry.set("")
        nonlocal selected_id
        selected_id = None

    def adicionar_convidado():
        nome = nome_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        rsvp = rsvp_entry.get().strip()

        if not nome or not email or not phone or not rsvp:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        convidados.insert_one({
            "name": nome,
            "email": encrypt(email),
            "phone": encrypt(phone),
            "rsvp": rsvp
        })
        messagebox.showinfo("Sucesso", f"🎉 {nome} adicionado com sucesso!")
        carregar_dados()
        limpar_campos()

    def ao_clicar_duas_vezes(event):
        nonlocal selected_id
        item = tree.selection()
        if not item:
            return
        selected_id = item[0]
        valores = tree.item(selected_id, "values")
        nome_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        rsvp_entry.set("")
        nome_entry.insert(0, valores[0])
        email_entry.insert(0, valores[1])
        phone_entry.insert(0, valores[2])
        rsvp_entry.set(valores[3])

    def atualizar_convidado():
        if not selected_id:
            messagebox.showwarning("Aviso", "Selecione um convidado para atualizar.")
            return

        nome = nome_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        rsvp = rsvp_entry.get().strip()

        update_data = {}
        if nome:
            update_data["name"] = nome
        if email:
            if email != "🔒 Dado protegido":update_data["email"] = encrypt(email)
        if phone:
            if phone != "🔒 Dado protegido":update_data["phone"] = encrypt(phone)
        if rsvp:
            update_data["rsvp"] = rsvp

        if not update_data:
            messagebox.showwarning("Aviso", "Nenhuma informação nova foi inserida!")
            return

        convidados.update_one({"_id": ObjectId(selected_id)}, {"$set": update_data})

        messagebox.showinfo("Sucesso", "🎃 Dados atualizados com sucesso!")
        carregar_dados()


    def deletar_convidado():
        if not selected_id:
            messagebox.showwarning("Atenção", "Selecione um convidado na lista para deletar.")
            return
        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este convidado?")
        if confirm:
            convidados.delete_one({"_id": ObjectId(selected_id)})

            messagebox.showinfo("Removido", "💀 Convidado excluído com sucesso!")
            carregar_dados()
            limpar_campos()

    # ====== BOTÕES ======
    botoes_frame = tk.Frame(root, bg="#252525")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Adicionar", command=adicionar_convidado,
              bg="orange", fg="black", font=("Arial", 12, "bold"), width=14).grid(row=0, column=0, padx=10)
    tk.Button(botoes_frame, text="Atualizar", command=atualizar_convidado,
              bg="orange", fg="black", font=("Arial", 12, "bold"), width=14).grid(row=0, column=1, padx=10)
    tk.Button(botoes_frame, text="Deletar", command=deletar_convidado,
              bg="red", fg="white", font=("Arial", 12, "bold"), width=14).grid(row=0, column=2, padx=10)
    tk.Button(botoes_frame, text="Limpar Campos", command=limpar_campos,
              bg="#555", fg="white", font=("Arial", 12, "bold"), width=16).grid(row=0, column=3, padx=10)

    tree.bind("<Double-1>", ao_clicar_duas_vezes)
    carregar_dados()

# ===================== MAIN =====================
root = tk.Tk()
root.title("🎃 Halloween Party – Acesso Restrito 🎃")
largura, altura = 800, 650
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
posx = (largura_tela // 2) - (largura // 2)
posy = (altura_tela // 2) - (altura // 2)
root.geometry(f"{largura}x{altura}+{posx}+{posy}")
root.configure(bg="#1c1c1c")
tela_charada()
root.mainloop()
