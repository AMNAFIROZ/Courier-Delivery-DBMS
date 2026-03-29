import mysql.connector
import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123", # Change this to your actual password
    database="courier_db"
)
cursor = db.cursor()

def view_customers():
    print("\n--- Registered Customers ---")
    cursor.execute("SELECT cust_id, name, phone, city, email FROM Customer")
    results = cursor.fetchall()
    
    if results:
        print(f"{'ID':<4} | {'Name':<15} | {'Phone':<12} | {'City':<15} | {'Email'}")
        print("-" * 75)
        for row in results:
            print(f"{row[0]:<4} | {row[1]:<15} | {row[2]:<12} | {row[3]:<15} | {row[4]}")
    else:
        print("No customers found in the database.")

def add_customer_db(name, email, phone, city):
    cursor.execute("SELECT MAX(cust_id) FROM Customer")
    result = cursor.fetchone()[0]
    new_id = 1 if result is None else result + 1

    # FIXED: Added reg_date using MySQL's CURDATE()
    query = """
    INSERT INTO Customer (cust_id, name, email, phone, city, reg_date)
    VALUES (%s,%s,%s,%s,%s, CURDATE())
    """
    cursor.execute(query, (new_id, name, email, phone, city))
    db.commit()
    return new_id

# FIXED: Added the missing CLI wrapper function
def add_customer():
    print("\n--- Add New Customer ---")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    city = input("Enter City: ")
    
    new_id = add_customer_db(name, email, phone, city)
    print(f"\n✅ SUCCESS: Customer added with ID {new_id}")

def track_shipment():
    tracking = input("Enter tracking number: ")
    query = "SELECT * FROM Shipment WHERE tracking_no = %s"
    cursor.execute(query, (tracking,))
    result = cursor.fetchone()

    if result:
        result = list(result)
        for i in range(len(result)):
            if hasattr(result[i], "strftime"):
                result[i] = result[i].strftime("%Y-%m-%d")

        print("\n" + "="*45)
        print(f"{'📦 SHIPMENT TRACKING DETAILS':^45}")
        print("="*45)
        print(f"{'Tracking No':<15}: {result[1]}")
        print(f"{'Current Status':<15}: [{result[4].upper()}]")
        print("-" * 45)
        print(f"{'Send Date':<15}: {result[2]}")
        print(f"{'Expected Date':<15}: {result[5]}")
        
        delivery = result[3] if result[3] else "Not yet delivered"
        print(f"{'Delivery Date':<15}: {delivery}")
        print("="*45)
    else:
        print("Shipment not found")

def view_pending_complaints():
    print("\n--- Pending Complaints ---")
    query = "SELECT complaint_id, description, type, complaint_date FROM Complaint WHERE resolution_status = 'Pending'"
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        for row in results:
            date_str = row[3].strftime("%Y-%m-%d") if hasattr(row[3], "strftime") else row[3]
            print(f"Complaint ID : {row[0]}\nIssue Type   : {row[2]}\nDate Filed   : {date_str}\nDescription  : {row[1]}")
            print("-" * 50)
    else:
        print("No pending complaints. All good!")

def view_all_shipments():
    print("\n--- All Current Shipments ---")
    query = """
    SELECT s.tracking_no, c.name, p.description, s.delivery_status, s.expected_date
    FROM Shipment s
    JOIN Package p ON s.package_id = p.package_id
    JOIN Customer c ON p.cust_id = c.cust_id
    ORDER BY s.shipment_id DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        print(f"{'Tracking No':<15} | {'Customer':<15} | {'Package':<20} | {'Status':<15} | {'Expected'}")
        print("-" * 85)
        for row in results:
            date_str = row[4].strftime("%Y-%m-%d") if hasattr(row[4], "strftime") and row[4] else "N/A"
            print(f"{row[0]:<15} | {row[1]:<15} | {row[2]:<20} | {row[3]:<15} | {date_str}")
    else:
        print("No shipments found in the system.")

def view_active_agents():
    print("\n--- Active Agent Dispatch ---")
    query = """
    SELECT d.name AS agent, v.plate_no, v.type, u.route 
    FROM Uses u
    JOIN Delivery_Agent d ON u.agent_id = d.agent_id
    JOIN Vehicle v ON u.vehicle_id = v.vehicle_id
    WHERE u.status = 'Active'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        print(f"{'Agent Name':<12} | {'Vehicle Details':<20} | {'Assigned Route'}")
        print("-" * 60)
        for row in results:
            vehicle_info = f"{row[2]} ({row[1]})"
            print(f"{row[0]:<12} | {vehicle_info:<20} | {row[3]}")
    else:
        print("No active agents currently on dispatch.")

