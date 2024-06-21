#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

# Constants
digital_edition_price = 389
disc_edition_price = 399
aaa_game_price = 75
indie_game_price = 25
number_aaa_games = 6
number_indie_games = 4
discount_rate = 0.60  # 60% of the time, there's a deal
deal_discount = 0.15  # Average deal discount for games, 15%

# Calculations
## Digital
digital_aaa_total = aaa_game_price * number_aaa_games * (1 - (discount_rate * deal_discount))
digital_indie_total = indie_game_price * number_indie_games
digital_total_cost = digital_edition_price + digital_aaa_total + digital_indie_total

## Disc - Assuming deals apply to physical copies more frequently
disc_aaa_discounted = aaa_game_price * (1 - deal_discount) * number_aaa_games * discount_rate
disc_aaa_full_price = aaa_game_price * number_aaa_games * (1 - discount_rate)
disc_aaa_total = disc_aaa_discounted + disc_aaa_full_price
disc_indie_total = indie_game_price * number_indie_games  # Assuming indie games remain digital
disc_total_cost = disc_edition_price + disc_aaa_total + disc_indie_total

# Data
labels = ['Digital Edition', 'Disc Edition']
costs = [digital_total_cost, disc_total_cost]

# Plot
fig, ax = plt.subplots()
bar_plot = ax.bar(labels, costs, color=['blue', 'green'])

# Adding the numerical data
ax.bar_label(bar_plot, padding=3, fmt='%.2f')

# Setting the title and labels
ax.set_ylabel('Total Cost ($)')
ax.set_title('Total Cost of PS5 + 10 Games Over 2 Years')

plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to not cut off labels

plt.show()
