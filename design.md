# Data

## User

- first name
- last name
- email
- password

## Links

- url
- user
- order
- description

## Notes

- title
- content
- user
- created date
- last updated

# Routes

## Public Routes

### POST `/login`

#### request

- email
- password

#### response

- token

### POST `/register`

#### request

- email
- first name
- last name
- password

## Private Routes

Assume that request is sent with user token. Return unauthorized otherwise.

### GET `/user`

#### request

- None

#### response

- id
- email
- first name
- last name

### PATCH `/user`

#### request

Subset of:

- email
- first name
- last name
- password

#### response

- id
- email
- first name
- last name

### GET `/links`

#### request

- None

#### response

List of:

- id
- url
- description

### POST `/links`

#### request

- url
- description

#### response

- None

### PATCH `/links`

Primarily used to order links

#### request

List of:

- id
- url
- description

#### response

List of:

- id
- url
- description

### GET `/links/:id`

#### request

- id

#### response

- id
- url
- description

### PATCH `/links/:id`

#### request

- url
- description

#### response

- id
- url
- description

### DELETE `/links/:id`

#### request

- id

#### response

- None

### GET `/notes`

#### request

- None

#### response

List of:

- id
- title
- contents
- created on
- last updated

### POST `/notes`

#### request

- title
- contents

#### response

- None

### GET `/notes/:id`

#### request

- id

#### response

- id
- title
- contents
- created on
- last updated

### PATCH `/notes/:id`

#### request

- title
- contents

#### response

- id
- title
- contents
- created on
- last updated

### DELETE `/notes/:id`

#### request

- id

#### response

- None
