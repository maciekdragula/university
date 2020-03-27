X = rand(8, 50);
Y = rand(8, 70);
all(size(knn(X, Y, 5)) == [5, 50])