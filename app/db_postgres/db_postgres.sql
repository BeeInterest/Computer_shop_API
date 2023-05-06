CREATE TABLE IF NOT EXISTS worker (
	id_worker uuid not null primary key,
	full_name varchar(500) not null,
	phone varchar(13) not null,
	email varchar(200) not null,
	date_birth_w date not null,
	position varchar(13) not null,
	login_ac varchar(200) not null
);
CREATE TABLE IF NOT EXISTS client (
	id_client uuid not null primary key,
	full_name varchar(500) not null,
	phone varchar(13) not null,
	email varchar(200) not null,
	date_birth date not null,
	login_ac varchar(200) not null
);
CREATE TABLE IF NOT EXISTS account (
	login_ac varchar(200) not null primary key,
	password_ac varchar(200) not null
);
ALTER TABLE worker
	ADD FOREIGN KEY(login_ac)
	REFERENCES account (login_ac);
ALTER TABLE client
	ADD FOREIGN KEY(login_ac)
	REFERENCES account (login_ac);
DELETE FROM worker;
DELETE FROM client;
DELETE FROM account;
INSERT INTO account
VALUES
('ylbek134','asdghj1'),
('maluk890','rhuilj2'),
('gagar189','ddfdhj6'),
('lidar908','dfdfmjvm8'),
('gogerai7','jhhjkjh9'),
('serduch901','fhjgjg10'),
('nepo457','ghfdfrgd78'),
('ago0876','fhnhgndg87'),
('run1346','fdgsdvv12'),
('gorelo7654','uterbe123'),
('noshe2893','zcvcbd34'),
('sheko34223','fvgdg89'),
('dira0743234','dsdfdsf45');
INSERT INTO client
VALUES
('aec266a9-923b-4ad3-b336-ddb3537ce282','Улбеков Спиридон Асеев','89334457849','yli@gmail.com','1999-12-01','ylbek134'),
('cfc57dbb-d46c-4a50-9546-108a334e3bf8','Малюк Платонида Терентьева','89444493489','malui@gmail.com','1987-03-12','maluk890'),
('c2343af5-002a-43f6-bd23-a7a738a4f57e','Гагарина Агапия Ионова','89330057629','gagary@gmail.com','1995-07-29','gagar189'),
('73487f1c-14c8-44d6-9fd2-d361b29e84e8','Лиданова Эсмеральда Анурьева','89333409489','lidan0@gmail.com','1989-09-25','lidar908'),
('a269bf6e-a7cb-4762-98d6-46d7e1303ebe','Гогер Ай Александрова','89334453489','gogerai@gmail.com','1971-05-16','gogerai7'),
('ec4638fe-6f61-4e33-8e38-7f0f605a89d9','Сердючкин Климент Златоустский','89334471589','serdu91@gmail.com','2000-11-30','serduch901');
INSERT INTO worker
VALUES
('6ff1fd16-c42c-4ab4-a2ba-cd146b6f6062','Непо Гаянэ Басинская','89334452389','nepo.ga@gmail.com','1997-04-11','admin','nepo457'),
('3097b4a6-3e0d-403b-85dd-369d40984024','Аго Элла Лаврина','89444458789','ago.all@gmail.com','1991-09-04','admin','ago0876'),
('9ea4baa7-d248-4149-9573-62baa828596d','Рун Родион Радугин','89334418629','run.ro@gmail.com','1994-10-23','manager','run1346'),
('effe1fa8-f5e4-4c28-ae9a-45b4370694ba','Горела Мина Малышев','89334100189','gorela.mi@gmail.com','1990-08-17','manager','gorelo7654'),
('8a2f345e-17f1-47b3-a16c-626894277a98','Ножевая Дина Феоктистова','89334449489','nosh.di@gmail.com','1982-12-03','manager','noshe2893'),
('c7a11bfb-8834-440f-a261-cb8ffdbdf042','Щекоч Тамила Несмеянова','89334473089','shekoch.ta@gmail.com','1983-05-21','admin','sheko34223'),
('332dfddc-8ca4-48ea-8b33-b03092a9bbae','Дир Эраст Плющев','89332936789','dir.era@gmail.com','1992-04-13','manager','dira0743234');