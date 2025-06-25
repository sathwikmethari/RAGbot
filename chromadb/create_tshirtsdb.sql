-- -- Create the database
-- CREATE DATABASE Project_tshirts;
-- USE Project_tshirts;

-- -- Create the t_shirts table
-- CREATE TABLE tshirts (
--     t_shirt_id INT AUTO_INCREMENT PRIMARY KEY,
--     brand ENUM('WROGN', 'LEVI', 'NIKE', 'ADIDAS', 'PUMA', 'REEBOK', 'HRX', '') NOT NULL,
--     color ENUM('RED', 'BLUE', 'BLACK', 'WHITE', 'GREEN', 'YELLOW', 'PURPLE', 'PINK') NOT NULL,
--     size ENUM('XS', 'S', 'M', 'L', 'XL', '2XL') NOT NULL,
--     price INT CHECK (price BETWEEN 200 AND 1000),
--     stock_quantity INT NOT NULL,
--     UNIQUE KEY brand_color_size (brand, color, size)
-- );

-- -- Create the discounts table
-- CREATE TABLE discounts (
--     discount_id INT AUTO_INCREMENT PRIMARY KEY,
--     t_shirt_id INT NOT NULL,
--     pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
--     FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id)
-- );

-- -- Create a stored procedure to populate the t_shirts table
-- DELIMITER $$
-- CREATE PROCEDURE PopulateTShirts()
-- BEGIN
--     DECLARE counter INT DEFAULT 0;
--     DECLARE max_records INT DEFAULT 500;
--     DECLARE brand ENUM('Van Huesen', 'Levi', 'Nike', 'Adidas');
--     DECLARE color ENUM('Red', 'Blue', 'Black', 'White');
--     DECLARE size ENUM('XS', 'S', 'M', 'L', 'XL');
--     DECLARE price INT;
--     DECLARE stock INT;

--     -- Seed the random number generator
--     SET SESSION rand_seed1 = UNIX_TIMESTAMP();

--     WHILE counter < max_records DO
--         -- Generate random values
--         SET brand = ELT(FLOOR(1 + RAND() * 4), 'Van Huesen', 'Levi', 'Nike', 'Adidas');
--         SET color = ELT(FLOOR(1 + RAND() * 4), 'Red', 'Blue', 'Black', 'White');
--         SET size = ELT(FLOOR(1 + RAND() * 5), 'XS', 'S', 'M', 'L', 'XL');
--         SET price = FLOOR(10 + RAND() * 41);
--         SET stock = FLOOR(10 + RAND() * 91);

--         -- Attempt to insert a new record
--         -- Duplicate brand, color, size combinations will be ignored due to the unique constraint
--         BEGIN
--             DECLARE CONTINUE HANDLER FOR 1062 BEGIN END;  -- Handle duplicate key error
--             INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
--             VALUES (brand, color, size, price, stock);
--             SET counter = counter + 1;
--         END;
--     END WHILE;
-- END$$
-- DELIMITER ;

-- -- Call the stored procedure to populate the t_shirts table
-- CALL PopulateTShirts();

-- -- Insert at least 10 records into the discounts table
-- INSERT INTO discounts (t_shirt_id, pct_discount)
-- VALUES
-- (1, 10.00),
-- (2, 15.00),
-- (3, 20.00),
-- (4, 5.00),
-- (5, 25.00),
-- (6, 10.00),
-- (7, 30.00),
-- (8, 35.00),
-- (9, 40.00),
-- (10, 45.00);

-- Postgres syntax

DO $$
DECLARE
    counter INT := 0;
    max_records INT := 750;
    brand TEXT;
    color TEXT;
    size TEXT;
    price INT;
    stock INT;
    brands TEXT[] := ARRAY['WROGN', 'LEVI', 'NIKE', 'ADIDAS', 'PUMA', 'REEBOK', 'HRX', 'ASICS', 'CULT', 'KAPPA', 'CELIO', 'DOMYOS', 'USPA'];
    colors TEXT[] := ARRAY['RED', 'BLUE', 'BLACK', 'WHITE', 'GREEN', 'YELLOW', 'PURPLE','PINK', 'BROWN', 'ORANGE', 'BEIGE', 'GREY', 'OLIVE'];
    sizes TEXT[] := ARRAY['XS', 'S', 'M', 'L', 'XL', '2XL'];
BEGIN
    WHILE counter < max_records LOOP
        brand := brands[FLOOR(1 + RANDOM() * array_length(brands, 1))::INT];
        color := colors[FLOOR(1 + RANDOM() * array_length(colors, 1))::INT];
        size := sizes[FLOOR(1 + RANDOM() * array_length(sizes, 1))::INT];
        price := FLOOR(200 + RANDOM() * 1001)::INT;
        stock := FLOOR(10 + RANDOM() * 41)::INT;

        BEGIN
            INSERT INTO tshirt_inventory ("BRAND", "COLOR", "SIZE", "PRICE", "STOCK_QUANTITY")
            VALUES (brand, color, size, price, stock);
            counter := counter + 1;
        EXCEPTION WHEN unique_violation THEN
            -- skip duplicate
            NULL;
        END;
    END LOOP;
END$$;