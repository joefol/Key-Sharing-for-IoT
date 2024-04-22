from secretsharing import SecretSharer

#TODO implement basic t out of n scheme using shamir's secret sharing from secretsharing python library

secret = input("Enter a secret: ")
threshold = 3
numShares = 5

shares = SecretSharer.split_secret(secret, threshold, numShares)

print("Generated Shares:")
for share in shares:
    print(share)

availableShares = shares[:3]

reconstructedSecret = SecretSharer.recover_secret(availableShares)
print("\nReconstructed Secret:", reconstructedSecret)