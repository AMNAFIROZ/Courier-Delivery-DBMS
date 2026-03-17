-- CUSTOMER TABLE
CREATE TABLE Customer (
    cust_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    city VARCHAR(50),
    street VARCHAR(100),
    pincode VARCHAR(10),
    state VARCHAR(50),
    reg_date DATE
);

-- BRANCH TABLE
CREATE TABLE Branch (
    branch_id INT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    city VARCHAR(50),
    phone VARCHAR(15)
);

-- DELIVERY AGENT TABLE
CREATE TABLE Delivery_Agent (
    agent_id INT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    license_no VARCHAR(50),
    status VARCHAR(50),
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- VEHICLE TABLE
CREATE TABLE Vehicle (
    vehicle_id INT PRIMARY KEY,
    plate_no VARCHAR(20),
    capacity INT,
    type VARCHAR(50),
    status VARCHAR(50),
    branch_id INT,
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- PACKAGE TABLE (UPDATED)
CREATE TABLE Package (
    package_id INT PRIMARY KEY,
    weight DECIMAL(5,2),
    type VARCHAR(50),
    description TEXT,
    receiver_name VARCHAR(100),
    receiver_phone VARCHAR(15),
    receiver_address TEXT,
    receiver_city VARCHAR(50),
    last_location VARCHAR(100),
    last_updated DATE,
    cust_id INT,
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
);

-- SHIPMENT TABLE
CREATE TABLE Shipment (
    shipment_id INT PRIMARY KEY,
    tracking_no VARCHAR(50),
    send_date DATE,
    delivery_date DATE,
    delivery_status VARCHAR(50),
    expected_date DATE,
    package_id INT,
    agent_id INT,
    FOREIGN KEY (package_id) REFERENCES Package(package_id),
    FOREIGN KEY (agent_id) REFERENCES Delivery_Agent(agent_id)
);

-- PAYMENT TABLE (UPDATED)
CREATE TABLE Payment (
    payment_id INT PRIMARY KEY,
    amount DECIMAL(10,2),
    payment_date DATE,
    payment_method VARCHAR(50),
    payment_type VARCHAR(50),
    payment_ref VARCHAR(100),
    status VARCHAR(50),
    cust_id INT,
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
);

-- COMPLAINT TABLE
CREATE TABLE Complaint (
    complaint_id INT PRIMARY KEY,
    description TEXT,
    type VARCHAR(50),
    status VARCHAR(50),
    complaint_date DATE,
    resolution_status VARCHAR(50),
    resolution_date DATE,
    cust_id INT,
    shipment_id INT,
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id),
    FOREIGN KEY (shipment_id) REFERENCES Shipment(shipment_id)
);

-- AGENT-VEHICLE RELATION (M:N)
CREATE TABLE Uses (
    agent_id INT,
    vehicle_id INT,
    assign_date DATE,
    route VARCHAR(100),
    status VARCHAR(50),
    PRIMARY KEY (agent_id, vehicle_id),
    FOREIGN KEY (agent_id) REFERENCES Delivery_Agent(agent_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
);
