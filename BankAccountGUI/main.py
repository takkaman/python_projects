import tkinter as tk
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
# Set window size here to '440x640' pixels
win.geometry('440x640')
# Set window title here to 'FedUni Banking'
win.winfo_toplevel().title("FedUni Banking")
# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, show="*", textvariable=pin_number_var)

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(win)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48, font=('Arial',9))

# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    account_pin_entry.delete(0, 'end')

def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''    
    global pin_number_var
    global account_pin_entry
    # Limit to 4 chars in length
    # pin_val = pin_number_var.get()
    # print(len(pin_val))
    # if len(pin_val) < 4:
    #     account_pin_entry.insert(END, 0)
    # Set the new pin number on the pin_number_var
    pin_number_var.set(pin_number_var.get()+event.widget['text'])


def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_num_entry
    global account_number_var

    # Create the filename from the entered account number with '.txt' on the end
    file_name = account_number_var.get()+".txt"
    # Try to open the account file for reading
    try:
        # Open the account file for reading
        fp = open(file_name, 'r')
        lines = fp.readlines()
        # First line is account number
        account.account_number = lines[0].strip()
        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read 
        psw_txt = lines[1].strip()
        if psw_txt != pin_number_var.get():
            raise Exception
        account.pin_number = psw_txt
        # Read third and fourth lines (balance and interest rate) 
        account.balance = lines[2].strip()
        account.interest_rate = lines[3].strip()
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        for i in range(4,len(lines)):
            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list            
            if i % 2 == 0:
                action = lines[i].strip()
            else:
                amount = lines[i].strip()
                account.transaction_list.append((action, amount))
        # Close the file now we're finished with it
        fp.close()
    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except IOError:
        tk.messagebox.showinfo("Error", "Invalid account number - please try again!")
        clear_pin_entry(event)
    except Exception:
        # Show error messagebox and & reset BankAccount object to default...
        tk.messagebox.showinfo("Error", "PIN entered did not match account PIN")
        #  ...also clear PIN entry and change focus to account number entry
        clear_pin_entry(event)
    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    else:
        create_account_screen()

# ---------- Button Handlers for Account Screen ----------


def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    
    # Reset the bank acount object

    # Reset the account number and pin to blank

    # Remove all widgets and display the login screen again
    remove_all_widgets()
    account_pin_entry.delete(0, 'end')
    create_login_screen()


def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var


    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        account.balance = float(amount_entry.get())+float(account.balance)
        # Deposit funds
        
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        account.transaction_list.append(("Deposit", amount_entry.get()))
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.configure(state='normal')
        transaction_text_widget.insert('end', "Deposit\n")
        transaction_text_widget.insert('end', "{0:.1f}\n".format(float(amount_entry.get())))
        transaction_text_widget.configure(state='disabled')
        # Change the balance label to reflect the new balance
        balance_var.set("Balance: ${0:.1f}".format(float(account.balance)))
        # Clear the amount entry
        amount_entry.delete(0, 'end')
        # Update the interest graph with our new balance

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except Exception as e:
        tk.messagebox.showinfo("Transaction Error", e)
        
def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method
        
        # Withdraw funds        

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        # Change the balance label to reflect the new balance

        # Clear the amount entry

        # Update the interest graph with our new balance

    # Catch and display any returned exception as a messagebox 'showerror'
        

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    x = 1
    y = 2
    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5,2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')

# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''
    # ----- Row 0 -----
    label = tk.Label(win,text="FedUni Banking", font=("Arial", 32)).grid(row=0,columnspan=3)

    # 'FedUni Banking' label here. Font size is 32.

    # ----- Row 1 -----

    # Acount Number / Pin label here
    label1 = tk.Label(win,text="Account Number / Pin").grid(row=1, column=0, sticky='nsew')
    # Account number entry here
    account_number_entry.grid(row=1, column=1, sticky='nsew')
    # Account pin entry here
    account_pin_entry.grid(row=1, column=2, sticky='nsew')
    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button1 = tk.Button(win, text='1')
    button1.grid(row=2, column=0, sticky='nsew')
    button1.bind('<Button-1>',handle_pin_button)
    button2 = tk.Button(win, text='2')
    button2.grid(row=2, column=1, sticky='nsew')
    button2.bind('<Button-1>',handle_pin_button)
    button3 = tk.Button(win, text='3')
    button3.grid(row=2, column=2, sticky='nsew')
    button3.bind('<Button-1>',handle_pin_button)
    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button4 = tk.Button(win, text='4')
    button4.grid(row=3, column=0, sticky='nsew')
    button4.bind('<Button-1>',handle_pin_button)
    button5 = tk.Button(win, text='5')
    button5.grid(row=3, column=1, sticky='nsew')
    button5.bind('<Button-1>',handle_pin_button)
    button6 = tk.Button(win, text='6')
    button6.grid(row=3, column=2, sticky='nsew')
    button6.bind('<Button-1>',handle_pin_button)

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button7 = tk.Button(win, text='7')
    button7.grid(row=4, column=0, sticky='nsew')
    button7.bind('<Button-1>',handle_pin_button)
    button8 = tk.Button(win, text='8')
    button8.grid(row=4, column=1, sticky='nsew')
    button8.bind('<Button-1>',handle_pin_button)
    button9 = tk.Button(win, text='9')
    button9.grid(row=4, column=2, sticky='nsew')
    button9.bind('<Button-1>',handle_pin_button)

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    button_ccl = tk.Button(win, text='Cancel/Clear', bg = 'red')
    button_ccl.grid(row=5, column=0, sticky='nsew')
    button_ccl.bind('<Button-1>', clear_pin_entry)
    # Button 0 here
    button0 = tk.Button(win, text='0')
    button0.grid(row=5, column=1, sticky='nsew')
    button0.bind('<Button-1>',handle_pin_button)
    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    button_login = tk.Button(win, text='Log In', bg = 'green')
    button_login.grid(row=5, column=2, sticky='nsew')
    button_login.bind('<Button-1>', log_in)
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.rowconfigure(0, weight=1)
    win.columnconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.columnconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.columnconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)

    win.rowconfigure(4, weight=1)

    win.rowconfigure(5, weight=1)


def create_account_screen():
    '''Function to create the account screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    global account

    remove_all_widgets()
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    label = tk.Label(win,text="FedUni Banking", font=("Arial", 24)).grid(row=0, columnspan=3)

    # ----- Row 1 -----

    # Account number label here
    account_lb = tk.Label(win, text="Account Number: $"+account.account_number)
    account_lb.grid(row=1, column=0, sticky='nsew')
    # Balance label here
    balance_var.set("Balance: $"+account.balance)
    balance_label.grid(row=1, column=1, sticky='nsew')
    # Log out button here
    logout = tk.Button(win, text="Log Out", command=save_and_log_out)
    logout.grid(row=1, column=2, columnspan=3, sticky='nsew')
    # logout.bind('<Button-1>', save_and_log_out)
    # ----- Row 2 -----

    # Amount label here
    amount_lb = tk.Label(win, text="Amount ($)")
    amount_lb.grid(row=2, column=0, sticky='nsew')
    # Amount entry here
    amount_entry.grid(row=2, column=1, sticky='nsew')
    # Deposit button here
    button_dep = tk.Button(win, text='Deposit', command=perform_deposit)
    button_dep.grid(row=2, column=2, sticky='nsew')
    # Withdraw button here
    button_wtd = tk.Button(win, text='Withdraw', command=perform_withdrawal)
    button_wtd.grid(row=2, column=3, columnspan=2, sticky='nsew')
    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    text_scrollbar = tk.Scrollbar(win)
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    transaction_text_widget.configure(state='disabled', yscrollcommand=text_scrollbar.set)
    transaction_text_widget.grid(row=3, column=0, columnspan=4, sticky='nsew')
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    transaction_text_widget.configure(state='normal')
    for (action,amount) in account.transaction_list:
        transaction_text_widget.insert('end', action+"\n")
        transaction_text_widget.insert('end', amount+"\n")
    transaction_text_widget.configure(state='disabled')
    # Now add the scrollbar and set it to change with the yview of the text widget

    text_scrollbar.grid(row=3, column=4, sticky='nsew')

    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    win.rowconfigure(0, weight=1)
    win.columnconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.columnconfigure(1, weight=1)

create_login_screen()
# create_account_screen()
win.mainloop()
