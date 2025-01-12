--users tablosu oluşturma
create table users (
    id serial primary key,
    name varchar(50) not null,
    age int not null,
    preferences text
);

--products tablosu oluşturma
create table products (
    id serial primary key,
    name varchar(50) not null,
    category varchar(50),
    price decimal(10, 2) not null
);


--users-products etkileşimleri tablosu
create table interactions (
    id serial primary key,
    user_id int references users(id),
    product_id int references products(id),
    rating int check (rating >= 1 and rating <= 5)
);


--TABLOLARA VERİ EKLEME

--users tablosuna veri ekleme
insert into users (name, age, preferences) values
('Axel', 20, 'technology,books'),
('Austin', 18, 'fashion,makeup'),
('Cyrus', 22, 'sports,fitness'),
('Luna', 25, 'music,travel'),
('Ethan', 30, 'photography,cooking'),
('Olivia', 28, 'art,reading'),
('Sophia', 24, 'gaming,design'),
('Mia', 27, 'fitness,yoga'),
('Liam', 32, 'technology,sports'),
('Noah', 19, 'travel,adventure'),
('Emma', 21, 'books,movies'),
('Ava', 26, 'fashion,shopping'),
('Isabella', 23, 'gardening,cooking'),
('Mason', 29, 'sports,technology'),
('Logan', 20, 'gaming,fitness'),
('Elijah', 25, 'travel,photography'),
('James', 22, 'art,music'),
('Lucas', 27, 'books,fashion'),
('Charlotte', 24, 'yoga,meditation'),
('Amelia', 23, 'technology,coding'),
('Harper', 21, 'movies,music'),
('Evelyn', 28, 'fashion,photography'),
('Henry', 29, 'sports,adventure'),
('Sebastian', 31, 'travel,books'),
('Alexander', 30, 'cooking,fitness'),
('Scarlett', 26, 'shopping,gaming'),
('Victoria', 19, 'art,reading'),
('Penelope', 18, 'makeup,movies'),
('Jack', 32, 'sports,fitness'),
('Oliver', 20, 'adventure,technology'),
('Ella', 22, 'music,books'),
('Chloe', 24, 'art,gaming'),
('Zoe', 23, 'photography,cooking'),
('Lily', 26, 'fashion,fitness'),
('Ryan', 21, 'technology,sports'),
('Grace', 28, 'yoga,travel'),
('Hannah', 30, 'books,movies'),
('Nora', 27, 'gardening,shopping'),
('Aaron', 25, 'fitness,travel'),
('Daniel', 29, 'adventure,reading'),
('Eli', 31, 'sports,photography'),
('Anna', 23, 'art,design'),
('Sophia', 19, 'technology,music'),
('Miles', 32, 'fashion,gaming'),
('Lila', 20, 'shopping,books'),
('Jordan', 22, 'sports,fitness'),
('Ruby', 24, 'adventure,yoga'),
('Molly', 26, 'movies,music'),
('Leo', 28, 'photography,travel');


--products tablosuna veri ekleme
insert into products (name, category, price) values
('Laptop', 'Electronics', 1200.00),
('Smartphone', 'Electronics', 800.00),
('Headphones', 'Electronics', 150.00),
('Running Shoes', 'Sports', 100.00),
('Yoga Mat', 'Fitness', 50.00),
('Cookbook', 'Books', 25.00),
('Travel Backpack', 'Travel', 60.00),
('Winter Jacket', 'Fashion', 200.00),
('Coffee Maker', 'Home', 100.00),
('Tablet', 'Electronics', 400.00),
('Sunglasses', 'Fashion', 80.00),
('Tennis Racket', 'Sports', 120.00),
('Gaming Console', 'Electronics', 500.00),
('Desk Lamp', 'Home', 40.00),
('Wireless Speaker', 'Electronics', 150.00),
('Smartwatch', 'Electronics', 300.00),
('Running Shorts', 'Sports', 30.00),
('Water Bottle', 'Fitness', 15.00),
('Mountain Bike', 'Sports', 1000.00),
('Perfume', 'Fashion', 120.00),
('Face Cream', 'Makeup', 50.00),
('Notebook', 'Books', 20.00),
('Painting Kit', 'Art', 70.00),
('Action Camera', 'Electronics', 300.00),
('Laptop Bag', 'Fashion', 40.00),
('Bluetooth Earbuds', 'Electronics', 200.00),
('Electric Kettle', 'Home', 70.00),
('Camping Tent', 'Travel', 250.00),
('Winter Boots', 'Fashion', 150.00),
('Cooking Pan', 'Home', 60.00),
('Digital Watch', 'Electronics', 250.00),
('Running Hat', 'Sports', 25.00),
('Sports Gloves', 'Fitness', 35.00),
('Cycling Helmet', 'Sports', 120.00),
('Drawing Pad', 'Art', 90.00),
('Gardening Tools', 'Home', 80.00),
('Travel Pillow', 'Travel', 40.00),
('Fitness Tracker', 'Electronics', 200.00),
('Winter Scarf', 'Fashion', 60.00),
('Gaming Chair', 'Electronics', 300.00),
('Trekking Poles', 'Sports', 80.00),
('Digital Camera', 'Electronics', 700.00),
('Photo Frame', 'Home', 30.00),
('Leather Wallet', 'Fashion', 70.00),
('Smart Light', 'Electronics', 50.00),
('Yoga Blocks', 'Fitness', 25.00),
('Sports Bag', 'Sports', 50.00),
('Makeup Kit', 'Makeup', 120.00),
('Wireless Charger', 'Electronics', 100.00),
('Travel Organizer', 'Travel', 30.00);


--users tablosunda eksik olan veriyi ekleme
insert into users (name, age, preferences) values
('User50', 25, 'sports,fitness');



--interactions tablosuna veri ekleme
insert into interactions (user_id, product_id, rating) values
(1, 1, 5),
(2, 3, 4),
(3, 5, 3),
(4, 7, 5),
(5, 9, 4),
(6, 11, 3),
(7, 13, 5),
(8, 15, 4),
(9, 17, 5),
(10, 19, 4),
(11, 21, 5),
(12, 23, 3),
(13, 25, 4),
(14, 27, 5),
(15, 29, 3),
(16, 2, 4),
(17, 4, 5),
(18, 6, 3),
(19, 8, 4),
(20, 10, 5),
(21, 12, 3),
(22, 14, 4),
(23, 16, 5),
(24, 18, 3),
(25, 20, 4),
(26, 22, 5),
(27, 24, 3),
(28, 26, 4),
(29, 28, 5),
(30, 30, 4),
(31, 29, 5),
(32, 28, 4),
(33, 27, 3),
(34, 26, 4),
(35, 25, 5),
(36, 24, 3),
(37, 23, 4),
(38, 22, 5),
(39, 21, 3),
(40, 20, 4),
(41, 19, 5),
(42, 18, 3),
(43, 17, 4),
(44, 16, 5),
(45, 15, 3),
(46, 14, 4),
(47, 13, 5),
(48, 12, 3),
(49, 11, 4),
(50, 10, 5);


--tabloların görünümü
select*from users
select*from products
select*from interactions

