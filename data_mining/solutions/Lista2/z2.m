X = rand(100, 10000);
Y = rand(100, 1000);

tic
  D = dist(X, Y);
time_elapsed = toc
all(size(D) == [10000, 1000])