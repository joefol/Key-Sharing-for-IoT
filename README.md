# Key-Sharing-for-IoT
Implementation of a key sharing scheme for IoT devices as defined in this paper:

https://dl.acm.org/doi/pdf/10.1145/3508398.3511520

## Instructions

Each folder contains different key sharing schemes. Running the code will return the time it takes to complete. ECDH and RSA are implemented as benchmarks to compare to our implementation of the proposed key sharing scheme outlined in the research paper.

- Under ECDH, run the server and client files in a terminal and it will output the time it takes for each party to calculate the shared key.
- Under RSA, run the server and client in a terminal and it will output the time taken to generate and send the public key across the network.
- Under Pi is our implementation. As of now it is still a work in progress.