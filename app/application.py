import tkinter as tk
from tkinter import *
from functions.reading_functions import ReadingFunctions
from functions.embedding_functions import EmbeddingFunctions
from functions.prompting_functions import PromptingFunctions
from functions.indexing_functions import IndexingFunctions
import globals

rf = ReadingFunctions()
ef = EmbeddingFunctions()
pf = PromptingFunctions()
indf = IndexingFunctions()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Base window
        self.geometry("800x700")
        self.title("RagBot")
        self.resizable(False, False)
        self.configure(bg="#D3D3D3")

        # Button: Select PDF File
        self.button_select_pdf = tk.Button(
            self,
            text="Select PDF",
            command=lambda: [
                rf.select_pdf_file(label=self.label_selected_pdf),
                rf.read_pdf(pdf_path=globals.pdf_path),
            ],
        )
        self.button_select_pdf.place(x=10, y=50, width=100, height=30)

        # Button: Create Index
        self.button_create_index = tk.Button(
            self,
            text="Create Index",
            command=lambda: [
                ef.create_vector_embeddings_from_pages(),
                indf.create_index(),
            ],
        )
        self.button_create_index.place(x=120, y=50, width=100, height=30)

        # Button: Load Index
        self.button_load_index = tk.Button(
            self,
            text="Load Index",
            command=lambda: [
                indf.load_index(),
            ],
        )
        self.button_load_index.place(x=230, y=50, width=100, height=30)

        # Button: Search
        self.button_search = tk.Button(
            self,
            text="Search",
            command=lambda: [self._update_query_vector(), self.display_response()],
        )
        self.button_search.place(x=10, y=660, width=250, height=30)

        # Button: Copy Answer
        self.button_copy_answer = tk.Button(self, text="Copy Answer", command=None)
        self.button_copy_answer.place(x=365, y=660, width=250, height=30)

        # Labels
        self.label_welcome = Label(
            self, text="Welcome to RAGBot! Your personal PDF assistant!"
        )
        self.label_welcome.config(font=("Arial", 12))
        self.label_welcome.place(x=10, y=10, width=605, height=30)

        self.label_selected_pdf = Label(self, text="Selected PDF: None Selected")
        self.label_selected_pdf.config(font=("Arial", 12), anchor="w")
        self.label_selected_pdf.place(x=10, y=90, width=605, height=30)

        self.label_status = Label(self, text="Status")
        self.label_status.config(font=("Arial", 12), anchor="center")
        self.label_status.place(x=10, y=130, width=605, height=30)

        self.label_chat = Label(self, text="Chat with RAGBot")
        self.label_chat.config(font=("Arial", 12))
        self.label_chat.place(x=10, y=350, width=605, height=30)

        # Status Chatbox
        self.chatbox_answer = Text(self, wrap=WORD)
        self.chatbox_answer.tag_configure("center", justify="center")
        self.chatbox_answer.insert(1.0, "Not Started")
        self.chatbox_answer.config(font=("Arial", 8), fg="black", bg="white")
        self.chatbox_answer.place(x=10, y=170, width=605, height=150)

        # Response Chatbox
        self.chatbox_answer = Text(self, wrap=WORD)
        self.chatbox_answer.tag_configure("center", justify="center")
        self.chatbox_answer.insert(1.0, "Answer will appear here")
        self.chatbox_answer.config(font=("Arial", 8), fg="black", bg="white")
        self.chatbox_answer.place(x=10, y=390, width=605, height=200)

        # Answer Chatbox
        self.chat_box_ask = Text(self, wrap=WORD)
        self.chat_box_ask.tag_configure("center", justify="center")
        self.chat_box_ask.insert(1.0, "Message RAGBot here!")
        self.chat_box_ask.config(font=("Arial", 8), fg="black", bg="white")
        self.chat_box_ask.place(x=10, y=600, width=605, height=50)

    def _take_input(self):
        input = self.chat_box_ask.get("1.0", "end-1c")
        return input

    def _update_query_vector(self):
        query = self._take_input()
        globals.query_vector = ef.create_vector_embedding_from_query(query=query)

    def _take_response(self):
        query_vector = globals.query_vector
        D, I = globals.index.search(query_vector, 5)
        return I

    def display_response(self):
        self.chatbox_answer.delete(1.0, "end")
        sentence_indexes = self._take_response()
        for i in sentence_indexes[0]:
            answer = globals.pdf_sentences.loc[i, "Sentences"]
            self.chatbox_answer.insert(1.0, f"{i}) {answer}\n\n")
