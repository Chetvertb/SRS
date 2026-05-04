import tkinter as tk
from tkinter import messagebox, ttk
import utils
import srs_logic
from datetime import date, timedelta

class SRSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SRS - Repeat cards")

        # Загрузка карточек
        self.cards = utils.load_cards()

        # Кнопки
        self.repeat_button = ttk.Button(self.root, text="Повторить карточки", command=self.repeat_cards)
        self.add_button = ttk.Button(self.root, text="Добавить карточку", command=self.add_card)
        self.look_button = ttk.Button(self.root, text="Посмотреть все карточки", command=self.look_cards)

        # Размещение кнопок
        self.repeat_button.pack(padx=10)
        self.add_button.pack(padx=10)
        self.look_button.pack(padx=10)

        self.card_generator = None 
        self.card_window = None
        self.current_card = None
        self.add_card_window = None

    def repeat_cards(self):
        if not self.cards:
            messagebox.showinfo("Information", "Cards not added")
            return
        today = date.today()
        self.card_generator = (card for card in self.cards if date.fromisoformat(card['next_date']) <= today)
        if self.card_window is None:
            self.create_repeat_window()
        self.show_next_card()

    def close_window(self, window):
        if window is self.card_window:
            self.card_generator = None
            self.current_card = None
            self.card_window.destroy()
            self.card_window = None
        else:
            self.add_card_window.destroy()
            self.add_card_window = None
        


    def create_repeat_window(self):
        self.card_window = tk.Toplevel(self.root)
        self.card_window.title('Repeat cards')
        self.card_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(self.card_window))


        self.question_label = tk.Label(self.card_window, text="", font=("Arial", 16))
        self.question_label.pack(pady=5)

        self.answer_label = tk.Label(self.card_window, text="", font=("Arial", 14))
        self.answer_label.pack(pady=5)

        self.mark_entry = tk.Entry(self.card_window)
        self.mark_entry.pack(pady=5)

        self.mark_button = tk.Button(self.card_window, text="Оценить", command=self.mark_current_card)
        self.mark_button.pack(pady=5)

        self.next_button = tk.Button(self.card_window, text="Следующая", command=self.show_next_card)
        self.next_button.pack(pady=5)

    def show_next_card(self):
        self.current_card = next(self.card_generator, None)

        if self.current_card is None:
            self.question_label.config(text="")
            self.answer_label.config(text="")
            self.mark_entry.delete(0, tk.END)
            self.card_window.destroy()
            self.card_window = None
            self.card_generator = None
            messagebox.showinfo("Информация", "Нет карточек для повторения.")
            return
        
        self.question_label.config(
            text=f"Вопрос: {self.current_card['question']}"
        )
        self.answer_label.config(text="Ответ: не показан")
        self.mark_entry.delete(0, tk.END)

    def mark_current_card(self):
        if self.current_card is None:
            messagebox.showinfo("Информация", "Сначала выберите карточку.")
            return

        value = self.mark_entry.get()

        if not value.isdigit():
            messagebox.showerror("Ошибка", "Введите число от 2 до 5.")
            return

        mark = int(value)
        if not 2 <= mark <= 5:
            messagebox.showerror("Ошибка", "Введите оценку от 2 до 5.")
            return

        interval, ratio = srs_logic.size_ratio(
            mark,
            self.current_card["interval"],
            self.current_card["ratio"]
        )

        self.current_card["interval"] = interval
        self.current_card["ratio"] = ratio
        self.current_card["next_date"] = str(date.today() + timedelta(days=interval))

        utils.save_cards(self.cards)

        self.answer_label.config(text=f"Ответ: {self.current_card['answer']}")      

    def add_card(self):
        if self.add_card_window is None:
            self.add_card_window = tk.Toplevel(self.root)
            self.add_card_window.title("Add card")
            self.add_card_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(self.add_card_window))


            def save_card():
                question = question_entry.get()
                answer = answer_entry.get()
                if question and answer:
                    card = {
                        "question": question,
                        "answer": answer,
                        "interval": 1,
                        "next_date": str(date.today() + timedelta(days=1)),
                        "ratio": 2.5
                    }
                    self.cards.append(card)
                    utils.save_cards(self.cards)
                    messagebox.showinfo("Успех", "Карточка добавлена!")
                    self.add_card_window.destroy()
                    self.add_card_window = None
                else:
                    messagebox.showerror("Ошибка", "Заполните все поля.")

            question_label = ttk.Label(self.add_card_window, text="Введите вопрос:")
            question_label.pack()

            question_entry = ttk.Entry(self.add_card_window)
            question_entry.pack()

            answer_label = tk.Label(self.add_card_window, text="Введите ответ:")
            answer_label.pack()

            answer_entry = tk.Entry(self.add_card_window)
            answer_entry.pack()

            save_button = ttk.Button(self.add_card_window, text="Сохранить карточку", command=save_card)
            save_button.pack()


    def look_cards(self):
        if not self.cards:
            messagebox.showinfo("Информация", "Карточки не добавлены.")
            return
        
        self.card_generator = (card for card in self.cards)
        if self.card_window is None:
            self.create_repeat_window()
        self.show_next_card()


if __name__ == "__main__":
    root = tk.Tk()
    app = SRSApp(root)
    root.mainloop()

