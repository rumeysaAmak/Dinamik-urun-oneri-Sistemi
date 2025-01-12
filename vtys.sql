select*from users
select*from products
select*from interactions

--799.00dan yüksek fiyattaki ürünler
select name,price from products where price>799.00

--inner join ile tabloları birleştirme
select i.rating,p.name from interactions as i
inner join products as p on p.id=i.product_id
where i.rating>4
group by i.rating,p.name 

select u.name,u.age, p.name from interactions as i
inner join products as p on p.id=i.product_id
inner join users as u on u.id=i.user_id
where u.age>24
group by u.name,u.age, p.name 

--220.00 fiyatından düşük ürünler
select name, price from products 
where price < 220.00
order by price asc

--her kategorinin ortalama fiyatı
select category, round(avg(price), 2) as ortalama_fiyat 
from products
group by category

-- En yüksek harcama yapan kullanıcı listesi
select u.name, sum(p.price) as harcamalar
from interactions as i
inner join users as u on u.id = i.user_id
inner join products as p on p.id = i.product_id
group by u.name
having sum(p.price) > 200
order by harcamalar asc
