CREATE TABLE download (
  id VARCHAR(50) NOT NULL PRIMARY KEY,
  title VARCHAR(50) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  institution VARCHAR(500) NOT NULL,
  scientific_purposes_only BOOLEAN NOT NULL,
  requested_date DATETIME NOT NULL
)
