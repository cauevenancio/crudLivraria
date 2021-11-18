from os import truncate
import mysql.connector 
from mysql.connector import Error
from tkinter import *
from tkinter import messagebox

class Livraria():

    def __init__(self):

        self.controle = 0

        self.conecta()
        self.cursor = self.conexao.cursor()


        if self.conexao != 1:
                self.usaDb()
                self.registraBd()

        else:
            print("Não conseguimos conectar ao Banco de dados. Por favor, revise sua conexão.\n Programa fechando...")
            exit()

        self.editora()

    def editora(self):
        self.telaViewEditora = Tk()
        self.controle = 0
        self.analise = 0
        self.telaViewEditora.geometry("1000x600")
        self.telaViewEditora.resizable(False, False)
        self.telaViewEditora.title('CRDU Livraria')
        self.telaViewEditora['bg'] = 'gray'

        seta = PhotoImage(file = '.\\imagens\\seta.png')
        self.botao(self.telaViewEditora, 'Arial 12', None, seta, 'gray', 'gray', 0.02, 0.03, 0.1, 0.11, None)

        self.label(self.telaViewEditora, "Roboto 25", 'Editoras Cadastradas', None, 'gray', None, 0.1, 0.05, 0.8, 0.05)

        self.listaEditora = Listbox(self.telaViewEditora, bg="gray", fg="black", font= ("Roboto", 15, 'bold'), justify = "center", selectbackground = '#FFFFFF', selectforeground = '#3ad1cb', borderwidth= 0, bd = 0)
        self.listaEditora.place(relx=0.03, rely=0.15, relwidth=0.91, relheight=0.65)

        scrollbar = Scrollbar(self.telaViewEditora)
        scrollbar.place(relx=0.93, rely=0.15, relwidth=0.035, relheight=0.65)

        self.listaEditora.config(yscrollcommand = scrollbar.set) 
        scrollbar.config(command = self.listaEditora.yview)

        self.botao(self.telaViewEditora, 'Roboto 17', "Adicionar", None, 'green', 'green', 0.425, 0.85, 0.15, 0.05, lambda: self.destruir(self.telaViewEditora, self.cadastroEditora))

        self.listaEditora.bind_all("<<ListboxSelect>>", self.editoraEscolhida)
        
        self.scannerBd(self.listaEditora, 'Editora', 'Codigo', 'Nome')

        self.telaViewEditora.mainloop()

    def cadastroEditora(self):

        self.telaAddEditora = Tk()
        self.telaAddEditora.geometry("1000x600")
        self.telaAddEditora.resizable(False, False)
        self.telaAddEditora.title('CRDU Livraria')
        self.telaAddEditora['bg'] = 'gray'
        

        seta = PhotoImage(file = '.\\imagens\\seta.png')
        self.botao(self.telaAddEditora, 'Arial 12', None, seta, 'gray', 'gray', 0.02, 0.03, 0.1, 0.1, lambda: self.destruir(self.telaAddEditora, self.editora))

        self.label(self.telaAddEditora, "Roboto 17", 'Nome', None, 'gray', None, 0.05, 0.2, 0.1, 0.1)

        self.nomeEditora = Entry(self.telaAddEditora, font = 'Roboto 17', background = 'white')
        self.nomeEditora.place(relx = 0.17, rely = 0.215, relheight = 0.07, relwidth = 0.8)

        self.label(self.telaAddEditora, "Roboto 17", 'Endereço', None, 'gray', None, 0.05, 0.35, 0.1, 0.1)

        self.enderecoEditora = Entry(self.telaAddEditora, font = 'Roboto 17', background = 'white')
        self.enderecoEditora.place(relx = 0.17, rely = 0.365, relheight = 0.07, relwidth = 0.8)

        self.label(self.telaAddEditora, "Roboto 17", 'Telefone', None, 'gray', None, 0.05, 0.5, 0.1, 0.1)

        self.telefoneEditora = Entry(self.telaAddEditora, font = 'Roboto 17', background = 'white')
        self.telefoneEditora.place(relx = 0.17, rely = 0.515, relheight = 0.07, relwidth = 0.8)

        self.label(self.telaAddEditora, "Roboto 17", 'Gerente', None, 'gray', None, 0.05, 0.65, 0.1, 0.1)

        self.gerenteEditora = Entry(self.telaAddEditora, font = 'Roboto 17', background = 'white')
        self.gerenteEditora.place(relx = 0.17, rely = 0.665, relheight = 0.07, relwidth = 0.8)

        if self.controle == 0:
            
            self.label(self.telaAddEditora, "Roboto 25", 'Cadastrar Editora', None, 'gray', None, 0.1, 0.05, 0.8, 0.05)

            self.botao(self.telaAddEditora, 'Roboto 17', "Adicionar", None, 'green', 'green', 0.425, 0.85, 0.15, 0.05, lambda: self.addBanco('Editora', 'Nome', self.nomeEditora, 'Endereco', self.enderecoEditora, 'Telefone', self.telefoneEditora, 'Gerente', self.gerenteEditora))

        else:

            self.label(self.telaAddEditora, "Roboto 25", 'Atualizar Editora', None, 'gray', None, 0.1, 0.05, 0.8, 0.05)

            self.botao(self.telaAddEditora, 'Roboto 17', "Atualizar", None, 'green', 'green', 0.55, 0.85, 0.15, 0.05, self.atualizaEditora)

            self.botao(self.telaAddEditora, 'Roboto 17', "Remover", None, 'red', 'red', 0.3, 0.85, 0.15, 0.05, self.removerEditora)

        if self.analise == 1:
            self.cursor.execute(f"SELECT nome FROM Editora WHERE codigo = {self.codigo}")

            for i in self.cursor:
                nome = i[0]

            self.nomeEditora.insert(0, nome)

            self.cursor.execute(f"SELECT telefone FROM Editora WHERE codigo = {self.codigo}")

            for i in self.cursor:
                telefone = i[0]

            self.telefoneEditora.insert(0, telefone)

            self.cursor.execute(f"SELECT endereco FROM Editora WHERE codigo = {self.codigo}")

            for i in self.cursor:
                endereco = i[0]

            self.enderecoEditora.insert(0, endereco)

            self.cursor.execute(f"SELECT gerente FROM Editora WHERE codigo = {self.codigo}")

            for i in self.cursor:
                gerente = i[0]

            self.gerenteEditora.insert(0, gerente)

            self.analise = 0

        self.telaAddEditora.mainloop()

    def esconder(self, atual, nova):
        atual.withdraw()
        nova()

    def aparecer(self, antiga, nova):
        antiga.destroy()
        nova.update()
        nova.deiconify()
  
    def destruir(self, atual, nova):
        atual.destroy()
        nova()

    def sair(self, destruir):
        destruir.destroy()    

    def conecta(self):
        try:
            self.conexao = mysql.connector.connect(user = "root",
									  	 host = "127.0.0.1")                                       
            return self.conexao
        
        except:
            print("Não foi possível conectar ao SGBD.")
            return 1

    def usaDb(self):
        '''
            Implementar o uso do BD como argumento.
        '''
        try:
            self.cursor.execute("CREATE DATABASE Livraria;")
            self.cursor.execute("USE Livraria;")
            print("Livraria Database criado!")
        except:
            self.cursor.execute("USE Livraria;")
            print("Livraria Database selecionado!")

    def registraBd(self):

        try:
            self.cursor.execute('''CREATE TABLE Editora (
                                Codigo int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                Nome varchar(20) NOT NULL,
                                Endereco varchar(50) NOT NULL,
                                Telefone varchar(11) NOT NULL,
                                Gerente varchar(20) NOT NULL
                                );''')

            self.cursor.execute('''
                                CREATE TABLE Cliente (
                                Codigo int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                Nome varchar(20) NOT NULL,
                                Telefone varchar(11) NOT NULL,
                                Endereco varchar(50) NOT NULL
                                );''')

            self.cursor.execute('''
                                CREATE TABLE Livro (
                                ISBN varchar(20) NOT NULL PRIMARY KEY,
                                Nome varchar(20) NOT NULL,
                                Assunto varchar(10) NOT NULL,
                                Qtd int NOT NULL,
                                Autor varchar(20) NOT NULL,
                                CodigoEditora int,
                                FOREIGN KEY (CodigoEditora) REFERENCES Editora(Codigo)
                                );''')

            self.cursor.execute('''
                                CREATE TABLE CompraLivro (
                                Codigo int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                DataCompra date,
                                CodigoCliente int,
                                ISBN varchar(20),
                                FOREIGN KEY (CodigoCliente) REFERENCES Cliente(Codigo),
                                FOREIGN KEY (ISBN) REFERENCES Livro(ISBN)
                                );''')

            self.cursor.execute('''
                                CREATE TABLE Fisica (
                                CPF varchar(11) NOT NULL PRIMARY KEY,
                                CodigoCliente int,
                                FOREIGN KEY (CodigoCliente) REFERENCES Cliente(Codigo)
                                );''')
        
            self.cursor.execute('''
                                CREATE TABLE Juridica (
                                CNPJ varchar(14) NOT NULL PRIMARY KEY,
                                CodigoCliente int,
                                FOREIGN KEY (CodigoCliente) REFERENCES Cliente(Codigo)
                                );''')
        
            print("Tabela criada com sucesso!")

        except:
            print("Tabelas já foi criada!")

    def scannerBd(self, lista, tabela, identificador, visorLista):

        self.cursor.execute(f"SELECT {identificador} FROM {tabela} ORDER BY {identificador}")
            
        listaCodigo = []
        for i in self.cursor:
            listaCodigo.append(i[0])

        self.cursor.execute(f"SELECT {visorLista} FROM {tabela} ORDER BY {identificador}")
            
        listaIdent = []
        for i in self.cursor:
            listaIdent.append(i[0])
        
        controle = 0

        for i in listaCodigo:

            codig = listaCodigo[controle]
            ident = listaIdent[controle]

            valor = str(f'{codig}-{ident}')

            lista.insert(END, valor)
            controle += 1

    def addBanco(self, tabela, valorum, listaum, valordois, listadois, valortres, listatres, valorquatro = None, listaquatro = None, valorcinco = None, listacinco = None, valorseis = None, listaseis = None, pessoa = None, Documento = None, numerodoc = None):

        tipoPessoa = pessoa
        tipoDocumento = Documento
        cpfnj = numerodoc


        lista1 = listaum.get()
        lista2 = listadois.get()
        lista3 = listatres.get()
        
        valor1= valorum
        valor2= valordois
        valor3= valortres
        valor4= valorquatro
        valor5= valorcinco
        valor6= valorseis

        try:

            if valor6 != None:
                
                lista4 = listaquatro.get()
                lista5 = listacinco.get()
                lista6 = listaseis.get()

                self.cursor.execute(f"INSERT INTO {tabela}({valor1}, {valor2}, {valor3}, {valor4}, {valor5}, {valor6}) VALUES ('{lista1}', '{lista2}', '{lista3}', '{lista4}', '{lista5}', '{lista6}');")
                self.conexao.commit()

                listaseis.delete(0,END)
                listacinco.delete(0,END)
                listaquatro.delete(0,END)
                listatres.delete(0,END)
                listadois.delete(0,END)
                listaum.delete(0,END)

            elif valor6 == None and valor4 != None:

                lista4 = listaquatro.get()

                self.cursor.execute(f'INSERT INTO {tabela}({valor1}, {valor2}, {valor3}, {valor4}) VALUES ("{lista1}", "{lista2}", "{lista3}", "{lista4}");')
                self.conexao.commit()

                listaquatro.delete(0,END)
                listatres.delete(0,END)
                listadois.delete(0,END)
                listaum.delete(0,END)

            elif valor4 == None:

                self.cursor.execute(f"INSERT INTO {tabela}({valor1}, {valor2}, {valor3}) VALUES ('{lista1}', '{lista2}', '{lista3}');")
                self.conexao.commit()

                listatres.delete(0,END)
                listadois.delete(0,END)
                listaum.delete(0,END)

            if tipoPessoa != None:

                self.cursor.execute(f"SELECT codigo FROM cliente WHERE nome == '{valor1}'")
            
                lista = []
                for i in self.cursor:
                    lista.append(i[0])

                codigo = lista[0]

                self.cursor.execute(f"INSERT INTO {tipoPessoa}({tipoDocumento}, codigo) VALUES ('{cpfnj}', '{codigo}');")
                self.conexao.commit()

                numerodoc.delete(0,END)
                listatres.delete(0,END)
                listadois.delete(0,END)
                listaum.delete(0,END)

            messagebox.showinfo(title= 'Sucesso!', message= 'Informações adicionadas.')
            

        
        except Error as er:

            messagebox.showerror(title = 'Erro!', message = 'Não foi possível adicionar')

            print(er)

    def editoraEscolhida(self,event = None):

        aux = self.listaEditora.curselection()
        codigo = self.listaEditora.get(aux[0])
        codigo = codigo.split('-')

        self.codigo = codigo[0]

        self.controle = 1
        self.analise = 1

        self.destruir(self.telaViewEditora, self.cadastroEditora)
       
    def removerEditora(self):

        try:

            self.cursor.execute(f"DELETE FROM editora WHERE codigo = '{self.codigo}'")
            self.conexao.commit()

            self.telaAddEditora.update()
            messagebox.showinfo(title= 'Sucesso!', message= 'Informações apagadas.')
            self.destruir(self.telaAddEditora, self.editora)
            
        except:

            messagebox.showerror(title = 'Erro!', message = 'Não foi possível apagar')

    def atualizaEditora(self):

        try:

            nome = self.nomeEditora.get()
            telefone = self.telefoneEditora.get()
            gerente = self.gerenteEditora.get()
            endereco = self.enderecoEditora.get()

            self.cursor.execute(f"UPDATE editora SET nome = '{nome}' WHERE codigo = '{self.codigo}'")
            self.conexao.commit()

            self.cursor.execute(f"UPDATE editora SET gerente = '{gerente}' WHERE codigo = '{self.codigo}'")
            self.conexao.commit()

            self.cursor.execute(f"UPDATE editora SET telefone = '{telefone}' WHERE codigo = '{self.codigo}'")
            self.conexao.commit()

            self.cursor.execute(f"UPDATE editora SET endereco = '{endereco}' WHERE codigo = '{self.codigo}'")
            self.conexao.commit()

            self.telaAddEditora.update()
            
            messagebox.showinfo(title= 'Sucesso!', message= 'Informações atualizadas.')

            self.destruir(self.telaAddEditora, self.editora)

        except:

            messagebox.showerror(title = 'Erro!', message = 'Não foi possível atualizar')

    def botao(self, janela, fonte, texto, image, bg, ab, x, y, width, height, command, cursor = None):
        btn = Button(janela)
        btn["font"] = fonte
        btn["text"] = texto
        btn["image"] = image
        btn["bg"] = bg  
        btn["command"] = command
        btn['activebackground'] = ab
        btn["bd"] = 0
        btn["relief"] = GROOVE
        btn['cursor'] = cursor
        btn.place(relx=x, rely=y, relwidth=width, relheight=height)

    def label(self, janela, fonte, text, image, bg, fg, x, y, width, height):
        lbl = Label(janela)
        lbl["font"] = fonte
        lbl["text"] = text
        lbl['image'] = image
        lbl['fg'] = fg
        lbl["bg"] = bg
        lbl.place(relx=x, rely=y, relwidth=width, relheight=height)


if __name__ == "__main__":
    Livraria()
