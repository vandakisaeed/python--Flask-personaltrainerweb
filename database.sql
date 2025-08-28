-- --CREATE database PersonalWebsite
-- -- PERSONAL_INFO TABLE
 -- CREATE TABLE personal_info (info_id SERIAL PRIMARY KEY,
--                                            full_name VARCHAR(100),
--                                                      bio TEXT, location VARCHAR(100),
--                                                                         email VARCHAR(100),
--                                                                               picture TEXT);
 -- -- PROJECTS TABLE
 -- CREATE TABLE projects (project_id SERIAL PRIMARY KEY,
--                                          project_name VARCHAR(200) NOT NULL,
--                                                                    demo_url TEXT, image TEXT, description TEXT);
 -- -- USERS TABLE
 -- CREATE TABLE users (user_id SERIAL PRIMARY KEY,
--                                    username VARCHAR(50) NOT NULL UNIQUE,
--                                                                  password VARCHAR(255) NOT NULL,
--                                                                                        email VARCHAR(100));
 -- Replace the values with your information!
 -- INSERT INTO public.personal_info (full_name, bio, location, email, picture)
-- VALUES ('Paddington Bear', 'A well-mannered bear from Darkest Peru, fond of marmalade sandwiches and adventures.', 'Darkest Peru', 'paddington@bearmail.com', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8YXdveMvNNCsr0p4hh2eOLG1rtEYu6rdq5GY6yPQxirDDM_gxUHzQ8sUbZa9Ek3w3Jwg&usqp=CAU');
 -- INSERT INTO projects (project_name, demo_url, image, description)
-- VALUES -- Project 1
-- ('Project 1', 'https://demo.com', 'https://placehold.co/600x400', 'Some description'),
--                    -- Project 2
-- ('Project 2', 'https://demo.com', 'https://placehold.co/600x400', 'Some description');

INSERT INTO users (username, password, email)
VALUES ('admin', 'scrypt:32768:8:1$eCkVMqBV8gmC94n5$b49c08f059f9eaf2031fd21bba69e84240ac01c0bf5c3b909f9d82da817773212c7cd97945bdecb81065b9dd0ad5b09c881373c0757ff278d8b1dd9322dfc85e', 'admin@email.com');