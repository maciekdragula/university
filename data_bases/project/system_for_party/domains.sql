CREATE DOMAIN id_type AS text NOT NULL CHECK (
  VALUE IN ('member',
    'action',
    'project',
    'authority')
);

CREATE DOMAIN action_type AS text NOT NULL CHECK (
  VALUE IN ('support',
    'protest')
);

CREATE DOMAIN vote_type AS int NOT NULL CHECK (
  VALUE IN (1,
    - 1)
);

