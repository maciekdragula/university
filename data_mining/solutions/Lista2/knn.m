function [res] = knn(X, Y, k)
  dists = dist(X, Y);
  [out, idx] = sort(dists.', 1);
  res = idx(1:k, :);
end  