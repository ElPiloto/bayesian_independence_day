# Bayesian Independence Day

This repository aims to simulate the game Escape From The Aliens In Outer Space


## Overview

### What game are we trying to solve?

The board game is called "Escape From the Aliens In Outer Space". It's a mix
between Werewolf and Battleship. Players are randomly assigned to be aliens or
humans. You don't know who the other aliens or humans are. The aliens need to
kill all the humans. The humans need to reach an escape pod before they're
killed. Importantly, there is no shared board. Instead, each player tracks
their own location. As they move around the board, they may be forced to
announce their current location, announce a decoy location of their choosing,
announce the type of location (i.e. silent sector or danger sector) they are
in. An important aspect is that it is not possible to tell the difference
between a player that was forced to reveal their true location and a player
that was allowed to say a decoy location. If they do certain actions like
attack or try to use an escape pod, they also announce their true location.
However, for these actions it is very clear that this is the true location
because of the accompanying action.


### What Do We Mean By Solve?

Given the information accumulated over a set of turns, we want to predict two things:  
1. Is a player human or alien?  
2. Where is the player?

For now, that's all we really care about. If we want to _solve_ solve this
game, we'd have to come up with the best policy for controlling our own player,
trying to intercept or fake out other players, etc. That's a whole can of worms
-- no, thanks.


### What's Our Approach?

KISS: we're gunna keep things real stupid simple. We're not going to use real
maps from the game, we're not going to use items.
