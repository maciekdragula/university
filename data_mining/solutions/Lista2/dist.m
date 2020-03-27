function [dists] = dist(X, Y)
  x = sum(X.^2, 1);
  y = sum(Y.^2, 1);
  dists = sqrt(x.' + y - 2 * X.' * Y);
end