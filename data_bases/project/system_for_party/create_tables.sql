CREATE TABLE all_ids (
  id int NOT NULL PRIMARY KEY,
  TYPE id_type
);

CREATE TABLE members (
  member_id int NOT NULL PRIMARY KEY REFERENCES all_ids (id),
  password_hash text NOT NULL,
  last_activity TIMESTAMP NOT NULL,
  upvotes int NOT NULL DEFAULT 0,
  downvotes int NOT NULL DEFAULT 0
);

CREATE TABLE leaders (
  leader_id int NOT NULL PRIMARY KEY REFERENCES members (member_id)
);

CREATE TABLE projects (
  project_id int NOT NULL PRIMARY KEY REFERENCES all_ids (id),
  authority_id int NOT NULL REFERENCES all_ids (id)
);

CREATE TABLE actions (
  action_id int NOT NULL PRIMARY KEY REFERENCES all_ids (id),
  action action_type,
  project_id int NOT NULL REFERENCES all_ids (id),
  member_id int NOT NULL REFERENCES all_ids (id),
  upvotes int NOT NULL DEFAULT 0,
  downvotes int NOT NULL DEFAULT 0
);

CREATE TABLE votes (
  action_id int NOT NULL REFERENCES actions (action_id),
  member_id int NOT NULL REFERENCES members (member_id),
  vote vote_type,
  PRIMARY KEY (action_id, member_id)
);

CREATE VIEW trolls AS (
  SELECT
    *
  FROM (
    SELECT
      member_id,
      sum(a.upvotes) upvotes,
      sum(a.downvotes) downvotes
    FROM
      members m
      JOIN actions a USING (member_id)
    GROUP BY
      member_id) sub
  WHERE
    downvotes - upvotes > 0
  ORDER BY
    downvotes - upvotes DESC,
    member_id ASC)