def view_payment_history():
    print("\n--- Payment History & Revenue ---")
    query = """
    SELECT p.payment_id, c.name, p.amount, p.payment_method, p.status, p.payment_date
    FROM Payment p
    JOIN Customer c ON p.cust_id = c.cust_id
    ORDER BY p.payment_id ASC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        print(f"{'ID':<4} | {'Customer':<10} | {'Amount':<8} | {'Method':<8} | {'Status':<10} | {'Date'}")
        print("-" * 65)
        for row in results:
            date_str = row[5].strftime("%Y-%m-%d") if hasattr(row[5], "strftime") else row[5]
            print(f"{row[0]:<4} | {row[1]:<10} | ₹{row[2]:<7} | {row[3]:<8} | {row[4]:<10} | {date_str}")
    else:
        print("No payment records found.")

def view_branch_stats():
    print("\n--- Branch Operational Statistics ---")
    query = """
    SELECT b.branch_id, b.name, b.city, b.phone, 
           COUNT(DISTINCT a.agent_id) AS total_agents,
           COUNT(DISTINCT v.vehicle_id) AS total_vehicles
    FROM Branch b
    LEFT JOIN Delivery_Agent a ON b.branch_id = a.branch_id
    LEFT JOIN Vehicle v ON b.branch_id = v.branch_id
    GROUP BY b.branch_id, b.name, b.city, b.phone
    ORDER BY b.branch_id ASC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        print(f"{'ID':<3} | {'Branch Name':<15} | {'City':<10} | {'Phone':<12} | {'Agents':<6} | {'Vehicles'}")
        print("-" * 75)
        for row in results:
            print(f"{row[0]:<3} | {row[1]:<15} | {row[2]:<10} | {row[3]:<12} | {row[4]:<6} | {row[5]}")
    else:
        print("No branch records found.")

# FIXED: Returns both login success status AND the connected cust_id
def login_screen(expected_role):
    print("\n" + "="*45)
    print(f"🔒 {expected_role.upper()} LOGIN".center(45))
    print("="*45)
    
    attempts = 3
    while attempts > 0:
        username = input("Username : ")
        password = input("Password : ")

        query = "SELECT user_id, cust_id FROM System_Users WHERE username = %s AND password_hash = %s AND role = %s"
        cursor.execute(query, (username, password, expected_role))
        user = cursor.fetchone()

        if user:
            print(f"\n✅ Access Granted. Welcome to the {expected_role} Portal!")
            return True, user[1] # Returns (True, cust_id)
        else:
            attempts -= 1
            print(f"❌ Invalid credentials. Attempts remaining: {attempts}\n")
            
    print("🚨 Maximum attempts reached. Returning to main menu.")
    return False, None

def update_customer():
    print("\n--- Update Customer Details ---")
    cust_id = input("Enter the Customer ID to update: ")
    
    cursor.execute("SELECT name FROM Customer WHERE cust_id = %s", (cust_id,))
    if not cursor.fetchone():
        print("❌ Customer not found.")
        return

    print("Leave field blank to keep current value.")
    new_phone = input("Enter new phone number: ")
    new_city = input("Enter new city: ")
    
    try:
        if new_phone:
            cursor.execute("UPDATE Customer SET phone = %s WHERE cust_id = %s", (new_phone, cust_id))
        if new_city:
            cursor.execute("UPDATE Customer SET city = %s WHERE cust_id = %s", (new_city, cust_id))
            
        db.commit()
        print("\n✅ SUCCESS: Customer updated successfully!")
    except mysql.connector.Error as err:
        print(f"\n❌ DATABASE ERROR: {err}")
        db.rollback()

