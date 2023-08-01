-- SELECT 
-- users.id, COUNT(posts.id)
-- FROM posts 
-- RIGHT JOIN users
-- ON posts.user_id = users.id
-- GROUP BY users.id

-- SELECT * 
-- FROM posts
-- LEFT JOIN votes
-- ON votes.post_id = id
-- LEFT JOIN users
-- on votes.user_id = users.id

SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.user_id AS posts_user_id, count(posts.user_id) AS users
FROM posts LEFT OUTER JOIN users ON posts.user_id = users.id GROUP BY posts.id