
--Nombre de la base de datos MySQL: tweets
--Nombre de usuario MySQL: diego
--Contraseña de usuario MySQL:  qVG!E4vuCzV#bu2y
--Verifique contraseña de usuario MySQL:

--Correo electrónico: innovcr2023@gmail.com
--host: db4free.net

CREATE TABLE usuarios (
  id INT AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
  nombre (hashtag)
);


CREATE TABLE tweets (
  id VARCHAR(255) PRIMARY KEY,
  texto TVARCHAR(1000) NOT NULL,
  feeling INT DEFAULT -2,
  fecha DATE,
  retweets INT,
  favoritos INT,
  usuario INT,
  FOREIGN KEY (usuario) REFERENCES usuarios(id)
);


CREATE TABLE hashtags (
  id INT AUTO_INCREMENT,
  hashtag VARCHAR(255) NOT NULL,
PRIMARY KEY (id),
UNIQUE (hashtag)
);



CREATE TABLE tweet_hashtags (
  tweet_id VARCHAR(255),
  hashtag_id INT,
  PRIMARY KEY (tweet_id, hashtag_id),
  FOREIGN KEY (tweet_id) REFERENCES tweets(id),
  FOREIGN KEY (hashtag_id) REFERENCES hashtags(id)
);








