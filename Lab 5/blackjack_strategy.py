def build_blackjack_strategy():
  # Encode the blackjack table into 2 dictionaries
  blackjack_strategy = dict()
  numerical_cards = {"TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9}
  all_cards = {"ACE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10}
  numerical_sums = list(range(5, 22))
  # ACE-X pattern
  for x, x_num in numerical_cards.items():
    for y, y_num in all_cards.items():
      z = "H"
      if (x_num in [2, 3, 4, 5, 6, 7] and y_num in [5, 6]) or (x_num in [4, 5, 6, 7] and y_num in [4]) or (x_num in [6, 7] and y_num in [3]):
        z = "D"
      elif (x_num in [8, 9, 10]) or (x_num in [7] and y_num in [2, 7, 8]):
        z = "S"
      blackjack_strategy[(y, "ACE", x)] = z
  
  # DOUBLE pattern X-X
  for x, x_num in all_cards.items():
    for y, y_num in all_cards.items():
      z = "H"
      if (x_num in [1, 8]) or (x_num in [7, 8, 9] and y_num in [2, 3, 4, 5, 6]) or (x_num in [6] and y_num in [3, 4, 5, 6]) or (x_num in [7, 8] and y_num in [7]) or (x_num in [9] and y_num in [8, 9]) or (x_num in [2, 3] and y_num in [4, 5, 6, 7]):
        z = "P"
      elif (x_num in [10] or (x_num in [9] and y_num in [7, 10, 1])):
        z = "S"
      elif (x_num in [5] and y_num in [2, 3, 4, 5, 6, 7, 8, 9]):
        z = "D"
    
      blackjack_strategy[(y, x, x)] = z
  
  # Remaining numerical sums
  for x_num in numerical_sums:
    for y, y_num in all_cards.items():
      z = "H"
      if (x_num in [17, 18, 19, 20, 21]) or (x_num in [13, 14, 15, 16] and y_num in [2, 3, 4, 5, 6]) or (x_num in [12] and y_num in [4, 5, 6]):
        z = "S"
      elif (x_num in [16] and y_num in [9, 10, 1]) or (x_num in [15] and y_num in [10]):
        z = "Su"
      elif (x_num in [9] and y_num in [3, 4, 5, 6]) or (x_num in [10, 11] and y in [2, 3, 4, 5, 6, 7, 8, 9]) or (x_num in [11] and y_num in [10]):
        z = "D"

      blackjack_strategy[(y, x_num)] = z

  print(blackjack_strategy)

  

build_blackjack_strategy()