def delete_customer():
    print("\n--- Delete Customer ---")
    cust_id = input("Enter the Customer ID to delete: ")
    confirm = input(f"Are you sure you want to delete Customer {cust_id}? (y/n): ")
    
    if confirm.lower() == 'y':
        try:
            cursor.execute("DELETE FROM Customer WHERE cust_id = %s", (cust_id,))
            db.commit()
            print("\n✅ SUCCESS: Customer deleted.")
        except mysql.connector.Error:
            print(f"\n❌ CANNOT DELETE: This customer has active packages or shipments.")
            db.rollback()

def update_shipment_status():
    print("\n--- Update Shipment Status ---")
    tracking_no = input("Enter Tracking Number: ")

    cursor.execute("SELECT shipment_id FROM Shipment WHERE tracking_no = %s", (tracking_no,))
    if not cursor.fetchone():
        print("❌ Shipment not found.")
        return

    print("Select new status:\n1. Pending\n2. In Transit\n3. Delivered")
    status_choice = input("Choice: ")

    status_map = {'1': 'Pending', '2': 'In Transit', '3': 'Delivered'}
    new_status = status_map.get(status_choice)

    if not new_status:
        print("❌ Invalid choice.")
        return

    try:
        if new_status == 'Delivered':
            today = datetime.date.today().strftime("%Y-%m-%d")
            query = "UPDATE Shipment SET delivery_status = %s, delivery_date = %s WHERE tracking_no = %s"
            cursor.execute(query, (new_status, today, tracking_no))
        else:
            query = "UPDATE Shipment SET delivery_status = %s WHERE tracking_no = %s"
            cursor.execute(query, (new_status, tracking_no))
            
        db.commit()
        print(f"\n✅ SUCCESS: Shipment {tracking_no} marked as '{new_status}'.")
    except mysql.connector.Error as err:
        print(f"\n❌ DATABASE ERROR: {err}")
        db.rollback()

def resolve_complaint():
    print("\n--- Resolve Customer Complaint ---")
    view_pending_complaints() 
    
    comp_id = input("Enter Complaint ID to resolve (or press Enter to cancel): ")
    if not comp_id: return

    cursor.execute("SELECT resolution_status FROM Complaint WHERE complaint_id = %s", (comp_id,))
    result = cursor.fetchone()

    if not result:
        print("❌ Complaint not found.")
        return
    if result[0] == 'Resolved':
        print("⚠️ This complaint is already resolved.")
        return

    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        query = "UPDATE Complaint SET resolution_status = 'Resolved', resolution_date = %s, status = 'Closed' WHERE complaint_id = %s"
        cursor.execute(query, (today, comp_id))
        db.commit()
        print(f"\n✅ SUCCESS: Complaint ID {comp_id} has been resolved and closed.")
    except mysql.connector.Error as err:
        print(f"\n❌ DATABASE ERROR: {err}")
        db.rollback()

# FIXED: Now automatically uses the logged-in user's cust_id
def file_complaint(logged_in_cust_id):
    print("\n--- File a New Complaint ---")
    try:
        cust_id = logged_in_cust_id
        if not cust_id: # Fallback just in case
            cust_id = input("Enter your Customer ID: ")
            
        tracking_no = input("Enter your Tracking Number: ")
        
        cursor.execute("SELECT shipment_id FROM Shipment WHERE tracking_no = %s", (tracking_no,))
        ship_result = cursor.fetchone()
        
        if not ship_result:
            print("❌ Error: Tracking Number not found.")
            return
            
        shipment_id = ship_result[0]

        print("\nSelect Issue Type:\n1. Delay\n2. Damage\n3. Lost Package\n4. Other")
        type_choice = input("Choice: ")
        
        type_map = {'1': 'Delay', '2': 'Damage', '3': 'Lost', '4': 'Other'}
        comp_type = type_map.get(type_choice, 'Other')
        
        description = input("Enter a brief description of the issue: ")
        
        cursor.execute("SELECT MAX(complaint_id) FROM Complaint")
        result = cursor.fetchone()[0]
        new_id = 1 if result is None else result + 1
        comp_date = datetime.date.today().strftime("%Y-%m-%d")
        
        query = """
        INSERT INTO Complaint 
        (complaint_id, description, type, status, complaint_date, resolution_status, cust_id, shipment_id) 
        VALUES (%s, %s, %s, 'Open', %s, 'Pending', %s, %s)
        """
        cursor.execute(query, (new_id, description, comp_type, comp_date, cust_id, shipment_id))
        db.commit()
        
        print(f"\n✅ SUCCESS: Complaint filed. Your Ticket ID is: {new_id}")
    except mysql.connector.Error as err:
        print(f"\n❌ DATABASE ERROR: {err}")
        db.rollback()

