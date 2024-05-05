.. include:: substitutions.rst

Implementation, Results and Discussion
======================================

Implementation and Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To test the Bracha-Toueg k-crash consensus algorithm, I implemented it on the AHCv2 platform. The implementation involved simulating a distributed system with variable process counts and failure rates. Each process was designed to execute its instance of the algorithm, handling inputs and broadcasting outputs according to the algorithm's specifications. Failures were randomly introduced based on predefined probabilities to simulate crash faults.

The methodology included detailed logging of all message exchanges and state changes to trace the decision-making process accurately. Testing scenarios varied the number of processes (n), the maximum number of allowable process crashes (k), and network latency to simulate different communication delays and disruptions.

Results
~~~~~~~~

Results indicated that the Bracha-Toueg algorithm performed robustly under conditions with fewer than N/2 crashes. Decision convergence times increased with the number of processes but remained within acceptable limits for up to 50% crash conditions. Under higher crash conditions, the system sometimes failed to reach consensus, illustrating the algorithm's limitations as predicted by theory.

Discussion
~~~~~~~~~~

The testing confirmed that the Bracha-Toueg algorithm is highly effective in environments with a predictable upper limit on crash faults. It successfully enabled a distributed consensus even with significant communication delays and disruptions, proving its robustness. The algorithm's resilience to failures supports its application in critical real-time systems where consensus is crucial for maintaining system integrity and availability.
