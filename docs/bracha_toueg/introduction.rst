.. include:: substitutions.rst

Introduction
============

In a distributed system, where processes potentially live on different computers, sometimes the system may end up at a distinction point at which the system must choose which road it will go. Since processes are partitioned across the network, resolving this distinction may not always be trivial. This is where consensus algorithms come in, ensuring all the working parts of the system can agree on a specific course of action, even when some parts fail.

Depending on the business logic and requirements, distributed systems choose how much they take action individually or collectively. For example, if the distributed system is the database of a bank, any withdrawal first must be approved by distributed processes before approved in order to prevent the double spending problem. Otherwise, the bank wouldn’t live long. On the other hand, if it is the number of comments a Youtube video has, a slight error wouldn’t make much difference. Therefore, distributed parties may take action individually trading off consistency for performance.

However, as Murphy’s Law states “ Anything that can go wrong, will go wrong”. That is, in a distributed system processes will fail. In fact, statistically speaking, there will be much more failure than a single system as the number of distributed processes increases. Therefore, while designing the system, it should be engineered by considering it will fail. One key method for achieving this is the Bracha-Toueg Crash Consensus Algorithm, designed to help the system reach a common decision, even if up to k processes crash where k is less than half of the number of total processes.

There are many consensus algorithms. However, they all have different characteristics. Some can arrive at a consensus faster but become unavailable meanwhile. Whereas some can tolerate less number of crashers but require less message passing. The point is that the Bracha-Toueg Crash Consensus Algorithm is not the only algorithm that solves this problem. It just solves it differently so that we as engineers can choose it when suitable.

The Bracha-Toueg Crash Consensus Algorithm requires that up to k processes, where k is less than the half of the total number of processes, fail at any point to keep the system consistent and reliable. If there are more processes crashing, it will not be able to keep the system reliable.

In this study, I will implement the Bracha-Toueg Crash Consensus Algorithm on the AHCv2 platform to test how well it works under different challenging conditions, such as crashes, delays in communication, and changes in the network structure. I want to see if the algorithm could still help the system agree on important decisions, keep everything running smoothly, and recover quickly from any problems.
