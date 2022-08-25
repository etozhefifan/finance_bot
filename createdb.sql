CREATE TABLE budget(
    codename VARCHAR(255) PRIMARY KEY,
    daily_expense INTEGER,
)

CREATE TABLE category(
    codename VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    is_basic_expense BOOLEAN,
    aliases TEXT,
)

CREATE TABLE expenses(
    id INTEGER PRIMARY KEY,
    money_amount INTEGER,
    created DATE,
    category_codename INTEGER,
    raw_text TEXT,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
)

INSERT INTO category (codename, name, is_basic_expense, aliases)
VALUES
    ('food', 'еда', true, 'еда, продукты, пятёрочка, магнит, дикси')
    ('cafe', 'кафе', false, 'кафе, паб, ресторан')
    ('books', 'книги', true, 'книги')
    ('transport', 'транспорт', true, 'трамвай, метро, автобус, троллейбус')
    ('internet', 'интернет', true, 'интернет')
    ('other', 'другое', false, '')
