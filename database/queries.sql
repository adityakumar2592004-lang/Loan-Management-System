-- 1. Display all customers
SELECT * FROM customers;


-- 2. Display all loan applications
SELECT * FROM applications;


-- 3. Display total number of customers
SELECT COUNT(*) AS total_customers
FROM customers;


-- 4. Display total number of loan applications
SELECT COUNT(*) AS total_applications
FROM applications;


-- 5. Display applications with customer details
SELECT
    a.application_id,
    c.full_name,
    c.pan_number,
    a.loan_amount,
    a.loan_type,
    a.application_date,
    a.status
FROM applications a
JOIN customers c
ON a.customer_id = c.customer_id;


-- 6. Calculate total loan amount
SELECT SUM(loan_amount) AS total_loan_amount
FROM applications;


-- 7. Count applications by status
SELECT status, COUNT(*) AS total
FROM applications
GROUP BY status;


-- 8. Display latest loan applications
SELECT *
FROM applications
ORDER BY application_id DESC
LIMIT 10;


-- 9. Display customers in descending order
SELECT *
FROM customers
ORDER BY customer_id DESC;