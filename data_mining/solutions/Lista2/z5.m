wins_stay = 0;
wins_switch = 0;
for i = 1:10000
  player = randi(3);
  perm = randperm(3);
  car = perm(1);
  if player == perm(2);
    open_goat = perm(3);
    closed_goat = perm(2);
  else
    open_goat = perm(2);
    closed_goat = perm(3);
  end
  if player == car
    wins_stay++;
  else
    wins_switch++;
  end
end
wins_stay/10000
wins_switch/10000