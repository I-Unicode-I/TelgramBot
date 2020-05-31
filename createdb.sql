create table users (
    id varchar(255) primary key,
    full_name varchar(255),
    user_name varchar(255),
    company text default "",
    reminder_action varchar(255) default "nothing"
    );

create table company (
    market_name varchar(255) primary key,
    company_name varchar(255),
    close_price float default 1.0
    );

insert into  company (market_name, company_name)
values
        ("TSLA", "Tesla"),
        ("GOOG", "Google"),
        ("MSFT", "Microsoft"),
        ("AAPL", "Apple"),
        ("AMZN", "Amazon"),
        ("FB", "Facebook"),
        ("NFLX", "Netflix"),
        ("WMT", "Walmart"),
        ("SSNLF", "Samsung"),
        ("DIS", "Walt Disney"),
        ("CSCO", "Cisco"),
        ("ADBE", "Adobe"),
        ("INTC", "Intel"),
        ("NVDA", "NVIDIA"),
        ("AMD", "AMD"),
        ("IBM", "IBM"),
        ("DELL", "Dell"),
        ("HPQ", "HP-Hewlett Packard"),
        ("V", "VISA"),
        ("MA", "MasterCard"),
        ("NSRGF", "Nestle"),
        ("JPM", "JPMorgan"),
        ("JNJ", "J&J"),
        ("BABA", "Alibaba ADR");


