CREATE DATABASE shopverse CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'shopverse_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON shopverse.* TO 'shopverse_user'@'localhost';
FLUSH PRIVILEGES;
