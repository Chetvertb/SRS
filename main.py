import tkinter as tk
from tkinter import messagebox
import utils
import srs_logic
from datetime import date, timedelta

class SRSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SRS - Повторение карточек")

        # Загрузка карточек
        self.cards = utils.load_cards()

        # Кнопки
        self.repeat_button = tk.Button(self.root, text="Повторить карточки", command=self.repeat_cards)
        self.add_button = tk.Button(self.root, text="Добавить карточку", command=self.add_card)
        self.look_button = tk.Button(self.root, text="Посмотреть все карточки", command=self.look_cards)

        # Размещение кнопок
        self.repeat_button.pack(padx=10)
        self.add_button.pack(padx=10)
        self.look_button.pack(padx=10)

    def repeat_cards(self):
        if not self.cards:
            messagebox.showinfo("Информация", "Карточки не добавлены.")
            return
        
        today = date.today()
        def get_next_card():
            for card in self.cards:
                d = date.fromisoformat(card['next_date'])
                if d <= today:
                    question = card["question"]
                    answer = card["answer"]
                    yield self.show_question_answer(question, answer, card)

        def show_next_card():
            result = next(self.card_generator, "cards ended")
            if result == "cards ended":
                messagebox.showinfo("Информация", "Нет карточек для повторения.")
            else:
                return result
            
        self.next_button = tk.Button(self.root, text="Следующая", command=show_next_card)
        self.next_button.pack(pady=10)

        
        self.card_generator = get_next_card()
        self.show_next_card()

    def mark_card(self,answer,  mark_entry, card, answer_label):
            mark = int(mark_entry.get())
            if 2 <= mark <= 5:
                interval, ratio = srs_logic.size_ratio(mark, card['interval'], card['ratio'])
                card['interval'] = interval
                card['ratio'] = ratio
                card['next_date'] = str(date.today() + timedelta(days=card['interval']))
                utils.save_cards(self.cards)
                answer_label.config(text=f"Ответ: {answer}")

            else:
                messagebox.showerror("Ошибка", "Введите оценку от 2 до 5.")       
            

    def show_question_answer(self, question, answer, card):
        

        question_label = tk.Label(self.root, text=f"Вопрос: {question}")
        question_label.pack()

        answer_label = tk.Label(self.root, text="Ответ: Не показан")
        answer_label.pack()

        mark_label = tk.Label(self.root, text="Оцените от 2 до 5")
        mark_label.pack()

        mark_entry = tk.Entry(self.root)
        mark_entry.pack()

        mark_button = tk.Button(self.root, text="Оценить", command=lambda: self.mark_card(answer, mark_entry, card, answer_label))
        mark_button.pack()

    def add_card(self):
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
                question_label.destroy()
                answer_label.destroy()
                question_entry.destroy()
                answer_entry.destroy()
                save_button.destroy()
            else:
                messagebox.showerror("Ошибка", "Заполните все поля.")

        question_label = tk.Label(self.root, text="Введите вопрос:")
        question_label.pack()

        question_entry = tk.Entry(self.root)
        question_entry.pack()

        answer_label = tk.Label(self.root, text="Введите ответ:")
        answer_label.pack()

        answer_entry = tk.Entry(self.root)
        answer_entry.pack()

        save_button = tk.Button(self.root, text="Сохранить карточку", command=save_card)
        save_button.pack()


    def look_cards(self):
        if not self.cards:
            messagebox.showinfo("Информация", "Карточки не добавлены.")
            return

        for card in self.cards:
            question = card["question"]
            answer = card["answer"]
            self.show_question_answer(question, answer, card)

if __name__ == "__main__":
    root = tk.Tk()
    app = SRSApp(root)
    root.mainloop()