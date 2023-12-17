from tkinter import *
import tkinter as tk
import time

is_int = [True]
memory = {'ANS':0, 'M*':'-', 'M':0}
oper = ['+', '-', '/', '*', '//', '%', '√']
numbers = [str(i) for i in range(10)]
expression = ['']

def eval_expr(expr):
    if expr == '':
        return 0
    
    n = len(expr)

# leveling

    level = 0
    levels = {}
    t = 0
    while t < n:
        if expr[t] == '(':
            level += 1
        elif expr[t] == ')':
            level -= 1
        else:
            levels[t] = level
        t += 1

    min_level = min(levels[t] for t in levels)

    if min_level > 0:
        return eval_expr(expr[1:n-1])
    
# finding sqrt

    # finding sqrt

    for t in range(n):
        if expr[t] == '√':
            if expr[t + 1] != '(':
                i = t + 1
                while i < n:
                    if expr[i] not in numbers and expr[i] != '.':
                        break
                    i += 1
                if i == n:
                    return eval_expr(expr[0:t] + str(eval_expr(expr[t+1:i]) ** 0.5))
                return eval_expr(expr[0:t] + str(eval_expr(expr[t+1:i]) ** 0.5) + expr[i:])
            else:
                count = 1
                for i in range(t+2, n):
                    if expr[i] == '(':
                        count += 1
                    elif expr[i] == ')':
                        count -= 1
                                 
                    if count == 0:
                        return eval_expr(expr[0:t] + str(eval_expr(expr[t+2:i]) ** 0.5) + expr[i+1:])
            

# finding plus

    for t in range(n):
        if expr[t] == '+' and levels[t] == min_level:
            a = eval_expr(expr[:t])
            b = eval_expr(expr[t+1:])
            return a + b

# finding minus in the middle

    for t in range(n - 1, 0, -1):
        if expr[t] == '-' and levels[t] == min_level:
            a = eval_expr(expr[:t])
            b = eval_expr(expr[t+1:])
            return a - b

# minus in the beginning
    
    if expr[0] == '-':
        return -eval_expr(expr[1:])

# finding others

    for t in range(n - 1, -1, -1):
        if expr[t] in oper and levels[t] == min_level:
            if expr[t] == '*':
                a = eval_expr(expr[:t])
                b = eval_expr(expr[t+1:])
                return a * b
            elif expr[t] == '%':
                a = eval_expr(expr[:t])
                b = eval_expr(expr[t+1:])
                return a % b
            elif expr[t] == '/' and t > 0 and expr[t-1] == '/':
                a = eval_expr(expr[:t-1])
                b = eval_expr(expr[t+1:])
                return a // b
            elif expr[t] == '/':
                a = eval_expr(expr[:t])
                b = eval_expr(expr[t+1:])
                if is_int and a % b == 0:
                    return a // b
                is_int[0] = False
                return a / b

# no operations

    if '.' in expr:
        is_int[0] = False
        return float(expr)

    return int(expr)

#----------------------
# Functions for buttons

def button_click(name):
    if name in numbers or name in oper or name in {'.', '(', ')'}:
        entry.insert(END, name)
    if name == '=':
        try:
            expr = entry.get()
            ans = round(eval_expr(expr), 7)
            if abs(ans - round(ans)) < 10**(-5):
                ans = round(ans)
            memory['ANS'] = ans
            entry.delete(0, END)
            entry.insert(0, ans)
            entry.configure(bg="white")
        except Exception:
            entry.configure(bg="#FFA07A")
    if name == '+/-':
        expr = entry.get()
        if len(expr) > 0:
            if expr[0] == '-':
                entry.delete(0, END)
                entry.insert(0, expr[1:])
            else:
                entry.insert(0, '-')
    if name == 'C':
        entry.configure(bg="white")
        memory['ANS'] = 0
        memory['M*'] = '-'
        buttons[(0, 1)].configure(text='M'+'*')
        entry.delete(0, END)
            
    if name in memory:
        if name == 'ANS':
            entry.insert(END, str(memory['ANS']))
        elif memory[name] == '-':
            try:
                expr = entry.get()
                ans = eval_expr(expr)
                memory['M*'] = ans
                buttons[(0, 1)].configure(text='M')
                entry.configure(bg="white")
            except Exception:
                entry.configure(bg="#FFA07A")
        else:
            entry.insert(END, str(memory[name]))


#----------------------------
# Making the interface window

root = Tk()
root.geometry("268x235")
root.title("Калькулятор")
root.resizable(0, 0)

def Enter(event):
    button_click('=')

buttons = {}

frame = Frame(root, width = 30, height = 30)
frame.grid(row=0, column=0, columnspan = 5)

entry = tk.Entry(frame, width = 44)
entry.grid(row=0, column=0)

name_buttons = (('ANS', 'M*', '(', ')', 'C'),
           ('7', '8', '9', '/', '//'),
           ('4', '5', '6', '*', '%'),
           ('1', '2', '3', '-', '√'),
           ('0', '.', '+/-', '+', '='))

for row in range(5):
    for col in range(5):
        buttons[(row, col)] = tk.Button(root, width=2, bg = 'white', height=2, text = name_buttons[row][col], command = lambda row=row, col=col: button_click(name_buttons[row][col]))
        buttons[(row, col)].grid(row=row + 2, column=col, sticky="nsew", padx=1, pady=1)
root.bind('<Return>', Enter)
button_click('C')
root.mainloop()
