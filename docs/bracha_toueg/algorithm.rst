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



Present any background information survey the related work. Provide citations.

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

TODO: Provide an example for the distributed algorithm.

Correctness
~~~~~~~~~~~

TODO: Present Correctness, safety, liveness and fairness proofs.


Complexity 
~~~~~~~~~~

TODO: Present theoretic complexity results in terms of number of messages and computational complexity.

.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
