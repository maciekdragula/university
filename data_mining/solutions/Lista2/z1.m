x = rand(100, 1);
y = rand(100, 1);
w = rand(100, 1);
vec_len(x)
weighted_avg(x, w)
euclid_dist(x, y)
dot_product(x, y)

X = rand(100, 1000);

v1 = sqrt(diag(X.' * X));
all(size(v1) == [1000, 1])

v2 = X.' * w / length(w);
all(size(v2) == [1000, 1])

v3 = sqrt(diag((X - y).' * (X - y)));
all(size(v3) == [1000, 1])

v4 = y.' * X;
all(size(v3) == [1000, 1])