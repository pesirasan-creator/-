import tkinter as tk
from tkinter import messagebox, ttk

def show_main_app(root):
    root.title("โปรแกรมบันทึกรายรับ-รายจ่าย")
    root.geometry("500x550")
    root.config(bg="#f0f0f0") 

    style = ttk.Style(root)
    style.theme_use("clam") 

    style.configure("TLabel", font=("Tahoma", 11), background="#f0f0f0")
    style.configure("TButton", font=("Tahoma", 11, "bold"), padding=5)
    style.configure("TRadiobutton", font=("Tahoma", 10), background="#f0f0f0")
    style.configure("TEntry", font=("Tahoma", 11), padding=3)
    
    style.configure("Summary.TLabel", font=("Tahoma", 12, "bold"), padding=10, 
                    background="#e9e9e9", relief="solid", borderwidth=1, anchor="center")
    style.configure("Success.TLabel", font=("Tahoma", 12, "bold"), padding=10, 
                    background="#dff0d8", foreground="#3c763d", relief="solid", borderwidth=1, anchor="center")
    style.configure("Error.TLabel", font=("Tahoma", 12, "bold"), padding=10, 
                    background="#f2dede", foreground="#a94442", relief="solid", borderwidth=1, anchor="center")

    records = []

    input_frame = ttk.Frame(root, padding="15")
    input_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(input_frame, text="รายการ:").pack(pady=5)
    entry_name = ttk.Entry(input_frame, width=40)
    entry_name.pack(pady=2, ipady=3) 

    ttk.Label(input_frame, text="จำนวนเงิน:").pack(pady=5)
    entry_amount = ttk.Entry(input_frame, width=40)
    entry_amount.pack(pady=2, ipady=3)

    radio_frame = ttk.Frame(input_frame)
    radio_frame.pack(pady=10)
    var_type = tk.StringVar(value="รายจ่าย") 
    ttk.Radiobutton(radio_frame, text="รายรับ", variable=var_type, value="รายรับ").pack(side="left", padx=20)
    ttk.Radiobutton(radio_frame, text="รายจ่าย", variable=var_type, value="รายจ่าย").pack(side="left", padx=20)

    def add_record():
        name = entry_name.get()
        amount = entry_amount.get()
        category = var_type.get()
        
        if name == "" or  amount == "":
            messagebox.showwarning("คำเตือน", "กรุณากรอกข้อมูลให้ครบ")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showwarning("คำเตือน", "จำนวนเงินต้องมากกว่า 0")
                return
                
            records.append((name, category, amount))
            update_list()
            entry_name.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            var_type.set("รายจ่าย") 
            entry_name.focus() 
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "จำนวนเงินต้องเป็นตัวเลขเท่านั้น")

    def update_list():
        listbox.delete(0, tk.END)
        total_income = 0
        total_expense = 0
        
        for r in records:
            name, category, amount = r
            text = f"{name} ({category}) - {amount:.2f} บาท"
            listbox.insert(tk.END, text)
            
            if category == "รายรับ":
                total_income += amount
                listbox.itemconfig(tk.END, {'fg': '#006400'}) 
            else:
                total_expense += amount
                listbox.itemconfig(tk.END, {'fg': '#8B0000'}) 
                
        balance = total_income - total_expense
        summary_text = f"รายรับ: {total_income:.2f} | รายจ่าย: {total_expense:.2f} | คงเหลือ: {balance:.2f}"
        label_summary.config(text=summary_text)
        
        if balance > 0:
            label_summary.config(style="Success.TLabel")
        elif balance < 0:
            label_summary.config(style="Error.TLabel")
        else:
            label_summary.config(style="Summary.TLabel")
            
    ttk.Button(root, text="เพิ่มข้อมูล", command=add_record).pack(pady=10, ipady=5)

    output_frame = ttk.Frame(root, padding="10")
    output_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
    listbox = tk.Listbox(output_frame, width=60, height=10, 
                         font=("Courier New", 10), 
                         yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)

    label_summary = ttk.Label(root, text="รายรับ: 0.00 | รายจ่าย: 0.00 | คงเหลือ: 0.00", 
                              style="Summary.TLabel")
    label_summary.pack(fill="x", padx=10, pady=10)


def show_splash_screen(root):
    splash = tk.Toplevel(root) 
    splash.title("Loading")
    
    splash_width = 350
    splash_height = 200
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width / 2) - (splash_width / 2)
    y = (screen_height / 2) - (splash_height / 2)
    splash.geometry(f'{splash_width}x{splash_height}+{int(x)}+{int(y)}')
    
    splash.overrideredirect(True) 
    
    splash.config(bg="#f0f0f0")
    frame = tk.Frame(splash, bg="#f0f0f0", highlightbackground="#0078d4", highlightthickness=2)
    frame.pack(expand=True, fill="both", padx=5, pady=5)
    
    tk.Label(frame, text="โปรแกรมบันทึกรายรับ-รายจ่าย", 
             font=("Tahoma", 16, "bold"), bg="#f0f0f0").pack(pady=20)
    
    tk.Label(frame, text="กำลังโหลด...", 
             font=("Tahoma", 11), bg="#f0f0f0").pack(pady=5)
    
    progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10, padx=20)
    
    def update_progress(value):
        progress['value'] = value
        if value < 100:
            splash.after(20, lambda: update_progress(value + 1))
        else:
            splash.destroy()
            root.deiconify() 

    splash.after(100, lambda: update_progress(0)) 


if __name__ == "__main__":
    
    root = tk.Tk()
    
    root.withdraw()
    
    show_splash_screen(root) 
    show_main_app(root)      
    
    root.mainloop()