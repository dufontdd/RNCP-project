-- ---------------------------------------------------
-- Manhwa Project: Initial Data Seed
-- ---------------------------------------------------

-- ------------------ USERS ------------------
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
)
VALUES
(
    '00000000-0000-0000-0000-000000000001',
    'Admin',
    'User',
    'admin@manhwa.com',
    '$2b$12$BNxZotWCx8OmVkEac8ejxuQUzqd7C8sa3UbvBzD8whvWpLpHeQeUS',
    1,
    datetime('now'),
    datetime('now')
);

-- ------------------ GENRES ------------------
INSERT INTO genres (id, name, description, created_at, updated_at)
VALUES
('11111111-1111-1111-1111-111111111111','Action','Combats et scènes d''action intenses',datetime('now'),datetime('now')),
('22222222-2222-2222-2222-222222222222','Fantasy','Mondes imaginaires et magie',datetime('now'),datetime('now')),
('33333333-3333-3333-3333-333333333333','Romance','Histoires d''amour et relations',datetime('now'),datetime('now'));

-- ------------------ MANHWAS ------------------
INSERT INTO manhwas (
    id,
    title,
    author,
    description,
    created_at,
    updated_at
)
VALUES
(
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'Solo Leveling',
    'Chugong',
    'Un chasseur de rang E devient le plus puissant des chasseurs.',
    datetime('now'),
    datetime('now')
);

-- ------------------ MANHWA_GENRE ------------------
INSERT INTO manhwa_genre (manhwa_id, genre_id)
VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa','11111111-1111-1111-1111-111111111111'),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa','22222222-2222-2222-2222-222222222222');

-- ------------------ REVIEWS ------------------
INSERT INTO reviews (
    id,
    text,
    user_id,
    manhwa_id,
    created_at,
    updated_at
)
VALUES
(
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    'Une histoire captivante, les combats sont incroyables !',
    '00000000-0000-0000-0000-000000000001',
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    datetime('now'),
    datetime('now')
);
