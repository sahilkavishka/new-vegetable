#!/usr/bin/env python3
"""
Enhanced Vegetable Market Management System
A comprehensive single-window GUI application for managing vegetable inventory and orders
"""

import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import os

class VegetableMarket:
    def __init__(self):
        self.data_file = "vegetable_market_data.json"
        self.load_data()
        self.setup_gui()
        
    def load_data(self):
        """Load data from JSON file or initialize empty data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    self.vegetables = data.get("vegetables", {})
                    self.orders = data.get("orders", [])
            else:
                self.vegetables = {}
                self.orders = []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
            self.vegetables = {}
            self.orders = []

    def save_data(self):
        """Save current data to JSON file"""
        try:
            data = {
                "vegetables": self.vegetables,
                "orders": self.orders
            }
            with open(self.data_file, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
            return False

    def setup_gui(self):
        """Initialize the main GUI"""
        self.root = tk.Tk()
        self.root.title("🥬 Vegetable Market Management System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(True, True)
        
        # Configure main grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create header frame
        self.create_header()
        
        # Create main content frame
        self.main_frame = tk.Frame(self.root, bg='#f8f9fa')
        self.main_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create navigation frame
        self.create_navigation()
        
        # Show main menu by default
        self.show_main_menu()
        
    def create_header(self):
        """Create the header with title and navigation"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.grid(row=0, column=0, sticky='ew')
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        
        # Logo/Icon
        logo_label = tk.Label(
            header_frame,
            text="🥬🥕",
            font=("Arial", 24),
            bg='#2c3e50',
            fg='white'
        )
        logo_label.grid(row=0, column=0, padx=20, pady=5)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Vegetable Market Management System",
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.grid(row=0, column=1, pady=15)
        
        # Current time display
        self.time_label = tk.Label(
            header_frame,
            text="",
            font=("Arial", 10),
            bg='#2c3e50',
            fg="#f5f7f8"
        )
        self.time_label.grid(row=0, column=2, padx=20, pady=15)
        self.update_time()
        
    def update_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def create_navigation(self):
        """Create navigation buttons"""
        nav_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        nav_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        nav_frame.grid_columnconfigure(7, weight=1)  # Make last column expandable
        
        nav_style = {
            'height': 2,
            'font': ("Arial", 10, "bold"),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 15
        }
        
        # Navigation buttons
        buttons = [
            ("🏠 Home", self.show_main_menu, '#3498db'),
            ("📋 Vegetables", self.show_vegetables, '#27ae60'),
            ("🛒 Order", self.show_create_order, '#f39c12'),
            ("📊 History", self.show_order_history, '#9b59b6'),
            ("⚙️ Admin", self.show_admin_panel, '#e74c3c'),
            ("❌ Exit", self.confirm_exit, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                nav_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                **nav_style
            )
            btn.grid(row=0, column=i, padx=5, sticky='w')
            
    def clear_content(self):
        """Clear the content area"""
        for widget in self.main_frame.winfo_children():
            if widget != self.main_frame.winfo_children()[0]:  # Keep navigation
                widget.destroy()
                
    def show_main_menu(self):
        """Show the main menu"""
        self.clear_content()
        
        content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        content_frame.grid(row=1, column=0, sticky='nsew', pady=20)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome section
        welcome_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=2)
        welcome_frame.grid(row=0, column=0, sticky='nsew', padx=50, pady=20)
        
        tk.Label(
            welcome_frame,
            text="Welcome to Vegetable Market System",
            font=("Arial", 18, "bold"),
            bg='white', fg='#2c3e50'
        ).pack(pady=30)
        
        # Quick stats
        self.show_quick_stats(welcome_frame)
        
        # Quick actions
        actions_frame = tk.Frame(welcome_frame, bg='white')
        actions_frame.pack(pady=30)
        
        tk.Label(
            actions_frame,
            text="Quick Actions:",
            font=("Arial", 14, "bold"),
            bg='white', fg='#34495e'
        ).pack(pady=(0, 15))
        
        action_buttons = [
            ("View Available Vegetables", self.show_vegetables, '#27ae60'),
            ("Place New Order", self.show_create_order, '#f39c12'),
            ("Check Order History", self.show_order_history, '#9b59b6')
        ]
        
        for text, command, color in action_buttons:
            tk.Button(
                actions_frame,
                text=text,
                command=command,
                bg=color, fg='white',
                font=("Arial", 11),
                width=25, height=2,
                relief='flat', cursor='hand2'
            ).pack(pady=5)
            
    def show_quick_stats(self, parent):
        """Show quick statistics on main menu"""
        stats_frame = tk.Frame(parent, bg='white')
        stats_frame.pack(pady=20)
        
        # Calculate stats
        total_vegetables = len(self.vegetables)
        total_orders = len(self.orders)
        total_revenue = sum(order.get("amount", 0) for order in self.orders)
        
        stats = [
            ("🥬 Total Vegetables", total_vegetables, '#27ae60'),
            ("🛒 Total Orders", total_orders, '#3498db'),
            ("💰 Total Revenue", f"Rs. {total_revenue:.2f}", '#e74c3c')
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg=color, width=150, height=80)
            stat_frame.grid(row=0, column=i, padx=10, pady=5)
            stat_frame.grid_propagate(False)
            
            tk.Label(
                stat_frame, text=label,
                font=("Arial", 10, "bold"),
                bg=color, fg='white'
            ).pack(pady=(10, 5))
            
            tk.Label(
                stat_frame, text=str(value),
                font=("Arial", 14, "bold"),
                bg=color, fg='white'
            ).pack()

    def show_vegetables(self):
        """Display available vegetables"""
        self.clear_content()
        
        content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        tk.Label(
            content_frame,
            text="📋 Available Vegetables",
            font=("Arial", 16, "bold"),
            bg='#f8f9fa', fg='#2c3e50'
        ).grid(row=0, column=0, pady=15)
        
        # Table frame
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Create treeview
        columns = ("Name", "Price (Rs/kg)", "Stock (kg)", "Status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        tree.column("Name", width=200, anchor="w")
        tree.column("Price (Rs/kg)", width=150, anchor="center")
        tree.column("Stock (kg)", width=150, anchor="center")
        tree.column("Status", width=120, anchor="center")
        
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, c))
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Populate data
        if self.vegetables:
            for name, data in sorted(self.vegetables.items()):
                stock = data.get('stock', 0)
                status = "In Stock" if stock > 0 else "Out of Stock"
                status_tag = "available" if stock > 0 else "unavailable"
                
                item = tree.insert("", "end", values=(
                    name.capitalize(),
                    f"{data.get('price', 0):.2f}",
                    f"{stock:.2f}",
                    status
                ), tags=(status_tag,))
        else:
            tree.insert("", "end", values=("No vegetables available", "", "", ""))
        
        # Configure tags for styling
        tree.tag_configure("available", foreground="green")
        tree.tag_configure("unavailable", foreground="red")
        
    def show_create_order(self):
        """Show order creation interface"""
        self.clear_content()
        
        if not self.vegetables:
            self.show_message("No vegetables available. Please contact admin.", "info")
            return
            
        content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Main order frame
        order_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=2)
        order_frame.grid(row=0, column=0, sticky='nsew', padx=50, pady=20)
        
        tk.Label(
            order_frame,
            text="🛒 Create New Order",
            font=("Arial", 16, "bold"),
            bg='white', fg='#2c3e50'
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(order_frame, bg='white')
        form_frame.pack(pady=20)
        
        # Vegetable selection
        tk.Label(form_frame, text="Select Vegetable:", font=("Arial", 12), bg='white').grid(row=0, column=0, sticky='w', pady=10)
        
        self.vegetable_var = tk.StringVar()
        vegetable_combo = ttk.Combobox(
            form_frame,
            textvariable=self.vegetable_var,
            values=[f"{name.capitalize()} (Rs.{data['price']:.2f}/kg - {data['stock']:.2f}kg available)" 
                   for name, data in self.vegetables.items() if data['stock'] > 0],
            state="readonly",
            width=50
        )
        vegetable_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Quantity input
        tk.Label(form_frame, text="Quantity:", font=("Arial", 12), bg='white').grid(row=1, column=0, sticky='w', pady=10)
        
        quantity_frame = tk.Frame(form_frame, bg='white')
        quantity_frame.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        
        self.quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(quantity_frame, textvariable=self.quantity_var, width=15, font=("Arial", 11))
        quantity_entry.pack(side="left", padx=(0, 5))
        
        self.unit_var = tk.StringVar(value="kg")
        unit_combo = ttk.Combobox(
            quantity_frame,
            textvariable=self.unit_var,
            values=["kg", "g"],
            state="readonly",
            width=8
        )
        unit_combo.pack(side="left")
        
        # Price display
        self.price_label = tk.Label(
            form_frame, text="", 
            font=("Arial", 14, "bold"), 
            bg='white'
        )
        self.price_label.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind events
        self.vegetable_var.trace('w', self.update_order_price)
        self.quantity_var.trace('w', self.update_order_price)
        self.unit_var.trace('w', self.update_order_price)
        
        # Buttons
        button_frame = tk.Frame(order_frame, bg='white')
        button_frame.pack(pady=30)
        
        tk.Button(
            button_frame,
            text="Place Order",
            command=self.place_order,
            bg='#28a745', fg='white',
            font=("Arial", 12, "bold"),
            width=15, height=2,
            relief='flat', cursor='hand2'
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_order_form,
            bg='#6c757d', fg='white',
            font=("Arial", 12),
            width=15, height=2,
            relief='flat', cursor='hand2'
        ).pack(side="left", padx=10)
        
    def update_order_price(self, *args):
        """Update price display in real-time"""
        try:
            selection = self.vegetable_var.get()
            if not selection or not self.quantity_var.get():
                self.price_label.config(text="", fg="black")
                return
                
            # Extract vegetable name from selection
            veg_name = selection.split(" (")[0].lower()
            
            if veg_name not in self.vegetables:
                return
                
            quantity = float(self.quantity_var.get())
            unit = self.unit_var.get()
            
            # Convert to kg if needed
            quantity_kg = quantity / 1000 if unit == "g" else quantity
            
            if quantity_kg > self.vegetables[veg_name]["stock"]:
                self.price_label.config(text="❌ Insufficient stock!", fg="red")
            else:
                total_price = quantity_kg * self.vegetables[veg_name]["price"]
                self.price_label.config(text=f"💰 Total: Rs. {total_price:.2f}", fg="green")
                
        except (ValueError, KeyError):
            self.price_label.config(text="", fg="black")
            
    def clear_order_form(self):
        """Clear the order form"""
        self.vegetable_var.set("")
        self.quantity_var.set("")
        self.unit_var.set("kg")
        self.price_label.config(text="")
        
    def place_order(self):
        """Place the order"""
        try:
            selection = self.vegetable_var.get()
            if not selection:
                self.show_message("Please select a vegetable", "error")
                return
                
            veg_name = selection.split(" (")[0].lower()
            quantity = float(self.quantity_var.get())
            unit = self.unit_var.get()
            
            if quantity <= 0:
                self.show_message("Quantity must be positive", "error")
                return
            
            # Convert to kg
            quantity_kg = quantity / 1000 if unit == "g" else quantity
            
            if quantity_kg > self.vegetables[veg_name]["stock"]:
                self.show_message("Insufficient stock available", "error")
                return
            
            # Calculate total
            total_amount = quantity_kg * self.vegetables[veg_name]["price"]

            cost_price = self.vegetables[veg_name].get("cost", 0)
            profit = round((self.vegetables[veg_name]["price"] - cost_price) * quantity_kg, 2)

            
            # Update stock
            self.vegetables[veg_name]["stock"] -= quantity_kg
            
            # Add to orders
            order = {
                "name": veg_name,
                "quantity": f"{quantity}{unit}",
                "amount": round(total_amount, 2),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "profit":profit,
            }
            self.orders.append(order)
            
            # Save data
            if self.save_data():
                self.show_message(
                    f"Order placed successfully!\n"
                    f"Vegetable: {veg_name.capitalize()}\n"
                    f"Quantity: {quantity}{unit}\n"
                    f"Total Amount: Rs. {total_amount:.2f}",
                    "success"
                )
                self.clear_order_form()
            
        except ValueError:
            self.show_message("Please enter a valid quantity", "error")
        except Exception as e:
            self.show_message(f"An error occurred: {e}", "error")

    def show_order_history(self):
        """Display order history"""
        self.clear_content()
        
        content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Title and summary
        title_frame = tk.Frame(content_frame, bg='#f8f9fa')
        title_frame.grid(row=0, column=0, sticky='ew', pady=15)
        title_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(
            title_frame,
            text="📊 Order History",
            font=("Arial", 16, "bold"),
            bg='#f8f9fa', fg='#2c3e50'
        ).grid(row=0, column=0, sticky='w')
        
        # Summary
        total_amount = sum(order.get("amount", 0) for order in self.orders)
        summary_label = tk.Label(
            title_frame,
            text=f"Total Orders: {len(self.orders)} | Total Revenue: Rs. {total_amount:.2f}",
            font=("Arial", 12, "bold"),
            bg='#f8f9fa', fg='#27ae60'
        )
        summary_label.grid(row=0, column=1, sticky='e')
        
        # Table frame
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Create treeview
        columns = ("Date", "Time", "Vegetable", "Quantity", "Amount (Rs)")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        tree.column("Date", width=120, anchor="center")
        tree.column("Time", width=100, anchor="center")
        tree.column("Vegetable", width=150, anchor="w")
        tree.column("Quantity", width=120, anchor="center")
        tree.column("Amount (Rs)", width=120, anchor="center")
        
        for col in columns:
            tree.heading(col, text=col)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Populate orders (latest first)
        if self.orders:
            for order in reversed(self.orders):
                date_time = order.get("date", "").split(" ")
                date_part = date_time[0] if len(date_time) > 0 else ""
                time_part = date_time[1] if len(date_time) > 1 else ""
                
                tree.insert("", "end", values=(
                    date_part,
                    time_part,
                    order.get("name", "").capitalize(),
                    order.get("quantity", ""),
                    f"{order.get('amount', 0):.2f}"
                ))
        else:
            tree.insert("", "end", values=("No orders found", "", "", "", ""))

    def show_admin_panel(self):
        """Show admin panel after authentication"""
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if password != "admin123":
            self.show_message("Incorrect password!", "error")
            return
            
        self.clear_content()
        
        content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        tk.Label(
            content_frame,
            text="⚙️ Admin Panel",
            font=("Arial", 16, "bold"),
            bg='#f8f9fa', fg='#e74c3c'
        ).grid(row=0, column=0, pady=15)
        
        # Admin actions frame
        admin_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=2)
        admin_frame.grid(row=1, column=0, sticky='nsew', padx=50, pady=20)
        
        # Create two columns for admin actions
        left_frame = tk.Frame(admin_frame, bg='white')
        left_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        
        right_frame = tk.Frame(admin_frame, bg='white')
        right_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Left column actions
        tk.Label(left_frame, text="Inventory Management", font=("Arial", 14, "bold"), bg='white').pack(pady=(0, 15))
        
        left_actions = [
            ("➕ Add Vegetable", self.add_vegetable, '#28a745'),
            ("🗑️ Remove Vegetable", self.remove_vegetable, '#dc3545'),
            ("📝 Update Stock", self.update_stock, '#ffc107'),
            ("💰 Update Price", self.update_price, '#17a2b8')
        ]
        
        for text, command, color in left_actions:
            tk.Button(
                left_frame, text=text, command=command,
                bg=color, fg='white',
                font=("Arial", 11), width=20, height=2,
                relief='flat', cursor='hand2'
            ).pack(pady=5)
        
        # Right column actions
        tk.Label(right_frame, text="Reports & Analytics", font=("Arial", 14, "bold"), bg='white').pack(pady=(0, 15))
        
        right_actions = [
            ("📊 View Statistics", self.view_statistics, '#6f42c1'),
            ("📈 Sales Report", self.show_sales_report, '#fd7e14'),
            ("🔄 Backup Data", self.backup_data, '#20c997'),
            ("⚠️ Clear All Data", self.clear_all_data, '#dc3545')
        ]
        
        for text, command, color in right_actions:
            tk.Button(
                right_frame, text=text, command=command,
                bg=color, fg='white',
                font=("Arial", 11), width=20, height=2,
                relief='flat', cursor='hand2'
            ).pack(pady=5)

    def add_vegetable(self):
        """Add new vegetable with enhanced validation"""
        # Create input dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Vegetable")
        dialog.geometry("300x400")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        tk.Label(dialog, text="Add New Vegetable", font=("Arial", 14, "bold"), bg='white').pack(pady=10)
        
        # Name input
        tk.Label(dialog, text="Name:", bg='white').pack()
        name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=name_var, width=20).pack(pady=5)
        
        # Price input
        tk.Label(dialog, text="Price (Rs/kg):", bg='white').pack()
        price_var = tk.StringVar()
        tk.Entry(dialog, textvariable=price_var, width=20).pack(pady=5)
        
        # Cost Price input
        tk.Label(dialog, text="Cost Price (Rs/kg):", bg='white').pack()
        cost_var = tk.StringVar()
        tk.Entry(dialog, textvariable=cost_var, width=20).pack(pady=5)


        # Stock input
        tk.Label(dialog, text="Stock (kg):", bg='white').pack()
        stock_var = tk.StringVar()
        tk.Entry(dialog, textvariable=stock_var, width=20).pack(pady=5)
        
        def save_vegetable():
            try:
                name = name_var.get().strip().lower()
                if not name:
                    messagebox.showerror("Error", "Please enter vegetable name")
                    return
                    
                if name in self.vegetables:
                    messagebox.showerror("Error", "Vegetable already exists!")
                    return
                
                price = float(price_var.get())
                stock = float(stock_var.get())
                cost=float(cost_var.get())
                
                if price <= 0:
                    messagebox.showerror("Error", "Price must be positive!")
                    return
                    
                if stock < 0:
                    messagebox.showerror("Error", "Stock cannot be negative!")
                    return
                
                if cost <= 0:
                   messagebox.showerror("Error", "Cost must be positive!")
                   return
                
                self.vegetables[name] = {"price": price, "stock": stock,"cost":cost}
                if self.save_data():
                    self.show_message(f"'{name.capitalize()}' added successfully!", "success")
                    dialog.destroy()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock!")
        
        tk.Button(dialog, text="Add", command=save_vegetable, bg='#28a745', fg='white').pack(pady=10)

    def remove_vegetable(self):
        """Remove vegetable with confirmation"""
        if not self.vegetables:
            self.show_message("No vegetables to remove!", "info")
            return
            
        # Create selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Vegetable")
        dialog.geometry("350x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select vegetable to remove:", font=("Arial", 12, "bold"), bg='white').pack(pady=10)
        
        # Create listbox for selection
        listbox_frame = tk.Frame(dialog, bg='white')
        listbox_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        listbox = tk.Listbox(listbox_frame, selectmode='single')
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate listbox
        for name, data in self.vegetables.items():
            listbox.insert(tk.END, f"{name.capitalize()} (Stock: {data['stock']:.2f}kg, Price: Rs.{data['price']:.2f}/kg)")
        
        def confirm_removal():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a vegetable!")
                return
                
            selected_item = listbox.get(selection[0])
            name = selected_item.split(" (")[0].lower()
            
            if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{name.capitalize()}'?"):
                del self.vegetables[name]
                if self.save_data():
                    self.show_message(f"'{name.capitalize()}' removed successfully!", "success")
                    dialog.destroy()
        
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Remove", command=confirm_removal, bg='#dc3545', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#6c757d', fg='white', width=10).pack(side='left', padx=5)

    def update_stock(self):
        """Update vegetable stock"""
        if not self.vegetables:
            self.show_message("No vegetables available!", "info")
            return
            
        self.create_update_dialog("stock", "Update Stock", "Enter new stock (kg):")

    def update_price(self):
        """Update vegetable price"""
        if not self.vegetables:
            self.show_message("No vegetables available!", "info")
            return
            
        self.create_update_dialog("price", "Update Price", "Enter new price (Rs/kg):")

    def create_update_dialog(self, field, title, prompt):
        """Create a generic update dialog for stock or price"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x350")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"{title}", font=("Arial", 14, "bold"), bg='white').pack(pady=10)
        
        # Selection frame
        selection_frame = tk.Frame(dialog, bg='white')
        selection_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(selection_frame, text="Select vegetable:", bg='white').pack()
        
        listbox = tk.Listbox(selection_frame, selectmode='single', height=8)
        scrollbar = ttk.Scrollbar(selection_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate listbox
        for name, data in self.vegetables.items():
            current_value = data[field]
            unit = "kg" if field == "stock" else "Rs/kg"
            listbox.insert(tk.END, f"{name.capitalize()} (Current: {current_value:.2f} {unit})")
        
        # Input frame
        input_frame = tk.Frame(dialog, bg='white')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text=prompt, bg='white').pack()
        value_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=value_var, width=20).pack(pady=5)
        
        def update_value():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a vegetable!")
                return
                
            try:
                selected_item = listbox.get(selection[0])
                name = selected_item.split(" (")[0].lower()
                new_value = float(value_var.get())
                
                if field == "price" and new_value <= 0:
                    messagebox.showerror("Error", "Price must be positive!")
                    return
                elif field == "stock" and new_value < 0:
                    messagebox.showerror("Error", "Stock cannot be negative!")
                    return
                
                self.vegetables[name][field] = new_value
                if self.save_data():
                    unit = "kg" if field == "stock" else "Rs/kg"
                    self.show_message(f"{field.capitalize()} updated for '{name.capitalize()}' to {new_value:.2f} {unit}!", "success")
                    dialog.destroy()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")
        
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Update", command=update_value, bg='#28a745', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#6c757d', fg='white', width=10).pack(side='left', padx=5)

    def view_statistics(self):
        """Display comprehensive business statistics"""
        self.clear_content()
        
        content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Main stats frame
        stats_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=2)
        stats_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        
        tk.Label(
            stats_frame,
            text="📊 Business Statistics & Analytics",
            font=("Arial", 16, "bold"),
            bg='white', fg='#2c3e50'
        ).pack(pady=20)
        
        # Calculate comprehensive statistics
        total_revenue = sum(order.get("amount", 0) for order in self.orders)
        total_profit = sum(order.get("profit", 0) for order in self.orders)
        total_orders = len(self.orders)
        total_vegetables = len(self.vegetables)
        total_stock_value = sum(veg["price"] * veg["stock"] for veg in self.vegetables.values())
        
        # Average order value
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Most popular vegetable
        vegetable_sales = {}
        for order in self.orders:
            veg_name = order.get("name", "")
            vegetable_sales[veg_name] = vegetable_sales.get(veg_name, 0) + 1
        
        most_popular = max(vegetable_sales.items(), key=lambda x: x[1]) if vegetable_sales else ("None", 0)
        
        # Low stock items
        low_stock_items = [name for name, data in self.vegetables.items() if data["stock"] < 5]
        
        # Create statistics display
        stats_container = tk.Frame(stats_frame, bg='white')
        stats_container.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Financial Stats
        financial_frame = tk.LabelFrame(stats_container, text="💰 Financial Overview", font=("Arial", 12, "bold"), bg='white')
        financial_frame.pack(fill='x', pady=10)
        
        financial_stats = [
            ("Total Revenue", f"Rs. {total_revenue:.2f}"),
            ("Average Order Value", f"Rs. {avg_order_value:.2f}"),
            ("Current Stock Value", f"Rs. {total_stock_value:.2f}"),
            ("Total Profit", f"Rs. {total_profit:.2f}")

        ]
        
        for i, (label, value) in enumerate(financial_stats):
            row_frame = tk.Frame(financial_frame, bg='white')
            row_frame.pack(fill='x', padx=10, pady=5)
            tk.Label(row_frame, text=f"{label}:", font=("Arial", 11), bg='white').pack(side='left')
            tk.Label(row_frame, text=value, font=("Arial", 11, "bold"), bg='white', fg='#27ae60').pack(side='right')
        
        # Inventory Stats
        inventory_frame = tk.LabelFrame(stats_container, text="📦 Inventory Overview", font=("Arial", 12, "bold"), bg='white')
        inventory_frame.pack(fill='x', pady=10)
        
        inventory_stats = [
            ("Total Vegetables", str(total_vegetables)),
            ("Total Orders Placed", str(total_orders)),
            ("Most Popular Item", f"{most_popular[0].capitalize()} ({most_popular[1]} orders)"),
            ("Low Stock Alerts", str(len(low_stock_items)))
        ]
        
        for label, value in inventory_stats:
            row_frame = tk.Frame(inventory_frame, bg='white')
            row_frame.pack(fill='x', padx=10, pady=5)
            tk.Label(row_frame, text=f"{label}:", font=("Arial", 11), bg='white').pack(side='left')
            color = '#e74c3c' if 'Low Stock' in label and len(low_stock_items) > 0 else '#3498db'
            tk.Label(row_frame, text=value, font=("Arial", 11, "bold"), bg='white', fg=color).pack(side='right')
        
        # Low stock warning
        if low_stock_items:
            warning_frame = tk.LabelFrame(stats_container, text="⚠️ Low Stock Alert", font=("Arial", 12, "bold"), bg='white', fg='red')
            warning_frame.pack(fill='x', pady=10)
            
            warning_text = "Low stock items: " + ", ".join([item.capitalize() for item in low_stock_items])
            tk.Label(warning_frame, text=warning_text, font=("Arial", 10), bg='white', fg='red', wraplength=400).pack(padx=10, pady=5)

    def show_sales_report(self):
      """Show detailed sales report"""
      self.clear_content()

      content_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
      content_frame.grid(row=1, column=0, sticky='nsew')
      content_frame.grid_rowconfigure(1, weight=1)
      content_frame.grid_columnconfigure(0, weight=1)

      tk.Label(
        content_frame,
        text="📈 Sales Report",
        font=("Arial", 16, "bold"),
        bg='#f8f9fa', fg='#2c3e50'
      ).grid(row=0, column=0, pady=15)

      report_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
      report_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
      report_frame.grid_rowconfigure(0, weight=1)
      report_frame.grid_columnconfigure(0, weight=1)

    # Calculate sales data
      vegetable_sales = {}
      for order in self.orders:
        veg_name = order.get("name", "")
        amount = order.get("amount", 0)
        profit = order.get("profit", 0)

        # Get cost per kg from vegetable database
        cost_per_kg = self.vegetables.get(veg_name, {}).get("cost", 0)

        # Convert quantity string like "2kg" or "500g" to float in kg
        quantity_str = order.get("quantity", "0kg").lower()
        if quantity_str.endswith("kg"):
            quantity = float(quantity_str.replace("kg", ""))
        elif quantity_str.endswith("g"):
            quantity = float(quantity_str.replace("g", "")) / 1000
        else:
            quantity = 0

        if veg_name in vegetable_sales:
            vegetable_sales[veg_name]["orders"] += 1
            vegetable_sales[veg_name]["quantity"] += quantity
            vegetable_sales[veg_name]["revenue"] += amount
            vegetable_sales[veg_name]["profit"] += profit
        else:
            vegetable_sales[veg_name] = {
                "orders": 1,
                "quantity": quantity,
                "revenue": amount,
                "profit": profit,
                "cost": cost_per_kg
            }

    # Create treeview for sales report
      columns = ("Vegetable", "Cost (Rs/kg)", "Quantity (kg)", "Profit (Rs)", "revenue","avg_revenue")
      tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=15)

      for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

      scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=tree.yview)
      tree.configure(yscrollcommand=scrollbar.set)

      tree.grid(row=0, column=0, sticky='nsew')
      scrollbar.grid(row=0, column=1, sticky='ns')

    # Populate data
      if vegetable_sales:
         for veg_name, data in sorted(vegetable_sales.items(), key=lambda x: x[1]["revenue"], reverse=True):
            avg_value = data["revenue"] / data["orders"] if data["orders"] > 0 else 0
            tree.insert("", "end", values=(
                veg_name.capitalize(),
                f"{data['cost']:.2f}",
                f"{data['quantity']:.2f}",
                f"{data['profit']:.2f}",
                f"{data['revenue']:.2f}",
                f"{avg_value:.2f}"
            ))
      else:
        tree.insert("", "end", values=("No sales data available", "", "", "", ""))


    def backup_data(self):
        """Create a backup of the data"""
        try:
            backup_filename = f"vegetable_market_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            data = {
                "vegetables": self.vegetables,
                "orders": self.orders,
                "backup_date": datetime.now().isoformat()
            }
            
            with open(backup_filename, "w") as file:
                json.dump(data, file, indent=4)
            
            self.show_message(f"Data backed up successfully to {backup_filename}", "success")
        except Exception as e:
            self.show_message(f"Backup failed: {e}", "error")

    def clear_all_data(self):
        """Clear all data with confirmation"""
        if messagebox.askyesno("Confirm Clear Data", 
                              "This will delete ALL vegetables and orders permanently!\n\nAre you absolutely sure?",
                              icon="warning"):
            if messagebox.askyesno("Final Confirmation", 
                                  "This action cannot be undone!\n\nProceed with clearing all data?"):
                self.vegetables = {}
                self.orders = []
                if self.save_data():
                    self.show_message("All data cleared successfully!", "success")
                    self.show_main_menu()  # Return to main menu

    def show_message(self, message, msg_type="info"):
        """Show message with appropriate styling"""
        if msg_type == "error":
            messagebox.showerror("Error", message)
        elif msg_type == "success":
            messagebox.showinfo("Success", message)
        else:
            messagebox.showinfo("Information", message)

    def sort_treeview(self, tree, col):
        """Sort treeview by column"""
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        # Try to sort numerically if possible
        try:
            data.sort(key=lambda x: float(x[0].replace('Rs. ', '').replace('kg', '').strip()))
        except (ValueError, AttributeError):
            data.sort()
        
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)

    def confirm_exit(self):
        """Confirm before exiting"""
        if messagebox.askyesno("Exit Application", "Are you sure you want to exit?"):
            self.root.quit()

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")

# Main execution
if __name__ == "__main__":
    try:
        app = VegetableMarket()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")