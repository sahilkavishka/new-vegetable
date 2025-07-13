import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

class VegetableMarketGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vegetable Market Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # File path to save and load data
        self.vegetable_data = "vegetable_market_data.json"
        
        # Initialize data
        self.load_data()
        
        # Current order variables
        self.current_order = []
        
        # Create main interface
        self.create_main_interface()
        
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.vegetable_data, "r") as file:
                data = json.load(file)
                self.vegetable_name = data.get("vegetable_name", [])
                self.vegetable_price = data.get("vegetable_price", [])
                self.vegetable_store = data.get("vegetable_store", [])
                self.bill_name = data.get("bill_name", [])
                self.quantity = data.get("quantity", [])
                self.amount = data.get("amount", [])
                self.total_sum = data.get("total_sum", [])
                self.vegetable_cost = data.get("vegetable_cost", [])
        except FileNotFoundError:
            self.vegetable_name = []
            self.vegetable_price = []
            self.vegetable_store = []
            self.bill_name = []
            self.quantity = []
            self.amount = []
            self.total_sum = []
            self.vegetable_cost = []
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            "vegetable_name": self.vegetable_name,
            "vegetable_price": self.vegetable_price,
            "vegetable_store": self.vegetable_store,
            "bill_name": self.bill_name,
            "quantity": self.quantity,
            "amount": self.amount,
            "total_sum": self.total_sum,
            "vegetable_cost": self.vegetable_cost
        }
        with open(self.vegetable_data, "w") as file:
            json.dump(data, file)
    
    def create_main_interface(self):
        """Create the main user interface"""
        # Title
        title_label = tk.Label(self.root, text="🥬 Vegetable Market Management System 🥕", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Main buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # Customer buttons
        customer_frame = tk.LabelFrame(button_frame, text="Customer Options", 
                                     font=("Arial", 12, "bold"), bg='#f0f0f0')
        customer_frame.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Button(customer_frame, text="Display Vegetables", command=self.display_vegetables,
                 bg='#3498db', fg='white', font=("Arial", 10, "bold"), width=20, height=2).pack(pady=5)
        
        tk.Button(customer_frame, text="Create Order", command=self.create_order,
                 bg='#2ecc71', fg='white', font=("Arial", 10, "bold"), width=20, height=2).pack(pady=5)
        
        tk.Button(customer_frame, text="View Current Order", command=self.view_current_order,
                 bg='#f39c12', fg='white', font=("Arial", 10, "bold"), width=20, height=2).pack(pady=5)
        
        # Admin buttons
        admin_frame = tk.LabelFrame(button_frame, text="Admin Options", 
                                  font=("Arial", 12, "bold"), bg='#f0f0f0')
        admin_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Button(admin_frame, text="Admin Login", command=self.admin_login,
                 bg='#e74c3c', fg='white', font=("Arial", 10, "bold"), width=20, height=2).pack(pady=5)
        
        # Display area
        self.display_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Initial display
        self.display_vegetables()
    
    def display_vegetables(self):
        """Display available vegetables"""
        # Clear display frame
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        # Create treeview for vegetables
        columns = ('Name', 'Price (Rs/kg)', 'Stock (kg)')
        tree = ttk.Treeview(self.display_frame, columns=columns, show='headings', height=10)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        # Insert data
        for i in range(len(self.vegetable_name)):
            tree.insert('', 'end', values=(
                self.vegetable_name[i].capitalize(),
                f"Rs. {self.vegetable_price[i]:.2f}",
                f"{self.vegetable_store[i]:.2f} kg"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.display_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_order(self):
        """Create a new order window"""
        if not self.vegetable_name:
            messagebox.showwarning("No Vegetables", "No vegetables available for ordering.")
            return
        
        order_window = tk.Toplevel(self.root)
        order_window.title("Create Order")
        order_window.geometry("500x400")
        order_window.configure(bg='#f0f0f0')
        
        # Vegetable selection
        tk.Label(order_window, text="Select Vegetable:", font=("Arial", 12, "bold"), 
                bg='#f0f0f0').pack(pady=10)
        
        vegetable_var = tk.StringVar()
        vegetable_combo = ttk.Combobox(order_window, textvariable=vegetable_var, 
                                     values=[veg.capitalize() for veg in self.vegetable_name],
                                     state="readonly", width=30)
        vegetable_combo.pack(pady=5)
        
        # Quantity input
        tk.Label(order_window, text="Quantity:", font=("Arial", 12, "bold"), 
                bg='#f0f0f0').pack(pady=(20, 5))
        
        quantity_frame = tk.Frame(order_window, bg='#f0f0f0')
        quantity_frame.pack(pady=5)
        
        quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var, width=10)
        quantity_entry.pack(side=tk.LEFT, padx=5)
        
        unit_var = tk.StringVar(value="kg")
        unit_combo = ttk.Combobox(quantity_frame, textvariable=unit_var, 
                                values=["kg", "g"], state="readonly", width=5)
        unit_combo.pack(side=tk.LEFT, padx=5)
        
        # Add to order button
        def add_to_order():
            try:
                selected_veg = vegetable_var.get()
                if not selected_veg:
                    messagebox.showwarning("Selection Error", "Please select a vegetable.")
                    return
                
                quantity_val = float(quantity_var.get())
                unit = unit_var.get()
                
                # Find vegetable index
                veg_index = None
                for i, veg in enumerate(self.vegetable_name):
                    if veg.capitalize() == selected_veg:
                        veg_index = i
                        break
                
                if veg_index is None:
                    messagebox.showerror("Error", "Vegetable not found.")
                    return
                
                # Convert to kg if needed
                required_stock = quantity_val if unit == "kg" else quantity_val / 1000
                
                # Check stock
                if required_stock > self.vegetable_store[veg_index]:
                    messagebox.showwarning("Stock Error", 
                                         f"Not enough stock. Available: {self.vegetable_store[veg_index]:.2f} kg")
                    return
                
                # Calculate price
                price = self.vegetable_price[veg_index] * required_stock
                
                # Add to current order
                self.current_order.append({
                    'name': self.vegetable_name[veg_index],
                    'quantity': f"{quantity_val}{unit}",
                    'price': price,
                    'stock_used': required_stock,
                    'index': veg_index
                })
                
                messagebox.showinfo("Success", f"Added {quantity_val}{unit} of {selected_veg} to order.")
                
                # Clear inputs
                quantity_var.set("")
                vegetable_var.set("")
                
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid quantity.")
        
        tk.Button(order_window, text="Add to Order", command=add_to_order,
                 bg='#2ecc71', fg='white', font=("Arial", 10, "bold")).pack(pady=20)
        
        # Finalize order button
        def finalize_order():
            if not self.current_order:
                messagebox.showwarning("Empty Order", "Please add items to your order first.")
                return
            
            # Update stock and save order
            for item in self.current_order:
                self.vegetable_store[item['index']] -= item['stock_used']
                self.bill_name.append(item['name'])
                self.quantity.append(item['quantity'])
                self.amount.append(item['price'])
            
            self.save_data()
            
            # Show bill
            self.show_bill()
            
            # Clear current order
            self.current_order = []
            
            # Close order window
            order_window.destroy()
            
            # Refresh display
            self.display_vegetables()
        
        tk.Button(order_window, text="Finalize Order", command=finalize_order,
                 bg='#e67e22', fg='white', font=("Arial", 10, "bold")).pack(pady=10)
    
    def view_current_order(self):
        """View current order before finalizing"""
        if not self.current_order:
            messagebox.showinfo("Empty Order", "No items in current order.")
            return
        
        order_window = tk.Toplevel(self.root)
        order_window.title("Current Order")
        order_window.geometry("500x400")
        order_window.configure(bg='#f0f0f0')
        
        # Order details
        text_area = ScrolledText(order_window, height=15, width=50)
        text_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        total = 0
        text_area.insert(tk.END, "=== CURRENT ORDER ===\n\n")
        
        for i, item in enumerate(self.current_order):
            text_area.insert(tk.END, f"{i+1}. {item['name'].capitalize()}\n")
            text_area.insert(tk.END, f"   Quantity: {item['quantity']}\n")
            text_area.insert(tk.END, f"   Price: Rs. {item['price']:.2f}\n\n")
            total += item['price']
        
        text_area.insert(tk.END, f"TOTAL: Rs. {total:.2f}")
        text_area.configure(state='disabled')
        
        # Clear order button
        def clear_order():
            self.current_order = []
            messagebox.showinfo("Success", "Order cleared.")
            order_window.destroy()
        
        tk.Button(order_window, text="Clear Order", command=clear_order,
                 bg='#e74c3c', fg='white', font=("Arial", 10, "bold")).pack(pady=10)
    
    def show_bill(self):
        """Show the final bill"""
        if not self.current_order:
            return
        
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Bill")
        bill_window.geometry("400x500")
        bill_window.configure(bg='#f0f0f0')
        
        # Bill details
        text_area = ScrolledText(bill_window, height=20, width=40)
        text_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        total = 0
        text_area.insert(tk.END, "=== BILL ===\n\n")
        
        for i, item in enumerate(self.current_order):
            text_area.insert(tk.END, f"{i+1}. {item['name'].capitalize()}\n")
            text_area.insert(tk.END, f"   Quantity: {item['quantity']}\n")
            text_area.insert(tk.END, f"   Price: Rs. {item['price']:.2f}\n\n")
            total += item['price']
        
        text_area.insert(tk.END, f"TOTAL: Rs. {total:.2f}\n")
        text_area.insert(tk.END, "\nThank you for shopping with us!")
        text_area.configure(state='disabled')
    
    def admin_login(self):
        """Admin login dialog"""
        password = simpledialog.askstring("Admin Login", "Enter password:", show='*')
        if password == "122333":
            self.admin_panel()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")
    
    def admin_panel(self):
        """Admin panel window"""
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("600x500")
        admin_window.configure(bg='#f0f0f0')
        
        tk.Label(admin_window, text="Admin Panel", font=("Arial", 16, "bold"), 
                bg='#f0f0f0').pack(pady=20)
        
        # Admin buttons
        button_frame = tk.Frame(admin_window, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Add Vegetable", command=self.add_vegetable,
                 bg='#2ecc71', fg='white', font=("Arial", 10, "bold"), width=15).pack(pady=5)
        
        tk.Button(button_frame, text="Update Vegetable", command=self.update_vegetable,
                 bg='#f39c12', fg='white', font=("Arial", 10, "bold"), width=15).pack(pady=5)
        
        tk.Button(button_frame, text="Delete Vegetable", command=self.delete_vegetable,
                 bg='#e74c3c', fg='white', font=("Arial", 10, "bold"), width=15).pack(pady=5)
        
        tk.Button(button_frame, text="Sales Report", command=self.sales_report,
                 bg='#9b59b6', fg='white', font=("Arial", 10, "bold"), width=15).pack(pady=5)
        
        tk.Button(button_frame, text="Profit Report", command=self.profit_report,
                 bg='#34495e', fg='white', font=("Arial", 10, "bold"), width=15).pack(pady=5)
    
    def add_vegetable(self):
        """Add new vegetable"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Vegetable")
        add_window.geometry("400x300")
        add_window.configure(bg='#f0f0f0')
        
        # Input fields
        tk.Label(add_window, text="Vegetable Name:", bg='#f0f0f0').pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var, width=30).pack(pady=5)
        
        tk.Label(add_window, text="Price per kg (Rs.):", bg='#f0f0f0').pack(pady=5)
        price_var = tk.StringVar()
        tk.Entry(add_window, textvariable=price_var, width=30).pack(pady=5)
        
        tk.Label(add_window, text="Cost per kg (Rs.):", bg='#f0f0f0').pack(pady=5)
        cost_var = tk.StringVar()
        tk.Entry(add_window, textvariable=cost_var, width=30).pack(pady=5)
        
        tk.Label(add_window, text="Stock (kg):", bg='#f0f0f0').pack(pady=5)
        stock_var = tk.StringVar()
        tk.Entry(add_window, textvariable=stock_var, width=30).pack(pady=5)
        
        def save_vegetable():
            try:
                name = name_var.get().lower().strip()
                price = float(price_var.get())
                cost = float(cost_var.get())
                stock = float(stock_var.get())
                
                if not name:
                    messagebox.showerror("Error", "Please enter vegetable name.")
                    return
                
                if name in self.vegetable_name:
                    messagebox.showerror("Error", "Vegetable already exists.")
                    return
                
                self.vegetable_name.append(name)
                self.vegetable_price.append(price)
                self.vegetable_cost.append(cost)
                self.vegetable_store.append(stock)
                
                self.save_data()
                messagebox.showinfo("Success", "Vegetable added successfully!")
                add_window.destroy()
                self.display_vegetables()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price, cost, and stock.")
        
        tk.Button(add_window, text="Add Vegetable", command=save_vegetable,
                 bg='#2ecc71', fg='white', font=("Arial", 10, "bold")).pack(pady=20)
    
    def update_vegetable(self):
        """Update existing vegetable"""
        if not self.vegetable_name:
            messagebox.showwarning("No Vegetables", "No vegetables available to update.")
            return
        
        # Selection window
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Vegetable to Update")
        select_window.geometry("300x200")
        select_window.configure(bg='#f0f0f0')
        
        tk.Label(select_window, text="Select Vegetable:", bg='#f0f0f0').pack(pady=10)
        
        vegetable_var = tk.StringVar()
        vegetable_combo = ttk.Combobox(select_window, textvariable=vegetable_var,
                                     values=[veg.capitalize() for veg in self.vegetable_name],
                                     state="readonly", width=30)
        vegetable_combo.pack(pady=10)
        
        def open_update_form():
            selected = vegetable_var.get()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select a vegetable.")
                return
            
            # Find index
            veg_index = None
            for i, veg in enumerate(self.vegetable_name):
                if veg.capitalize() == selected:
                    veg_index = i
                    break
            
            if veg_index is None:
                return
            
            select_window.destroy()
            
            # Update form
            update_window = tk.Toplevel(self.root)
            update_window.title("Update Vegetable")
            update_window.geometry("400x300")
            update_window.configure(bg='#f0f0f0')
            
            # Pre-fill with current values
            tk.Label(update_window, text="Vegetable Name:", bg='#f0f0f0').pack(pady=5)
            name_var = tk.StringVar(value=self.vegetable_name[veg_index])
            tk.Entry(update_window, textvariable=name_var, width=30).pack(pady=5)
            
            tk.Label(update_window, text="Price per kg (Rs.):", bg='#f0f0f0').pack(pady=5)
            price_var = tk.StringVar(value=str(self.vegetable_price[veg_index]))
            tk.Entry(update_window, textvariable=price_var, width=30).pack(pady=5)
            
            tk.Label(update_window, text="Cost per kg (Rs.):", bg='#f0f0f0').pack(pady=5)
            cost_var = tk.StringVar(value=str(self.vegetable_cost[veg_index]))
            tk.Entry(update_window, textvariable=cost_var, width=30).pack(pady=5)
            
            tk.Label(update_window, text="Stock (kg):", bg='#f0f0f0').pack(pady=5)
            stock_var = tk.StringVar(value=str(self.vegetable_store[veg_index]))
            tk.Entry(update_window, textvariable=stock_var, width=30).pack(pady=5)
            
            def save_update():
                try:
                    name = name_var.get().lower().strip()
                    price = float(price_var.get())
                    cost = float(cost_var.get())
                    stock = float(stock_var.get())
                    
                    if not name:
                        messagebox.showerror("Error", "Please enter vegetable name.")
                        return
                    
                    self.vegetable_name[veg_index] = name
                    self.vegetable_price[veg_index] = price
                    self.vegetable_cost[veg_index] = cost
                    self.vegetable_store[veg_index] = stock
                    
                    self.save_data()
                    messagebox.showinfo("Success", "Vegetable updated successfully!")
                    update_window.destroy()
                    self.display_vegetables()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for price, cost, and stock.")
            
            tk.Button(update_window, text="Update Vegetable", command=save_update,
                     bg='#f39c12', fg='white', font=("Arial", 10, "bold")).pack(pady=20)
        
        tk.Button(select_window, text="Select", command=open_update_form,
                 bg='#3498db', fg='white', font=("Arial", 10, "bold")).pack(pady=10)
    
    def delete_vegetable(self):
        """Delete vegetable"""
        if not self.vegetable_name:
            messagebox.showwarning("No Vegetables", "No vegetables available to delete.")
            return
        
        # Selection window
        select_window = tk.Toplevel(self.root)
        select_window.title("Delete Vegetable")
        select_window.geometry("300x200")
        select_window.configure(bg='#f0f0f0')
        
        tk.Label(select_window, text="Select Vegetable to Delete:", bg='#f0f0f0').pack(pady=10)
        
        vegetable_var = tk.StringVar()
        vegetable_combo = ttk.Combobox(select_window, textvariable=vegetable_var,
                                     values=[veg.capitalize() for veg in self.vegetable_name],
                                     state="readonly", width=30)
        vegetable_combo.pack(pady=10)
        
        def confirm_delete():
            selected = vegetable_var.get()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select a vegetable.")
                return
            
            # Find index
            veg_index = None
            for i, veg in enumerate(self.vegetable_name):
                if veg.capitalize() == selected:
                    veg_index = i
                    break
            
            if veg_index is None:
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected}?"):
                del self.vegetable_name[veg_index]
                del self.vegetable_price[veg_index]
                del self.vegetable_cost[veg_index]
                del self.vegetable_store[veg_index]
                
                self.save_data()
                messagebox.showinfo("Success", "Vegetable deleted successfully!")
                select_window.destroy()
                self.display_vegetables()
        
        tk.Button(select_window, text="Delete", command=confirm_delete,
                 bg='#e74c3c', fg='white', font=("Arial", 10, "bold")).pack(pady=10)
    
    def sales_report(self):
        """Show sales report"""
        if not self.bill_name:
            messagebox.showinfo("No Sales", "No sales data available.")
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Sales Report")
        report_window.geometry("500x400")
        report_window.configure(bg='#f0f0f0')
        
        text_area = ScrolledText(report_window, height=20, width=50)
        text_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        total_sales = 0
        text_area.insert(tk.END, "=== SALES REPORT ===\n\n")
        
        for i in range(len(self.bill_name)):
            text_area.insert(tk.END, f"{i+1}. {self.bill_name[i].capitalize()}\n")
            text_area.insert(tk.END, f"   Quantity: {self.quantity[i]}\n")
            text_area.insert(tk.END, f"   Amount: Rs. {self.amount[i]:.2f}\n\n")
            total_sales += self.amount[i]
        
        text_area.insert(tk.END, f"TOTAL SALES: Rs. {total_sales:.2f}")
        text_area.configure(state='disabled')
    
    def profit_report(self):
        """Show profit report"""
        if not self.bill_name:
            messagebox.showinfo("No Sales", "No sales data available.")
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Profit Report")
        report_window.geometry("500x400")
        report_window.configure(bg='#f0f0f0')
        
        text_area = ScrolledText(report_window, height=20, width=50)
        text_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        total_profit = 0
        text_area.insert(tk.END, "=== PROFIT REPORT ===\n\n")
        
        for i in range(len(self.bill_name)):
            try:
                # Find vegetable index
                veg_index = self.vegetable_name.index(self.bill_name[i])
                sell_price = self.vegetable_price[veg_index]
                cost_price = self.vegetable_cost[veg_index]
                
                # Parse quantity
                qty_str = self.quantity[i]
                if qty_str.endswith("kg"):
                    qty = float(qty_str.replace("kg", ""))
                elif qty_str.endswith("g"):
                    qty = float(qty_str.replace("g", "")) / 1000
                else:
                    continue
                
                profit = (sell_price - cost_price) * qty
                total_profit += profit
                
                text_area.insert(tk.END, f"{i+1}. {self.bill_name[i].capitalize()}\n")
                text_area.insert(tk.END, f"   Quantity: {qty_str}\n")
                text_area.insert(tk.END, f"   Profit: Rs. {profit:.2f}\n\n")
                
            except (ValueError, IndexError):
                continue
        
        text_area.insert(tk.END, f"TOTAL PROFIT: Rs. {total_profit:.2f}")
        text_area.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = VegetableMarketGUI(root)
    root.mainloop()