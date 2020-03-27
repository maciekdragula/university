function [res] = weighted_avg(x, w)
  n = length(x);
  res = x.' * w / n;
 end