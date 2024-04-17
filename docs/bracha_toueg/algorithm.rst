.. include:: substitutions.rst

|Bracha-Toueg|
=========================================



Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As explained in [Fokking2013]_ as below:

The Bracha-Toueg k-crash consensus algorithm, for k < N/2 , progresses in rounds. Initially,
at the start of round 0, each process randomly chooses a value 0 or 1. The
weight of a process, holding value b which is either 0 or 1, approximates from below the number
of processes that voted b in the previous round. In round 0, each  process has weight 1.
In each round n >= 0, each correct, undecided process p sends its value and
weight to all processes, and determines a new value and weight, based on the first
N - k messages it receives in this round:

- p sends n, value_p, weight_p to all processes (including itself).
- p waits until N - k messages <n, b,w> have arrived. (It purges/stores messages from earlier/future rounds.)
- If w > N / 2 for an incoming message <n, b,w>, then value_p ← b. Otherwise, value_p ← 0 if most messages voted 0, or else value_p ← 1.
- weight_p is changed into the number of incoming votes for value_p in round n.
- If w > N / 2 for more than k incoming messages <n, b,w>, then p decides for b.

If p decides for b in round n, it broadcasts <n+1, b,N-k> and <n+2, b,N-k>, and
terminates. This suffices because when a process decides, all other correct processes
are guaranteed to decide within two rounds.


Distributed Algorithm: |Bracha-Toueg| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _BlindFloodingAlgorithmLabel:

.. code-block:: RST
    :linenos:
    :caption: The Bracha-Toueg k-crash consensus algorithm

    OnInit: () do
        ramdomly choose value as either 0 or 1
        weight ← 1
        send ( 0, value, weight )
    
    OnMessage at round r: ( r ) do
        send  ( r, value, weight )

        wait for N - k messages ( r, b, w )
        if w > N / 2 for more than k incoming messages then
            value ← b
            send ( r + 1, value, N - k ) 
            send ( r + 2, value, N - k )
        if w > N / 2 for any of N - k messages then
            value ← b
            weight ← total_w_b
            send ( r + 1, value, weight )
        else
            if total_w_0 > total_w_1 then
                value ← 0
                weight ← total_w_0 - total_w_1
            else
                value ← 1
                weight ← total_w_1 - total_w_0
            send ( r + 1, value, weight )


Do not forget to explain the algorithm line by line in the text.

Example
~~~~~~~~

Below example is taken from [Fokking2013]_:

Given a network of three processes p, q, r, and k = 1. Each round a
process requires two incoming messages to determine a new value and weight, and
two b-votes with weight 2 to decide for b. We consider one possible computation of
the Bracha-Toueg 1-crash consensus algorithm on this network.
    - Initially, p and q randomly choose the value 0 and r the value 1, all three with weight 1.
    - In round 0, p takes into account the messages from p and r; it sets its value to 1, and its weight to 1. Moreover, q and r both take into account the messages from p and q; they set their value to 0, and their weight to 2.
    - In round 1, q takes into account the messages from q and r; since both messages carry weight 2, it decides for 0. Moreover, p and r both take into account the messages from p and r; since the message from r carries weight 2, they set their value to 0, and their weight to 1.
    - At the start of round 2, q crashes. So p and r can take into account only the messages from p and r; as a result, they set their value to 0, and their weight to 2.
    - In round 3, p and r can again only take into account the messages from p and r; since both messages carry weight 2, they decide for 0.
    - p and r send messages with value 0 and weight 2 for two more rounds, and terminate.

Correctness
~~~~~~~~~~~

If scheduling of messages is fair, then the Bracha-Toueg k-crash consensus
algorithm, for any k < N/2 , is a Las Vegas algorithm that terminates with
probability one.

This theorem is proved in [Fokking2013]_ as below:

First we prove that processes cannot decide for different values. Then we
prove that the algorithm terminates with probability one, under the assumption that
scheduling of messages is fair, meaning that each possible order of delivery of the
messages in a round occurs with a positive probability.

Suppose a process p decides for a value b at the end of a round n. Then at the start
of round n, value_q = b and weight_q > N/2 for more than k processes q. Since in every
round, each correct, undecided process ignores messages from only k processes, in
round n these processes all take into account a message <q, b,w> with w > N/2 . So in
round n+1, all correct processes vote b. So in round n+2, all correct processes vote
b with weight N - k. Hence, after round n + 2, all correct processes have decided
for b. To conclude, all correct processes decide for the same value.

Due to fair scheduling, in each round there is a positive probability that all processes
receive the first N - k messages from the same N - k processes. After such
a round n, all correct processes have the same value b. Then after round n + 1, all
correct processes have the value b with weight N - k. And after round n + 2, all
correct processes have decided for b. In conclusion, the algorithm terminates with
probability one.

Complexity 
~~~~~~~~~~

TODO: Present theoretic complexity results in terms of number of messages and computational complexity.

.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
