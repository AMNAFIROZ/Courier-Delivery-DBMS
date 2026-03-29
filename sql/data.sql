-- CUSTOMER (5 records)
INSERT INTO Customer VALUES
(1, 'Aisha', 'aisha@gmail.com', '9876543210', 'Calicut', 'Street A', '673001', 'Kerala', '2024-01-01'),
(2, 'Rahul', 'rahul@gmail.com', '9876501234', 'Kochi', 'Street B', '682001', 'Kerala', '2024-02-01'),
(3, 'Neha', 'neha@gmail.com', '9123456789', 'Trivandrum', 'Street C', '695001', 'Kerala', '2024-02-10'),
(4, 'Arun', 'arun@gmail.com', '9012345678', 'Kannur', 'Street D', '670001', 'Kerala', '2024-03-01'),
(5, 'Meera', 'meera@gmail.com', '9988776655', 'Kollam', 'Street E', '691001', 'Kerala', '2024-03-05');

-- BRANCH (5 records)
INSERT INTO Branch VALUES
(1, 'Calicut Branch', 'Main Road', 'Calicut', '0495-123456'),
(2, 'Kochi Branch', 'MG Road', 'Kochi', '0484-654321'),
(3, 'TVM Branch', 'Central', 'Trivandrum', '0471-111222'),
(4, 'Kannur Branch', 'Town Area', 'Kannur', '0497-222333'),
(5, 'Kollam Branch', 'Market Road', 'Kollam', '0474-333444');

-- DELIVERY AGENT (5 records)
INSERT INTO Delivery_Agent VALUES
(1, 'Arjun', '9999990001', 'LIC101', 'Active', 1),
(2, 'Vijay', '9999990002', 'LIC102', 'Active', 2),
(3, 'Kiran', '9999990003', 'LIC103', 'Active', 3),
(4, 'Ravi', '9999990004', 'LIC104', 'Inactive', 4),
(5, 'Manoj', '9999990005', 'LIC105', 'Active', 5);

-- VEHICLE (5 records)
INSERT INTO Vehicle VALUES
(1, 'KL11AB1234', 100, 'Van', 'Available', 1),
(2, 'KL07CD5678', 80, 'Bike', 'Available', 2),
(3, 'KL01EF9012', 120, 'Truck', 'Busy', 3),
(4, 'KL12GH3456', 90, 'Van', 'Available', 4),
(5, 'KL02IJ7890', 70, 'Bike', 'Maintenance', 5);

-- PACKAGE (5 records)
INSERT INTO Package VALUES
(1, 2.5, 'Electronics', 'Mobile Phone', 'Sneha', '8888888888', 'Address X', 'Kochi', 'Calicut', '2024-03-01', 1),
(2, 1.2, 'Clothes', 'Shirt', 'Anu', '7777777777', 'Address Y', 'Calicut', 'Kochi', '2024-03-02', 2),
(3, 3.0, 'Books', 'Engineering Books', 'Riya', '7666666666', 'Address Z', 'Trivandrum', 'Kannur', '2024-03-03', 3),
(4, 0.8, 'Accessories', 'Watch', 'Maya', '7555555555', 'Address W', 'Kannur', 'Calicut', '2024-03-04', 4),
(5, 5.0, 'Furniture', 'Chair', 'Nikhil', '7444444444', 'Address V', 'Kollam', 'Kochi', '2024-03-05', 5);

-- SHIPMENT (5 records)
INSERT INTO Shipment VALUES
(1, 'TRK101', '2024-03-01', '2024-03-03', 'Delivered', '2024-03-04', 1, 1),
(2, 'TRK102', '2024-03-02', NULL, 'In Transit', '2024-03-05', 2, 2),
(3, 'TRK103', '2024-03-03', NULL, 'In Transit', '2024-03-06', 3, 3),
(4, 'TRK104', '2024-03-04', '2024-03-06', 'Delivered', '2024-03-07', 4, 4),
(5, 'TRK105', '2024-03-05', NULL, 'Pending', '2024-03-08', 5, 5);

-- PAYMENT (5 records)
INSERT INTO Payment VALUES
(1, 500.00, '2024-03-01', 'UPI', 'Online', 'REF101', 'Completed', 1),
(2, 300.00, '2024-03-02', 'Cash', 'Offline', 'REF102', 'Completed', 2),
(3, 700.00, '2024-03-03', 'Card', 'Online', 'REF103', 'Completed', 3),
(4, 250.00, '2024-03-04', 'UPI', 'Online', 'REF104', 'Pending', 4),
(5, 900.00, '2024-03-05', 'Cash', 'Offline', 'REF105', 'Completed', 5);

-- COMPLAINT (5 records)
INSERT INTO Complaint VALUES
(1, 'Late delivery', 'Delay', 'Open', '2024-03-04', 'Pending', NULL, 1, 1),
(2, 'Damaged item', 'Damage', 'Closed', '2024-03-05', 'Resolved', '2024-03-06', 2, 2),
(3, 'Wrong address', 'Error', 'Open', '2024-03-06', 'Pending', NULL, 3, 3),
(4, 'Missing package', 'Lost', 'Open', '2024-03-07', 'Pending', NULL, 4, 4),
(5, 'Late update', 'Delay', 'Closed', '2024-03-08', 'Resolved', '2024-03-09', 5, 5);

-- USES (5 records)
INSERT INTO Uses VALUES
(1, 1, '2024-03-01', 'Route A', 'Active'),
(2, 2, '2024-03-02', 'Route B', 'Active'),
(3, 3, '2024-03-03', 'Route C', 'Active'),
(4, 4, '2024-03-04', 'Route D', 'Inactive'),
(5, 5, '2024-03-05', 'Route E', 'Active');


-- Insert a test admin user
-- NOTE: In a real app, 'admin123' would be a long, scrambled hash
INSERT INTO System_Users (username, password_hash, role) 
VALUES ('admin', 'admin123', 'Admin');

INSERT INTO System_Users (username, password_hash, role, cust_id) VALUES 
('admin', 'admin123', 'Admin', NULL),
('aisha', 'aisha123', 'Customer', 1),
('rahul', 'rahul123', 'Customer', 2),
('neha', 'neha123', 'Customer', 3),
('arun', 'arun123', 'Customer', 4),
('meera', 'meera123', 'Customer', 5);