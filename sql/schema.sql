CREATE TABLE IF NOT EXISTS currency_rates (
    rate_date DATE NOT NULL,
    currency_code VARCHAR(3) NOT NULL,
    nominal INTEGER NOT NULL,
    rate NUMERIC  NOT NULL,
    CONSTRAINT currency_rates_unique
    UNIQUE (rate_date, currency_code)
    );