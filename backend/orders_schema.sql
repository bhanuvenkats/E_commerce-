-- 1. carts
CREATE TABLE siri.carts (
    id serial PRIMARY KEY,
    user_id int NOT NULL REFERENCES siri.users(id) ON DELETE CASCADE,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- 2. cart_items
CREATE TABLE siri.cart_items (
    id serial PRIMARY KEY,
    cart_id int NOT NULL REFERENCES siri.carts(id) ON DELETE CASCADE,
    product_id int NOT NULL REFERENCES siri.products(id) ON DELETE CASCADE,
    quantity int NOT NULL,
    price_at_add numeric(10,2) NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- 3. orders
CREATE TABLE siri.orders (
    id serial PRIMARY KEY,
    user_id int NOT NULL REFERENCES siri.users(id) ON DELETE CASCADE,
    total_amount numeric(12,2) NOT NULL,
    status varchar(32) NOT NULL DEFAULT 'pending',
    shipping_address_id int REFERENCES siri.user_addresses(id) ON DELETE SET NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- 4. order_items
CREATE TABLE siri.order_items (
    id serial PRIMARY KEY,
    order_id int NOT NULL REFERENCES siri.orders(id) ON DELETE CASCADE,
    product_id int NOT NULL REFERENCES siri.products(id) ON DELETE CASCADE,
    quantity int NOT NULL,
    price_at_order numeric(10,2) NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- 5. payments (optional)
CREATE TABLE siri.payments (
    id serial PRIMARY KEY,
    order_id int NOT NULL REFERENCES siri.orders(id) ON DELETE CASCADE,
    payment_method varchar(32) NOT NULL,
    amount numeric(12,2) NOT NULL,
    status varchar(32) NOT NULL DEFAULT 'pending',
    transaction_id varchar(128),
    created_at timestamptz DEFAULT now()
);

-- Additional: order_status_history
CREATE TABLE siri.order_status_history (
    id serial PRIMARY KEY,
    order_id int NOT NULL REFERENCES siri.orders(id) ON DELETE CASCADE,
    old_status varchar(32),
    new_status varchar(32) NOT NULL,
    changed_at timestamptz DEFAULT now()
);

-- Additional: shipments (tracking)
CREATE TABLE siri.shipments (
    id serial PRIMARY KEY,
    order_id int NOT NULL REFERENCES siri.orders(id) ON DELETE CASCADE,
    carrier varchar(64),
    tracking_number varchar(128),
    shipped_at timestamptz,
    delivered_at timestamptz,
    status varchar(32) DEFAULT 'pending'
);

-- Additional: coupons/discounts
CREATE TABLE siri.coupons (
    id serial PRIMARY KEY,
    code varchar(32) UNIQUE NOT NULL,
    description text,
    discount_percent numeric(5,2),
    max_uses int DEFAULT 1,
    expires_at timestamptz,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE siri.order_coupons (
    id serial PRIMARY KEY,
    order_id int NOT NULL REFERENCES siri.orders(id) ON DELETE CASCADE,
    coupon_id int NOT NULL REFERENCES siri.coupons(id) ON DELETE CASCADE,
    applied_at timestamptz DEFAULT now()
);
