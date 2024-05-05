.. include:: substitutions.rst

Conclusion
==========

The Bracha-Toueg k-crash consensus algorithm offers a valuable method for achieving consensus in distributed systems, particularly where up to half of the processes may experience crashes. The implementation on the AHCv2 platform demonstrated that while the algorithm is highly effective under specified conditions, its performance degrades beyond the theoretical crash fault limit. Future work could explore optimizations or hybrid models that incorporate features from other consensus protocols to extend fault tolerance or reduce message complexity. Further investigations into adaptive algorithms that dynamically adjust to varying network conditions and process reliability might also enhance practical implementations in real-world distributed systems.