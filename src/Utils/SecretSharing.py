from Crypto.Protocol.SecretSharing import Shamir

secret = 28
print("\nSecret: ", secret, "\n")
shares = Shamir.split(4, 6, secret)

shares2 = []

print("Generated Shares:")
for i in range(len(shares)):
    print(shares[i])
    shares2.append(shares[i])

reconstructed_secret = Shamir.combine(shares2)
reconstructed_secret = int.from_bytes(reconstructed_secret, 'big')
print("\nReconstructed Secret:", reconstructed_secret)