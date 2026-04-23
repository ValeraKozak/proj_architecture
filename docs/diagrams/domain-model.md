# Domain Model

## UML / доменна модель у текстовому вигляді
- `User` 1..* `Listing`
- `Category` 1..* `Listing`
- `Listing` 1..* `Message`
- `User` 1..* `Message` як `sender`
- `User` 1..* `Message` як `recipient`

## Атрибути
- `User`: id, email, full_name, password_hash, role, is_blocked
- `Category`: id, name, description
- `Listing`: id, title, description, price, status, rejection_reason
- `Message`: id, listing_id, sender_id, recipient_id, body

