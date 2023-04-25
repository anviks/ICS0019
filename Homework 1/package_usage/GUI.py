from square_anviks import calculator
import tkinter
from decimal import *


def open_window():
    def get_result():
        try:
            a = Decimal(num1.get())
            b = Decimal(num2.get())
            result = calculator.square_of_sum(a, b)
            if result == result // 1:
                result = int(result)
        except (ValueError, DecimalException):
            result = "Please enter valid numbers."
        answer.configure(text=result)

    window = tkinter.Tk()
    window.title("Calculator")
    window.geometry("500x140")
    window.minsize(500, 140)
    window.configure(bg="#FFF1DE")

    open_bracket = tkinter.Label(window, text="(", font=("Arial", 15), bg="#FFF1DE")
    open_bracket.grid(row=0, column=0, padx=(20, 0), pady=(16, 10), sticky="nsew")

    plus = tkinter.Label(window, text="+", font=("Arial", 15), bg="#FFF1DE")
    plus.grid(row=0, column=2, pady=(16, 10), sticky="ew")

    close_bracket = tkinter.Label(window, text=") ²  =", font=("Arial", 15), bg="#FFF1DE")
    close_bracket.grid(row=0, column=4, pady=(16, 10), sticky="nsew")

    answer = tkinter.Label(window, text="", font=("Arial", 12), bg="#FFF1DE", width=25, height=1, anchor="w")
    answer.grid(row=0, column=5, pady=(18, 10), sticky="ew")

    num1 = tkinter.Entry(window, width=8, font=("Arial", 15))
    num1.grid(row=0, column=1, padx=(0, 0), pady=(20, 10), sticky="nsew")
    num1.configure(justify="center")

    num2 = tkinter.Entry(window, width=8, font=("Arial", 15))
    num2.grid(row=0, column=3, padx=(0, 0), pady=(20, 10), sticky="nsew")
    num2.configure(justify="center")

    calc_button = tkinter.Button(window, text="Calculate", command=get_result)
    calc_button.grid(row=2, column=1, columnspan=3, padx=(15, 10), pady=(10, 5), sticky="nsew")
    calc_button.configure(justify="center")

    close_button = tkinter.Button(window, text="Close", command=window.destroy)
    close_button.grid(row=3, column=1, columnspan=3, padx=(15, 10), pady=(0, 10), sticky="nsew")

    window.bind("<Return>", lambda event: get_result())

    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=4)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(5, weight=1)
    window.columnconfigure(3, weight=1)

    window.mainloop()


if __name__ == '__main__':
    open_window()