# FIXED: Now automatically uses the logged-in user's cust_id
def view_my_shipments(logged_in_cust_id):
    print("\n" + "="*45)
    print(f"{'📦 MY SHIPMENTS DASHBOARD':^45}")
    print("="*45)
    
    cust_id = logged_in_cust_id
    if not cust_id:
        cust_id = input("Enter your Customer ID: ")

    query = """
    SELECT s.tracking_no, p.description, s.send_date, s.delivery_status, s.expected_date
    FROM Shipment s
    JOIN Package p ON s.package_id = p.package_id
    WHERE p.cust_id = %s
    ORDER BY s.shipment_id DESC
    """
    try:
        cursor.execute(query, (cust_id,))
        results = cursor.fetchall()

        if results:
            print(f"\n{'Tracking No':<15} | {'Package Item':<20} | {'Sent On':<12} | {'Status':<15} | {'Expected'}")
            print("-" * 80)
            for row in results:
                send_date = row[2].strftime("%Y-%m-%d") if hasattr(row[2], "strftime") and row[2] else "N/A"
                exp_date = row[4].strftime("%Y-%m-%d") if hasattr(row[4], "strftime") and row[4] else "N/A"
                print(f"{row[0]:<15} | {row[1]:<20} | {send_date:<12} | {row[3]:<15} | {exp_date}")
            print("-" * 80)
        else:
            print("\n❌ No shipments found for this account.")
    except mysql.connector.Error as err:
        print(f"\n❌ DATABASE ERROR: {err}")


# --- MENUS ---

def manage_customers_menu():
    while True:
        print("\n--- Manage Customers ---")
        print("1. View All Customers\n2. Add New Customer\n3. Update Customer Details\n4. Delete Customer\n5. Back")
        choice = input("Enter choice: ")
        if choice == '1': view_customers()
        elif choice == '2': add_customer()
        elif choice == '3': update_customer()
        elif choice == '4': delete_customer()
        elif choice == '5': break
        else: print("Invalid choice.")

def manage_operations_menu():
    while True:
        print("\n--- Manage Operations ---")
        print("1. View All Shipments\n2. Track Shipment\n3. Update Shipment Status\n4. View Agents\n5. View Pending Complaints\n6. Resolve Complaint\n7. Back")
        choice = input("Enter choice: ")
        if choice == '1': view_all_shipments()
        elif choice == '2': track_shipment()
        elif choice == '3': update_shipment_status()
        elif choice == '4': view_active_agents()
        elif choice == '5': view_pending_complaints()
        elif choice == '6': resolve_complaint()
        elif choice == '7': break
        else: print("Invalid choice.")

def admin_menu():
    while True:
        print("\n=== ADMIN DASHBOARD ===")
        print("1. Manage Customers\n2. Manage Operations\n3. View Reports\n4. Logout")
        choice = input("Enter choice: ")
        if choice == '1': manage_customers_menu() 
        elif choice == '2': manage_operations_menu() 
        elif choice == '3': 
            view_payment_history()
            view_branch_stats()
        elif choice == '4': break
        else: print("Invalid choice.")

def customer_menu(logged_in_cust_id):
    while True:
        print("\n=== CUSTOMER PORTAL ===")
        print("1. View My Shipments\n2. Track a Specific Shipment\n3. File a Complaint\n4. Logout")
        choice = input("Enter choice: ")
        if choice == '1': view_my_shipments(logged_in_cust_id)
        elif choice == '2': track_shipment()
        elif choice == '3': file_complaint(logged_in_cust_id)
        elif choice == '4': break
        else: print("Invalid choice.")

# --- MAIN ---
def main():
    while True:
        print("\n" + "="*50)
        print(f"{'🚚 COURIER MANAGEMENT SYSTEM':^50}")
        print("="*50)
        print("1. Admin Portal")
        print("2. Customer Portal")
        print("3. Exit System")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            success, _ = login_screen('Admin')
            if success: admin_menu()
        elif choice == '2':
            success, cust_id = login_screen('Customer')
            if success: customer_menu(cust_id)
        elif choice == '3':
            print("Shutting down system. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()