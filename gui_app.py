import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# --- 1. SETUP & DATABASE CONNECTION ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123", # ⚠️ Change this to your actual MySQL password
        database="courier_db"
    )
    cursor = db.cursor()
except Exception as e:
    messagebox.showerror("Database Error", f"Connection failed: {e}")
    exit()

# --- 2. ADMIN FUNCTIONS ---
def open_admin_dashboard():
    admin_win = ctk.CTkToplevel(root)
    admin_win.title("Admin Dashboard - Full Access")
    admin_win.geometry("650x600")
    
    # --- LOGOUT HEADER ---
    def logout_admin():
        admin_win.destroy() 
        user_ent.delete(0, 'end') 
        pass_ent.delete(0, 'end') 
        root.deiconify() 
        
    admin_win.protocol("WM_DELETE_WINDOW", logout_admin)

    header = ctk.CTkFrame(admin_win, fg_color="transparent")
    header.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(header, text="🛡️ Admin Dashboard", font=("Arial", 20, "bold")).pack(side="left")
    ctk.CTkButton(header, text="Logout", width=80, fg_color="darkred", hover_color="red", command=logout_admin).pack(side="right")

    tabs = ctk.CTkTabview(admin_win)
    tabs.pack(fill="both", expand=True, padx=10, pady=5)
    
    tab_add_cust = tabs.add("Add Customer")
    tab_edit_cust = tabs.add("Edit/Delete Customer")
    tab_shipment = tabs.add("Update Shipment")
    tab_complaint = tabs.add("Manage Complaints")

    # ==========================================
    # TAB 1: ADD CUSTOMER (CREATE)
    # ==========================================
    scroll_add = ctk.CTkScrollableFrame(tab_add_cust, width=400, height=300)
    scroll_add.pack(pady=5, fill="both", expand=True)

    ctk.CTkLabel(scroll_add, text="Name:").pack()
    name_ent = ctk.CTkEntry(scroll_add)
    name_ent.pack(pady=2)

    ctk.CTkLabel(scroll_add, text="Email:").pack()
    email_ent = ctk.CTkEntry(scroll_add)
    email_ent.pack(pady=2)

    ctk.CTkLabel(scroll_add, text="Phone:").pack()
    phone_ent = ctk.CTkEntry(scroll_add)
    phone_ent.pack(pady=2)
    
    ctk.CTkLabel(scroll_add, text="Street Address:").pack()
    street_ent = ctk.CTkEntry(scroll_add)
    street_ent.pack(pady=2)

    ctk.CTkLabel(scroll_add, text="City:").pack()
    city_ent = ctk.CTkEntry(scroll_add)
    city_ent.pack(pady=2)

    def save_customer():
        cursor.execute("SELECT MAX(cust_id) FROM Customer")
        max_id = cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1
        
        try:
            query = "INSERT INTO Customer (cust_id, name, email, phone, street, city, reg_date) VALUES (%s, %s, %s, %s, %s, %s, CURDATE())"
            values = (new_id, name_ent.get(), email_ent.get(), phone_ent.get(), street_ent.get(), city_ent.get())
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", f"Customer Added! Assigned ID: {new_id}")
            for ent in [name_ent, email_ent, phone_ent, street_ent, city_ent]: 
                ent.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(tab_add_cust, text="Save Customer", command=save_customer).pack(pady=10)


    # ==========================================
    # TAB 2: EDIT / DELETE CUSTOMER (READ, UPDATE, DELETE)
    # ==========================================
    search_frame = ctk.CTkFrame(tab_edit_cust)
    search_frame.pack(pady=5, fill="x")
    
    ctk.CTkLabel(search_frame, text="Customer ID:").pack(side="left", padx=5)
    search_id_ent = ctk.CTkEntry(search_frame, width=100)
    search_id_ent.pack(side="left", padx=5)

    edit_name = ctk.StringVar()
    edit_phone = ctk.StringVar()
    edit_city = ctk.StringVar()

    def fetch_customer():
        try:
            query = "SELECT name, phone, city FROM Customer WHERE cust_id=%s"
            cursor.execute(query, (search_id_ent.get(),))
            res = cursor.fetchone()
            if res:
                edit_name.set(res[0])
                edit_phone.set(res[1])
                edit_city.set(res[2])
            else:
                messagebox.showerror("Not Found", "Customer ID does not exist.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(search_frame, text="Fetch", command=fetch_customer).pack(side="left", padx=5)

    edit_form = ctk.CTkFrame(tab_edit_cust)
    edit_form.pack(pady=10, fill="both", expand=True)

    ctk.CTkLabel(edit_form, text="Name:").pack()
    ctk.CTkEntry(edit_form, textvariable=edit_name).pack(pady=5)

    ctk.CTkLabel(edit_form, text="Phone:").pack()
    ctk.CTkEntry(edit_form, textvariable=edit_phone).pack(pady=5)

    ctk.CTkLabel(edit_form, text="City:").pack()
    ctk.CTkEntry(edit_form, textvariable=edit_city).pack(pady=5)

    def update_customer():
        try:
            query = "UPDATE Customer SET name=%s, phone=%s, city=%s WHERE cust_id=%s"
            cursor.execute(query, (edit_name.get(), edit_phone.get(), edit_city.get(), search_id_ent.get()))
            db.commit()
            messagebox.showinfo("Success", "Customer details updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_customer():
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?")
        if confirm:
            try:
                cursor.execute("DELETE FROM Customer WHERE cust_id=%s", (search_id_ent.get(),))
                db.commit()
                messagebox.showinfo("Deleted", "Customer deleted successfully.")
                edit_name.set(""); edit_phone.set(""); edit_city.set(""); search_id_ent.delete(0, 'end')
            except mysql.connector.IntegrityError:
                messagebox.showerror("Constraint Error", "Cannot delete: This customer has active packages/shipments linked to them.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    btn_frame1 = ctk.CTkFrame(edit_form, fg_color="transparent")
    btn_frame1.pack(pady=10)
    ctk.CTkButton(btn_frame1, text="Update Data", command=update_customer).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame1, text="Delete Customer", fg_color="darkred", hover_color="red", command=delete_customer).pack(side="right", padx=10)


    # ==========================================
    # TAB 3: UPDATE SHIPMENT (UPDATE)
    # ==========================================
    ctk.CTkLabel(tab_shipment, text="Tracking Number:").pack(pady=10)
    track_ent = ctk.CTkEntry(tab_shipment, placeholder_text="e.g., TRK101")
    track_ent.pack(pady=5)
    
    status_var = ctk.StringVar(value="Delivered")
    ctk.CTkOptionMenu(tab_shipment, variable=status_var, values=["Pending", "In Transit", "Delivered"]).pack(pady=10)

    def update_status():
        try:
            query = "UPDATE Shipment SET delivery_status=%s WHERE tracking_no=%s"
            cursor.execute(query, (status_var.get(), track_ent.get()))
            db.commit()
            messagebox.showinfo("Success", "Shipment Status Updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(tab_shipment, text="Update Status", command=update_status).pack(pady=15)


    # ==========================================
    # TAB 4: MANAGE COMPLAINTS (READ, UPDATE, DELETE)
    # ==========================================
    comp_search_frame = ctk.CTkFrame(tab_complaint)
    comp_search_frame.pack(pady=5, fill="x")
    
    ctk.CTkLabel(comp_search_frame, text="Complaint ID:").pack(side="left", padx=5)
    comp_id_ent = ctk.CTkEntry(comp_search_frame, width=100)
    comp_id_ent.pack(side="left", padx=5)

    comp_desc = ctk.StringVar()
    comp_res_status = ctk.StringVar(value="Pending")

    def fetch_complaint():
        try:
            query = "SELECT description, resolution_status FROM Complaint WHERE complaint_id=%s"
            cursor.execute(query, (comp_id_ent.get(),))
            res = cursor.fetchone()
            if res:
                comp_desc.set(res[0])
                comp_res_status.set(res[1])
            else:
                messagebox.showerror("Not Found", "Complaint ID does not exist.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(comp_search_frame, text="Fetch Ticket", command=fetch_complaint).pack(side="left", padx=5)

    comp_form = ctk.CTkFrame(tab_complaint)
    comp_form.pack(pady=10, fill="both", expand=True)

    ctk.CTkLabel(comp_form, text="Issue Description:").pack()
    ctk.CTkEntry(comp_form, textvariable=comp_desc, state="disabled", width=300).pack(pady=5)

    ctk.CTkLabel(comp_form, text="Resolution Status:").pack()
    ctk.CTkOptionMenu(comp_form, variable=comp_res_status, values=["Pending", "Resolved", "Closed"]).pack(pady=5)

    def update_complaint():
        try:
            # Stamp today's date on it
            query = "UPDATE Complaint SET resolution_status=%s, resolution_date=CURDATE() WHERE complaint_id=%s"
            cursor.execute(query, (comp_res_status.get(), comp_id_ent.get()))
            db.commit()
            messagebox.showinfo("Success", "Complaint ticket updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_complaint():
        confirm = messagebox.askyesno("Confirm Delete", "Delete this complaint ticket entirely?")
        if confirm:
            try:
                cursor.execute("DELETE FROM Complaint WHERE complaint_id=%s", (comp_id_ent.get(),))
                db.commit()
                messagebox.showinfo("Deleted", "Complaint removed from system.")
                comp_desc.set(""); comp_id_ent.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", str(e))

    btn_frame2 = ctk.CTkFrame(comp_form, fg_color="transparent")
    btn_frame2.pack(pady=15)
    ctk.CTkButton(btn_frame2, text="Update Ticket", command=update_complaint).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame2, text="Delete Ticket", fg_color="darkred", hover_color="red", command=delete_complaint).pack(side="right", padx=10)


# --- 3. CUSTOMER FUNCTIONS ---
def open_customer_dashboard(cust_id):
    cust_win = ctk.CTkToplevel(root)
    cust_win.title("Customer Portal")
    cust_win.geometry("500x480")
    
    # --- LOGOUT HEADER ---
    def logout_cust():
        cust_win.destroy()
        user_ent.delete(0, 'end')
        pass_ent.delete(0, 'end')
        root.deiconify()
        
    cust_win.protocol("WM_DELETE_WINDOW", logout_cust)

    header = ctk.CTkFrame(cust_win, fg_color="transparent")
    header.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(header, text="📦 Customer Portal", font=("Arial", 20, "bold")).pack(side="left")
    ctk.CTkButton(header, text="Logout", width=80, fg_color="darkred", hover_color="red", command=logout_cust).pack(side="right")

    # Tabs for the Customer Portal
    tabs = ctk.CTkTabview(cust_win)
    tabs.pack(fill="both", expand=True, padx=10, pady=5)
    
    tab_track = tabs.add("Track Package")
    tab_complain = tabs.add("File Complaint")

    # ==========================================
    # TAB 1: TRACK PACKAGE (READ)
    # ==========================================
    ctk.CTkLabel(tab_track, text="Track Your Package", font=("Arial", 16, "bold")).pack(pady=15)
    
    track_ent = ctk.CTkEntry(tab_track, placeholder_text="Enter Tracking No (e.g., TRK101)", width=250)
    track_ent.pack(pady=10)

    def track_package():
        query = "SELECT delivery_status, expected_date FROM Shipment WHERE tracking_no=%s"
        cursor.execute(query, (track_ent.get(),))
        result = cursor.fetchone()
        
        if result:
            messagebox.showinfo("Tracking Details", f"Status: {result[0]}\nExpected Delivery: {result[1]}")
        else:
            messagebox.showerror("Error", "Invalid Tracking Number")

    ctk.CTkButton(tab_track, text="Search Package", command=track_package).pack(pady=15)

    # ==========================================
    # TAB 2: FILE COMPLAINT (CREATE)
    # ==========================================
    ctk.CTkLabel(tab_complain, text="Report an Issue", font=("Arial", 16, "bold")).pack(pady=10)

    c_track_ent = ctk.CTkEntry(tab_complain, placeholder_text="Tracking Number", width=250)
    c_track_ent.pack(pady=5)

    comp_type_var = ctk.StringVar(value="Delay")
    ctk.CTkOptionMenu(tab_complain, variable=comp_type_var, values=["Delay", "Damage", "Lost", "Error", "Other"], width=250).pack(pady=5)

    c_desc_ent = ctk.CTkEntry(tab_complain, placeholder_text="Brief description of the issue", width=250)
    c_desc_ent.pack(pady=5)

    def submit_complaint():
        trk = c_track_ent.get()
        desc = c_desc_ent.get()
        ctype = comp_type_var.get()

        if not trk or not desc:
            messagebox.showwarning("Missing Info", "Please provide a tracking number and description.")
            return

        try:
            # 1. Verify the tracking number exists and get shipment_id
            cursor.execute("SELECT shipment_id FROM Shipment WHERE tracking_no=%s", (trk,))
            s_res = cursor.fetchone()
            if not s_res:
                messagebox.showerror("Not Found", "Tracking number does not exist.")
                return

            shipment_id = s_res[0]

            # 2. Generate new complaint_id
            cursor.execute("SELECT MAX(complaint_id) FROM Complaint")
            m_id = cursor.fetchone()[0]
            new_id = 1 if m_id is None else m_id + 1

            # 3. Insert complaint
            query = """INSERT INTO Complaint 
                       (complaint_id, description, type, status, complaint_date, resolution_status, cust_id, shipment_id) 
                       VALUES (%s, %s, %s, 'Open', CURDATE(), 'Pending', %s, %s)"""
            cursor.execute(query, (new_id, desc, ctype, cust_id, shipment_id))
            db.commit()

            messagebox.showinfo("Success", f"Complaint submitted successfully!\nYour Ticket ID is: {new_id}")
            
            c_track_ent.delete(0, 'end')
            c_desc_ent.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(tab_complain, text="Submit Complaint", fg_color="darkred", hover_color="red", command=submit_complaint).pack(pady=15)

    # Status text at the bottom
    ctk.CTkLabel(cust_win, text=f"Logged in securely as Customer ID: {cust_id}", text_color="gray").pack(side="bottom", pady=10)


# --- 4. LOGIN SYSTEM ---
def login():
    user = user_ent.get()
    pwd = pass_ent.get()
    role = role_var.get()

    query = "SELECT cust_id FROM System_Users WHERE username=%s AND password_hash=%s AND role=%s"
    cursor.execute(query, (user, pwd, role))
    result = cursor.fetchone()

    if result:
        root.withdraw() 
        if role == "Admin": 
            open_admin_dashboard()
        else: 
            open_customer_dashboard(result[0])
    else:
        messagebox.showerror("Login Failed", "Invalid credentials or incorrect role selected.")

# --- 5. MAIN WINDOW UI (LOGIN SCREEN) ---
root = ctk.CTk()
root.title("System Login")
root.geometry("350x450")

ctk.CTkLabel(root, text="Courier System", font=("Arial", 22, "bold")).pack(pady=(40, 30))

user_ent = ctk.CTkEntry(root, placeholder_text="Username", width=200)
user_ent.pack(pady=10)

pass_ent = ctk.CTkEntry(root, placeholder_text="Password", show="*", width=200)
pass_ent.pack(pady=10)

role_var = ctk.StringVar(value="Admin")
ctk.CTkOptionMenu(root, variable=role_var, values=["Admin", "Customer"], width=200).pack(pady=10)

btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=30)

ctk.CTkButton(btn_frame, text="Login", command=login, width=200).pack(pady=5)
ctk.CTkButton(btn_frame, text="Exit System", fg_color="darkred", hover_color="red", command=root.destroy, width=200).pack(pady=5)

root.mainloop()