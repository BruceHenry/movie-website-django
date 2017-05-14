CREATE  TRIGGER add_seen after INSERT ON movie_seen
BEGIN
  DELETE FROM movie_expect WHERE movieid_id=new.movieid_id AND username=new.username;
END;

CREATE  TRIGGER add_expect after INSERT ON movie_expect
BEGIN
  DELETE FROM movie_seen WHERE movieid_id=new.movieid_id AND username=new.username;
END;