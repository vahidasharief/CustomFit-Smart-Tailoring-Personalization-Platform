-- Delete existing tailors
DELETE FROM tailors;

-- Insert new tailors
INSERT INTO tailors (name, email, phone, experience_years, specialty) VALUES
('Rajesh Kumar', 'rajesh.kumar@customfit.com', '+91-555-0123', 15, 'Traditional Sherwanis & Wedding Wear'),
('Priya Sharma', 'priya.sharma@customfit.com', '+91-555-0124', 12, 'Designer Sarees & Lehengas'),
('Abdul Karim', 'abdul.karim@customfit.com', '+91-555-0125', 18, 'Modern Indo-Western Fusion'),
('Meera Patel', 'meera.patel@customfit.com', '+91-555-0126', 20, 'Bridal Couture & Embroidery'),
('Suresh Mehta', 'suresh.mehta@customfit.com', '+91-555-0127', 16, 'Contemporary Ethnic Wear');