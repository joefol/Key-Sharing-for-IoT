# Key-Sharing-for-IoT
Implementation of a key sharing scheme for IoT devices as defined in this paper:

https://dl.acm.org/doi/pdf/10.1145/3508398.3511520

## Instructions

Each folder contains different key sharing schemes. Running the code will return the time it takes to complete. ECDH and RSA are implemented as benchmarks to compare to our implementation of the proposed key sharing scheme outlined in the research paper.

- Under ECDH, run the server and client files in a terminal and it will output the time it takes for each party to calculate the shared key.
- Under RSA, run the server and client in a terminal and it will output the time taken to generate and send the public key across the network.
- Under Pi is our implementation. 
    - Run the server file and client file in a terminal to establish a connection. 
    - The time it takes to derive a session key will be outputted.
    - After a session key is established between the client and server, you will be able to send encrypted messages to the server.
    - The server then decrypts any incoming messages with the key and outputs them.
    - Encryption and decryption are done using AES-256 with CBC mode.

## Analysis
Each implementation (RSA, ECDH, Pi) were ran 20 times. Listed below are the average times in seconds for each. See the 'Key_Sharing_Data' text file in the repo for all data collected. 

- RSA:
    - 10.63924192 seconds
- ECDH:
    - 0.456192446 seconds
- Pi:
    - 0.159353876 seconds