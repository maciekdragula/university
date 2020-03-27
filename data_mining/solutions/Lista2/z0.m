# Postawiłem średniki w prostych przykładach, więc po uruchomieniu tego skryptu
# powinny zostać wypisane tylko wielkości e, D i E

a = 1:100;
b = 1:2:99;
c = pi * (-1:0.01:1);
d = pi * [-1:0.01:-0.01, 0.01:0.01:1];
e = arrayfun(@(ei)(ei * ((ei > 0) == 1)), sin(1:100))
A = reshape(1:100, 10, 10);
B = diag(1:100, 0) + diag(99:-1:1, -1) + diag(99:-1:1, 1);
C = triu(ones(7));
D = reshape([arrayfun(@(i)(sum(1:i)), 1:100), arrayfun(@(i)(factorial(i)), 1:100)], 100, 2).'
[x, y] = meshgrid(1:100, 1:100);
E = (mod(x, y) == 0)