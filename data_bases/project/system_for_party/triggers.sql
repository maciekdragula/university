CREATE FUNCTION update_action_votes ()
  RETURNS TRIGGER
  AS $update_action_votes$
BEGIN
  UPDATE
    actions
  SET
    upvotes = upvotes + 1
  WHERE
    action_id = NEW.action_id
    AND NEW.vote = 1;
  UPDATE
    actions
  SET
    downvotes = downvotes + 1
  WHERE
    action_id = NEW.action_id
    AND NEW.vote = - 1;
  RETURN NEW;
END
$update_action_votes$
LANGUAGE plpgsql;

CREATE FUNCTION update_members_votes ()
  RETURNS TRIGGER
  AS $update_members_votes$
BEGIN
  UPDATE
    members
  SET
    upvotes = upvotes + 1
  WHERE
    member_id = NEW.member_id
    AND NEW.vote = 1;
  UPDATE
    members
  SET
    downvotes = downvotes + 1
  WHERE
    member_id = NEW.member_id
    AND NEW.vote = - 1;
  RETURN NEW;
END
$update_members_votes$
LANGUAGE plpgsql;

CREATE TRIGGER update_action_votes_trigger
  AFTER INSERT ON votes
  FOR EACH ROW
  EXECUTE PROCEDURE update_action_votes ();

CREATE TRIGGER update_member_votes_trigger
  AFTER INSERT ON votes
  FOR EACH ROW
  EXECUTE PROCEDURE update_members_votes ();

