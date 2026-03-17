-- 1. Show all customers
SELECT * FROM Customer;

-- 2. Show all shipments with customer name
SELECT c.name, s.tracking_no, s.delivery_status
FROM Customer c
JOIN Package p ON c.cust_id = p.cust_id
JOIN Shipment s ON p.package_id = s.package_id;

-- 3. Find all delivered shipments
SELECT * FROM Shipment
WHERE delivery_status = 'Delivered';

-- 4. Find packages sent from Calicut
SELECT * FROM Package
WHERE sender_city = 'Calicut';

-- 5. Count total shipments
SELECT COUNT(*) AS total_shipments FROM Shipment;

-- 6. Find highest payment
SELECT MAX(amount) FROM Payment;

-- 7. Show complaints that are pending
SELECT * FROM Complaint
WHERE resolution_status = 'Pending';

-- 8. Show agent and vehicle used
SELECT d.name AS agent, v.plate_no
FROM Uses u
JOIN Delivery_Agent d ON u.agent_id = d.agent_id
JOIN Vehicle v ON u.vehicle_id = v.vehicle_id;

-- 9. Find shipments not delivered yet
SELECT * FROM Shipment
WHERE delivery_status != 'Delivered';

-- 10. Find customer and payment details
SELECT c.name, p.amount, p.payment_type
FROM Customer c
JOIN Payment p ON c.cust_id = p.cust_id;
