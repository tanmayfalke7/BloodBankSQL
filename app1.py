import streamlit as st
import mysql.connector
import pandas as pd

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1", port=3306,
        user="root",  # Change this
        password="Tanmaychasql@123",  # Change this
        database="blood"
    )

# Function to execute queries
def execute_query(query, values=None, fetch=False):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    
    if fetch:
        result = cursor.fetchall()
    else:
        conn.commit()
        result = None
    
    cursor.close()
    conn.close()
    return result

# Streamlit UI
st.title("🩸 Blood Bank Management System")

menu = st.sidebar.selectbox("Navigation", ["Employees", "Donors", "Hospitals", "Blood Storage", "Orders", "Supply"])

# Employee Management
if menu == "Employees":
    st.subheader("Manage Employees")
    
    # Display employees
    employees = execute_query("SELECT * FROM Employee", fetch=True)
    st.dataframe(pd.DataFrame(employees))

    # Add new employee
    with st.form("add_employee"):
        emp_name = st.text_input("Employee Name")
        email = st.text_input("Email")
        salary = st.number_input("Salary", min_value=0)
        designation = st.text_input("Designation")
        joining_date = st.date_input("Joining Date")
        bb_contact = st.text_input("Blood Bank Contact")
        bb_id = st.number_input("Blood Bank ID", min_value=1)
        bb_address = st.text_area("Blood Bank Address")
        
        submit = st.form_submit_button("Add Employee")
        
        if submit:
            execute_query(
                "INSERT INTO Employee (Emp_name, Email, Salary, Designation, Joining_date, BB_contact, BB_id, BB_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (emp_name, email, salary, designation, joining_date, bb_contact, bb_id, bb_address)
            )
            st.success("Employee added successfully!")

# Donor Management
elif menu == "Donors":
    st.subheader("Manage Donors")
    
    donors = execute_query("SELECT * FROM Donor", fetch=True)
    st.dataframe(pd.DataFrame(donors))

    with st.form("add_donor"):
        name = st.text_input("Donor Name")
        contact = st.text_input("Contact")
        time = st.date_input("Donation Time")
        blood_grp = st.selectbox("Blood Group", ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
        address = st.text_area("Address")
        
        submit = st.form_submit_button("Add Donor")
        
        if submit:
            execute_query(
                "INSERT INTO Donor (Dona_name, Dona_contact, Dona_time, Blood_grp, Dona_addr) VALUES (%s, %s, %s, %s, %s)",
                (name, contact, time, blood_grp, address)
            )
            st.success("Donor added successfully!")

# Hospital Management
elif menu == "Hospitals":
    st.subheader("Manage Hospitals")
    
    hospitals = execute_query("SELECT * FROM Hospital", fetch=True)
    st.dataframe(pd.DataFrame(hospitals))

    with st.form("add_hospital"):
        name = st.text_input("Hospital Name")
        contact = st.text_input("Contact")
        address = st.text_area("Address")
        blood_grp = st.selectbox("Blood Group", ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
        units = st.number_input("Units Required", min_value=1)
        
        submit = st.form_submit_button("Add Hospital")
        
        if submit:
            execute_query(
                "INSERT INTO Hospital (Hospital_name, Hospital_contact, Hospital_address, Blood_grp, Units_required) VALUES (%s, %s, %s, %s, %s)",
                (name, contact, address, blood_grp, units)
            )
            st.success("Hospital added successfully!")

# Blood Storage
elif menu == "Blood Storage":
    st.subheader("Manage Blood Storage")
    
    storage = execute_query("SELECT * FROM Storage_House", fetch=True)
    st.dataframe(pd.DataFrame(storage))

    with st.form("add_storage"):
        store_keeper = st.text_input("Store Keeper Name")
        total_units = st.number_input("Total Units", min_value=1)
        
        submit = st.form_submit_button("Add Storage")
        
        if submit:
            execute_query(
                "INSERT INTO Storage_House (Store_keeper, Total_units) VALUES (%s, %s)",
                (store_keeper, total_units)
            )
            st.success("Storage added successfully!")

    if st.button("Delete Storage Entry"):
        execute_query("DELETE FROM Storage_House WHERE Store_keeper = %s LIMIT 1", (store_keeper,))
        st.warning("Storage entry deleted successfully!")    

# Order Management
elif menu == "Orders":
    st.subheader("Manage Orders")
    
    orders = execute_query("SELECT * FROM Orders", fetch=True)
    st.dataframe(pd.DataFrame(orders))

    with st.form("add_order"):
        hospital_id = st.number_input("Hospital ID", min_value=1)
        blood_grp = st.selectbox("Blood Group", ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
        quantity = st.number_input("Quantity", min_value=1)
        
        submit = st.form_submit_button("Add Order")
        
        if submit:
            execute_query(
                "INSERT INTO Orders (Hospital_id, Blood_grp, Quantity) VALUES (%s, %s, %s)",
                (hospital_id, blood_grp, quantity)
            )
            st.success("Order placed successfully!")

# Supply Management
elif menu == "Supply":
    st.subheader("Manage Supply")

    supply = execute_query("SELECT * FROM Supply", fetch=True)
    st.dataframe(pd.DataFrame(supply))

    with st.form("add_supply"):
        order_no = st.number_input("Order No", min_value=1)
        storage_id = st.number_input("Storage ID", min_value=1)
        qty_sent = st.number_input("Quantity Sent", min_value=1)
        
        submit = st.form_submit_button("Add Supply Record")
        
        if submit:
            execute_query(
                "INSERT INTO Supply (Order_no, Storage_id, Qty_sent) VALUES (%s, %s, %s)",
                (order_no, storage_id, qty_sent)
            )
            st.success("Supply record added successfully!")
