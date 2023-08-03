drop database if exists db;
create database db default character set utf8 collate utf8_general_ci;
grant all on db.* to 'staff'@'localhost' identified by 'password';
use db;

create table kuafu(
	id int auto_increment primary key, 
    name varchar(200) not null, 
    version varchar(200) not null unique
);

create table cnf(
	id int auto_increment primary key, 
    status varchar(200) not null, 
    name varchar(200) not null, 
    product varchar(200) not null, 
    tool varchar(200) not null, 
    ip varchar(200) not null, 
	username varchar(200) not null, 
    password varchar(200) not null,
    foreign key(tool) references kuafu(version)
);

create table history(
	id int auto_increment primary key, 
    status varchar(200) not null, 
    name varchar(200) not null, 
    start_time varchar(200) not null, 
    end_time varchar(200) not null,
    log_name varchar(200) not null,
    cnf_id int not null,
    foreign key(cnf_id) references cnf(id)
);

insert into kuafu values(null, 'kuafu-v6.18.0', '6.18.0');
insert into kuafu values(null, 'kuafu-v6.19.0', '6.19.0');
insert into cnf values(null, 'NEW', 'vCU-36908', 'VCU', '6.18.0', '10.69.57.210', 'cranuser1', 'systeM!23');
insert into cnf values(null, 'NEW', 'vDU-36908', 'VDU', '6.19.0', '10.69.57.210', 'cranuser2', 'systeM!23');