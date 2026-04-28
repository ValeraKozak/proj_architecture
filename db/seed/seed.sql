INSERT INTO categories (name, description)
VALUES
    ('Electronics', 'Phones, laptops, gaming gear and accessories'),
    ('Vehicles', 'Cars, motorcycles, bicycles and transport accessories'),
    ('Home & Living', 'Furniture, decor, kitchen and home office items'),
    ('Services', 'Freelance, tutoring, local repair and business services'),
    ('Real Estate', 'Apartments, houses, rooms and office spaces'),
    ('Fashion', 'Clothing, footwear, accessories and personal style'),
    ('Kids & Family', 'Toys, strollers, school items and family essentials'),
    ('Jobs', 'Hiring, part-time work, internships and freelance opportunities'),
    ('Pets', 'Pet care, accessories, adoption support and supplies'),
    ('Garden & Outdoor', 'Tools, plants, grills, patio and outdoor living')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (email, full_name, password_hash, role, is_blocked)
VALUES
    ('admin@example.com', 'Admin Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'admin', FALSE),
    ('moderator@example.com', 'Moderator Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'moderator', FALSE),
    ('seller@example.com', 'Seller Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('buyer@example.com', 'Buyer Demo', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('seller2@example.com', 'Studio Seller', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('blocked@example.com', 'Blocked Reader', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', TRUE),
    ('designer@example.com', 'Design Seller', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('auto@example.com', 'Auto Seller', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('realtor@example.com', 'Estate Agent', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('tutor@example.com', 'Tutor Expert', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('parentseller@example.com', 'Family Seller', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('employer@example.com', 'Hiring Manager', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('petseller@example.com', 'Pet Care Shop', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('gardener@example.com', 'Outdoor Seller', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('buyer2@example.com', 'Second Buyer', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('buyer3@example.com', 'Third Buyer', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE),
    ('buyer4@example.com', 'Fourth Buyer', '2236c89f42dfc3243032f4ccf3ee0ed0$8e3b283f82fc6626bc96efdfe173c6e9f36d042dd4350becf46fb33c594fcef2', 'user', FALSE)
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

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'PlayStation 5 Slim Bundle',
    'Console bundle with two controllers, charging dock and three games. Lightly used and fully tested.',
    640.00,
    'approved',
    NULL,
    seller2.id,
    electronics.id
FROM users seller2
CROSS JOIN categories electronics
WHERE seller2.email = 'seller2@example.com'
  AND electronics.name = 'Electronics'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'PlayStation 5 Slim Bundle'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Mirrorless Camera Starter Kit',
    'Camera body, 35mm lens, extra battery and compact travel tripod for creators who want a sharp portable setup.',
    980.00,
    'pending',
    NULL,
    seller2.id,
    electronics.id
FROM users seller2
CROSS JOIN categories electronics
WHERE seller2.email = 'seller2@example.com'
  AND electronics.name = 'Electronics'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'Mirrorless Camera Starter Kit'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Weekend Cleaning Service',
    'Apartment cleaning with kitchen and bathroom deep-clean add-on, available on weekends in the city center.',
    55.00,
    'pending',
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
      WHERE existing.title = 'Weekend Cleaning Service'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Luxury Villa for 200',
    'Unrealistically priced property listing included to demonstrate moderation rejection and QA scenarios.',
    200.00,
    'rejected',
    'Suspicious pricing and insufficient ownership details.',
    seller2.id,
    living.id
FROM users seller2
CROSS JOIN categories living
WHERE seller2.email = 'seller2@example.com'
  AND living.name = 'Home & Living'
  AND NOT EXISTS (
      SELECT 1
      FROM listings existing
      WHERE existing.title = 'Luxury Villa for 200'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Vintage Vinyl Collection',
    'Curated jazz and rock vinyl selection prepared as a draft listing before publication.',
    260.00,
    'draft',
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
      WHERE existing.title = 'Vintage Vinyl Collection'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Scandinavian Lounge Chair',
    'Accent armchair in oak and textured beige fabric, recently cleaned and kept in a smoke-free apartment.',
    315.00,
    'approved',
    NULL,
    designer.id,
    living.id
FROM users designer
CROSS JOIN categories living
WHERE designer.email = 'designer@example.com'
  AND living.name = 'Home & Living'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Scandinavian Lounge Chair'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Minimal Floor Lamp',
    'Warm ambient floor lamp with matte black frame and soft linen shade for living room or studio corner.',
    85.00,
    'approved',
    NULL,
    designer.id,
    living.id
FROM users designer
CROSS JOIN categories living
WHERE designer.email = 'designer@example.com'
  AND living.name = 'Home & Living'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Minimal Floor Lamp'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Toyota Corolla 2016',
    'Reliable sedan with automatic transmission, full service history and recent brake replacement.',
    9400.00,
    'approved',
    NULL,
    auto.id,
    vehicles.id
FROM users auto
CROSS JOIN categories vehicles
WHERE auto.email = 'auto@example.com'
  AND vehicles.name = 'Vehicles'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Toyota Corolla 2016'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Electric Scooter Ninebot',
    'Foldable electric scooter with charger, good battery health and fresh tires for city commuting.',
    520.00,
    'approved',
    NULL,
    auto.id,
    vehicles.id
FROM users auto
CROSS JOIN categories vehicles
WHERE auto.email = 'auto@example.com'
  AND vehicles.name = 'Vehicles'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Electric Scooter Ninebot'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Sunny Studio Near Metro',
    'Compact furnished studio with balcony, fast internet and a five-minute walk to the metro station.',
    480.00,
    'approved',
    NULL,
    realtor.id,
    realestate.id
FROM users realtor
CROSS JOIN categories realestate
WHERE realtor.email = 'realtor@example.com'
  AND realestate.name = 'Real Estate'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Sunny Studio Near Metro'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Coworking Desk Downtown',
    'Monthly desk rental in a bright coworking space with meeting rooms, coffee and 24/7 access.',
    220.00,
    'approved',
    NULL,
    realtor.id,
    realestate.id
FROM users realtor
CROSS JOIN categories realestate
WHERE realtor.email = 'realtor@example.com'
  AND realestate.name = 'Real Estate'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Coworking Desk Downtown'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'English Speaking Club',
    'Weekly online sessions focused on fluent conversation, pronunciation and confidence for intermediate learners.',
    18.00,
    'approved',
    NULL,
    tutor.id,
    services.id
FROM users tutor
CROSS JOIN categories services
WHERE tutor.email = 'tutor@example.com'
  AND services.name = 'Services'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'English Speaking Club'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'SAT Math Intensive Course',
    'Structured SAT math preparation with weekly progress reports and practice-test reviews.',
    45.00,
    'approved',
    NULL,
    tutor.id,
    services.id
FROM users tutor
CROSS JOIN categories services
WHERE tutor.email = 'tutor@example.com'
  AND services.name = 'Services'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'SAT Math Intensive Course'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Double Baby Stroller',
    'Side-by-side stroller with rain cover, storage basket and compact fold for family travel.',
    210.00,
    'approved',
    NULL,
    family.id,
    kids.id
FROM users family
CROSS JOIN categories kids
WHERE family.email = 'parentseller@example.com'
  AND kids.name = 'Kids & Family'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Double Baby Stroller'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Wooden Montessori Toy Set',
    'Colorful early-learning toy bundle with safe wooden pieces for toddlers and preschoolers.',
    54.00,
    'approved',
    NULL,
    family.id,
    kids.id
FROM users family
CROSS JOIN categories kids
WHERE family.email = 'parentseller@example.com'
  AND kids.name = 'Kids & Family'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Wooden Montessori Toy Set'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Graphic Designer Internship',
    'Part-time remote internship for a junior designer with Figma basics and portfolio samples.',
    300.00,
    'approved',
    NULL,
    employer.id,
    jobs.id
FROM users employer
CROSS JOIN categories jobs
WHERE employer.email = 'employer@example.com'
  AND jobs.name = 'Jobs'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Graphic Designer Internship'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Customer Support Specialist',
    'Evening support role for chat and email communication with fluent English and calm communication style.',
    650.00,
    'pending',
    NULL,
    employer.id,
    jobs.id
FROM users employer
CROSS JOIN categories jobs
WHERE employer.email = 'employer@example.com'
  AND jobs.name = 'Jobs'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Customer Support Specialist'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Leather Weekend Bag',
    'Travel bag in dark brown leather with shoulder strap and solid metal hardware in excellent shape.',
    165.00,
    'approved',
    NULL,
    designer.id,
    fashion.id
FROM users designer
CROSS JOIN categories fashion
WHERE designer.email = 'designer@example.com'
  AND fashion.name = 'Fashion'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Leather Weekend Bag'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Vintage Denim Jacket',
    'Oversized classic denim jacket with light wash and clean stitching, easy to style year-round.',
    72.00,
    'approved',
    NULL,
    designer.id,
    fashion.id
FROM users designer
CROSS JOIN categories fashion
WHERE designer.email = 'designer@example.com'
  AND fashion.name = 'Fashion'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Vintage Denim Jacket'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Premium Dog Bed XL',
    'Supportive washable bed for large dogs with non-slip base and removable outer cover.',
    68.00,
    'approved',
    NULL,
    pet.id,
    pets.id
FROM users pet
CROSS JOIN categories pets
WHERE pet.email = 'petseller@example.com'
  AND pets.name = 'Pets'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Premium Dog Bed XL'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Cat Tree with Hammock',
    'Tall scratching tower with hammock, hideout and multiple platforms for active indoor cats.',
    96.00,
    'approved',
    NULL,
    pet.id,
    pets.id
FROM users pet
CROSS JOIN categories pets
WHERE pet.email = 'petseller@example.com'
  AND pets.name = 'Pets'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Cat Tree with Hammock'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Gas Grill 4 Burner',
    'Outdoor gas grill with side shelf, cover and cast iron grates for summer gatherings.',
    430.00,
    'approved',
    NULL,
    outdoor.id,
    garden.id
FROM users outdoor
CROSS JOIN categories garden
WHERE outdoor.email = 'gardener@example.com'
  AND garden.name = 'Garden & Outdoor'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Gas Grill 4 Burner'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Raised Garden Bed Kit',
    'Easy-assemble outdoor planter kit for herbs and vegetables with weather-resistant boards.',
    120.00,
    'draft',
    NULL,
    outdoor.id,
    garden.id
FROM users outdoor
CROSS JOIN categories garden
WHERE outdoor.email = 'gardener@example.com'
  AND garden.name = 'Garden & Outdoor'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Raised Garden Bed Kit'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'Gaming PC RTX 4070 Build',
    'Custom desktop with Ryzen 7, RTX 4070, 32GB RAM and a clean airflow case for gaming and editing.',
    1650.00,
    'approved',
    NULL,
    seller2.id,
    electronics.id
FROM users seller2
CROSS JOIN categories electronics
WHERE seller2.email = 'seller2@example.com'
  AND electronics.name = 'Electronics'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'Gaming PC RTX 4070 Build'
  );

INSERT INTO listings (title, description, price, status, rejection_reason, owner_id, category_id)
SELECT
    'iPhone 14 Pro 256GB',
    'Unlocked smartphone with 87 percent battery health, original box and no display damage.',
    890.00,
    'approved',
    NULL,
    seller.id,
    electronics.id
FROM users seller
CROSS JOIN categories electronics
WHERE seller.email = 'seller@example.com'
  AND electronics.name = 'Electronics'
  AND NOT EXISTS (
      SELECT 1 FROM listings existing WHERE existing.title = 'iPhone 14 Pro 256GB'
  );

DELETE FROM listing_images
WHERE listing_id IN (
    SELECT id
    FROM listings
    WHERE title IN (
        'MacBook Pro 14 M3',
        'City Bicycle Riverside',
        'Walnut Standing Desk',
        'Math Tutoring for High School',
        'PlayStation 5 Slim Bundle',
        'Mirrorless Camera Starter Kit',
        'Weekend Cleaning Service',
        'Luxury Villa for 200',
        'Vintage Vinyl Collection',
        'Scandinavian Lounge Chair',
        'Minimal Floor Lamp',
        'Toyota Corolla 2016',
        'Electric Scooter Ninebot',
        'Sunny Studio Near Metro',
        'Coworking Desk Downtown',
        'English Speaking Club',
        'SAT Math Intensive Course',
        'Double Baby Stroller',
        'Wooden Montessori Toy Set',
        'Graphic Designer Internship',
        'Customer Support Specialist',
        'Leather Weekend Bag',
        'Vintage Denim Jacket',
        'Premium Dog Bed XL',
        'Cat Tree with Hammock',
        'Gas Grill 4 Burner',
        'Raised Garden Bed Kit',
        'Gaming PC RTX 4070 Build',
        'iPhone 14 Pro 256GB'
    )
);

INSERT INTO listing_images (listing_id, url, position)
SELECT listing.id, image.url, image.position
FROM listings listing
JOIN (
    VALUES
        ('MacBook Pro 14 M3', '/demo-images/macbook-pro-14-m3.svg', 0),
        ('City Bicycle Riverside', '/demo-images/city-bicycle-riverside.svg', 0),
        ('Walnut Standing Desk', '/demo-images/walnut-standing-desk.svg', 0),
        ('Math Tutoring for High School', '/demo-images/math-tutoring-for-high-school.svg', 0),
        ('PlayStation 5 Slim Bundle', '/demo-images/playstation-5-slim-bundle.svg', 0),
        ('Mirrorless Camera Starter Kit', '/demo-images/mirrorless-camera-starter-kit.svg', 0),
        ('Weekend Cleaning Service', '/demo-images/weekend-cleaning-service.svg', 0),
        ('Luxury Villa for 200', '/demo-images/luxury-villa-for-200.svg', 0),
        ('Vintage Vinyl Collection', '/demo-images/vintage-vinyl-collection.svg', 0),
        ('Scandinavian Lounge Chair', '/demo-images/scandinavian-lounge-chair.svg', 0),
        ('Minimal Floor Lamp', '/demo-images/minimal-floor-lamp.svg', 0),
        ('Toyota Corolla 2016', '/demo-images/toyota-corolla-2016.svg', 0),
        ('Electric Scooter Ninebot', '/demo-images/electric-scooter-ninebot.svg', 0),
        ('Sunny Studio Near Metro', '/demo-images/sunny-studio-near-metro.svg', 0),
        ('Coworking Desk Downtown', '/demo-images/coworking-desk-downtown.svg', 0),
        ('English Speaking Club', '/demo-images/english-speaking-club.svg', 0),
        ('SAT Math Intensive Course', '/demo-images/sat-math-intensive-course.svg', 0),
        ('Double Baby Stroller', '/demo-images/double-baby-stroller.svg', 0),
        ('Wooden Montessori Toy Set', '/demo-images/wooden-montessori-toy-set.svg', 0),
        ('Graphic Designer Internship', '/demo-images/graphic-designer-internship.svg', 0),
        ('Customer Support Specialist', '/demo-images/customer-support-specialist.svg', 0),
        ('Leather Weekend Bag', '/demo-images/leather-weekend-bag.svg', 0),
        ('Vintage Denim Jacket', '/demo-images/vintage-denim-jacket.svg', 0),
        ('Premium Dog Bed XL', '/demo-images/premium-dog-bed-xl.svg', 0),
        ('Cat Tree with Hammock', '/demo-images/cat-tree-with-hammock.svg', 0),
        ('Gas Grill 4 Burner', '/demo-images/gas-grill-4-burner.svg', 0),
        ('Raised Garden Bed Kit', '/demo-images/raised-garden-bed-kit.svg', 0),
        ('Gaming PC RTX 4070 Build', '/demo-images/gaming-pc-rtx-4070-build.svg', 0),
        ('iPhone 14 Pro 256GB', '/demo-images/iphone-14-pro-256gb.svg', 0)
) AS image(title, url, position)
    ON image.title = listing.title;

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

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    seller.id,
    buyer.id,
    'Yes, it is available. I can offer a small discount if you can pick it up this week.'
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
        AND existing.sender_id = seller.id
        AND existing.recipient_id = buyer.id
  );

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    buyer.id,
    seller2.id,
    'Hi! Can you confirm the shutter count and whether the original box is included?'
FROM listings listing
CROSS JOIN users buyer
CROSS JOIN users seller2
WHERE listing.title = 'Mirrorless Camera Starter Kit'
  AND buyer.email = 'buyer@example.com'
  AND seller2.email = 'seller2@example.com'
  AND NOT EXISTS (
      SELECT 1
      FROM messages existing
      WHERE existing.listing_id = listing.id
        AND existing.sender_id = buyer.id
        AND existing.recipient_id = seller2.id
  );

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    buyer2.id,
    auto.id,
    'Hello! Is the Toyota still available and can you share the VIN privately?'
FROM listings listing
CROSS JOIN users buyer2
CROSS JOIN users auto
WHERE listing.title = 'Toyota Corolla 2016'
  AND buyer2.email = 'buyer2@example.com'
  AND auto.email = 'auto@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM messages existing
      WHERE existing.listing_id = listing.id
        AND existing.sender_id = buyer2.id
        AND existing.recipient_id = auto.id
  );

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    auto.id,
    buyer2.id,
    'Yes, still available. I can send the VIN and service records after your next reply.'
FROM listings listing
CROSS JOIN users buyer2
CROSS JOIN users auto
WHERE listing.title = 'Toyota Corolla 2016'
  AND buyer2.email = 'buyer2@example.com'
  AND auto.email = 'auto@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM messages existing
      WHERE existing.listing_id = listing.id
        AND existing.sender_id = auto.id
        AND existing.recipient_id = buyer2.id
  );

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    buyer3.id,
    realtor.id,
    'Could I schedule a viewing for the studio this Thursday evening?'
FROM listings listing
CROSS JOIN users buyer3
CROSS JOIN users realtor
WHERE listing.title = 'Sunny Studio Near Metro'
  AND buyer3.email = 'buyer3@example.com'
  AND realtor.email = 'realtor@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM messages existing
      WHERE existing.listing_id = listing.id
        AND existing.sender_id = buyer3.id
        AND existing.recipient_id = realtor.id
  );

INSERT INTO messages (listing_id, sender_id, recipient_id, body)
SELECT
    listing.id,
    buyer4.id,
    tutor.id,
    'Do you offer a trial lesson before joining the English speaking club?'
FROM listings listing
CROSS JOIN users buyer4
CROSS JOIN users tutor
WHERE listing.title = 'English Speaking Club'
  AND buyer4.email = 'buyer4@example.com'
  AND tutor.email = 'tutor@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM messages existing
      WHERE existing.listing_id = listing.id
        AND existing.sender_id = buyer4.id
        AND existing.recipient_id = tutor.id
  );
