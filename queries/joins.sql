-- SELECT 
-- users.id, COUNT(posts.id)
-- FROM posts 
-- RIGHT JOIN users
-- ON posts.user_id = users.id
-- GROUP BY users.id

SELECT * 
FROM posts
LEFT JOIN votes
ON votes.post_id = id
LEFT JOIN users
on votes.user_id = users.id

