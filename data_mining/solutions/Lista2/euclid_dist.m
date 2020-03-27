function [res] = euclid_dist(x, y)
  d = x - y;
  res = sqrt(d.' * d);
 end