INSERT INTO categories (name, description)
VALUES
    ('Electronics', 'Phones, laptops, gaming gear and accessories'),
    ('Vehicles', 'Cars, motorcycles, bicycles and transport accessories'),
    ('Home & Living', 'Furniture, decor, kitchen and home office items'),
    ('Services', 'Freelance, tutoring, local repair and business services')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (email, full_name, password_hash, role, is_blocked)
VALUES
    ('admin@example.com', 'Admin Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'admin', FALSE),
    ('moderator@example.com', 'Moderator Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'moderator', FALSE),
    ('seller@example.com', 'Seller Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('buyer@example.com', 'Buyer Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE)
ON CONFLICT (email) DO NOTHING;

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'MacBook Pro 14 M3',
    'Compact performance laptop with 16GB RAM, 512GB SSD, charger and excellent battery health. Ideal for development, design and study.',
    1799.00,
    'approved',
    NULL,
    seller.id,
    electronics.id
FROM users seller
CROSS JOIN categories electronics
WHERE seller.email = 'seller@example.com'
  AND electronics.name = 'Electronics'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'MacBook Pro 14 M3'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'City Bicycle Riverside',
    'Reliable commuter bike with lights, rear rack and recently serviced brakes. Perfect for daily city rides.',
    420.00,
    'approved',
    NULL,
    seller.id,
    vehicles.id
FROM users seller
CROSS JOIN categories vehicles
WHERE seller.email = 'seller@example.com'
  AND vehicles.name = 'Vehicles'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'City Bicycle Riverside'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Walnut Standing Desk',
    'Height-adjustable standing desk with walnut finish, cable tray and quiet motor. Great for a modern home office.',
    690.00,
    'approved',
    NULL,
    seller.id,
    living.id
FROM users seller
CROSS JOIN categories living
WHERE seller.email = 'seller@example.com'
  AND living.name = 'Home & Living'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'Walnut Standing Desk'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Math Tutoring for High School',
    'One-on-one online tutoring for algebra, geometry and exam prep with flexible evening slots and progress tracking.',
    30.00,
    'approved',
    NULL,
    seller.id,
    services.id
FROM users seller
CROSS JOIN categories services
WHERE seller.email = 'seller@example.com'
  AND services.name = 'Services'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'Math Tutoring for High School'
  );

INSERT INTO listing_images (listing_id, url, position)
SELECT listing.id, image.url, image.position
FROM listings listing
JOIN (
    VALUES
        ('MacBook Pro 14 M3', 'https://images.unsplash.com/photo-1517336714739-489689fd1ca8?auto=format&fit=crop&w=1200&q=80', 0),
        ('MacBook Pro 14 M3', 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=1200&q=80', 1),
        ('City Bicycle Riverside', 'https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=1200&q=80', 0),
        ('Walnut Standing Desk', 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80', 0),
        ('Walnut Standing Desk', 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=80', 1),
        ('Math Tutoring for High School', 'https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=1200&q=80', 0)
) AS image(title, url, position)
    ON image.title = listing.title
WHERE NOT EXISTS (
    SELECT 1
    FROM listing_images existing
    WHERE existing.listing_id = listing.id
      AND existing.url = image.url
);

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    buyer.id,
    seller.id,
    'Hello! Is this listing still available, and is there room for a small discount?'
FROM listings listing
CROSS JOIN users buyer
CROSS JOIN users seller
WHERE listing.title = 'MacBook Pro 14 M3'
  AND buyer.email = 'buyer@example.com'
  AND seller.email = 'seller@example.com'
  AND NOT EXISTS (
      SELECT 1
      FROM messages existing
      WHERE existing.listing_id = listing.id
        AND existing.sender_id = buyer.id
        AND existing.recipient_id = seller.id
  );
