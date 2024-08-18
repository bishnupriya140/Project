def main():
    data = "0101010001101001"  # Example binary representation of "Hi"
    key = "1010111100101001"

    encrypted_data = encrypt_decrypt(data, key)
    digital_signature = generate_digital_signature(encrypted_data)
    print("\nDigital Signature:", digital_signature)


# Perform initial permutation (reverse order of data)
def initial_permutation(data):
    return data[::-1]
# Divide the 16-bit block into two 8-bit parts
def divide_block(data):
    LPT = data[:8]
    RPT = data[8:]
    return LPT, RPT
# Convert the 16-bit key (4 bits each block) into a 12-bit key
def convert_key(key):
    return key[:4] + key[8:12] + key[4:8]
# Expand the 8-bit RPT to 12-bits RPT
def expand_rpt(RPT):
    return RPT[:4] + RPT + RPT[4:]
# XOR operation between RPT and the key
def xor_operation(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))
# Apply S-Box substitutions using the specified table
def sbox_substitution(input):
    sbox_table = [
        "1010", "0110", "1001", "0011",
        "0111", "1011", "1000", "1110",
        "0000", "0001", "1111", "1100",
        "1101", "0100", "0010", "0101"
    ]

    result = []
    for i in range(0, len(input), 4):
        chunk = input[i:i + 4]
        index = int(chunk, 2)
        result.append(sbox_table[index])

    return ''.join(result)


# P-box permutation, swapping two consecutive bits
def pbox_permutation(input):
    result = []
    for i in range(0, len(input), 2):
        result.append(input[i + 1])
        result.append(input[i])
    return ''.join(result)


# Perform the encryption/decryption
def encrypt_decrypt(data, key):
    print("Original Data:", data)
    data = initial_permutation(data)
    print("After Initial Permutation:", data)

    LPT, RPT = divide_block(data)
    print("LPT:", LPT, ", RPT:", RPT)

    key = convert_key(key)
    print("12-bit Key:", key)

    for round in range(4):
        print("\nRound", round + 1, ":")
        expanded_RPT = expand_rpt(RPT)
        print("Expanded RPT:", expanded_RPT)

        RPT = xor_operation(expanded_RPT, key)
        print("After XOR with Key:", RPT)

        RPT = sbox_substitution(RPT)
        print("After S-Box Substitution:", RPT)

        RPT = pbox_permutation(RPT)
        print("After P-Box Permutation:", RPT)

        LPT, RPT = RPT[:8], xor_operation(RPT[:8], LPT)
        print("After XOR with LPT and Swap: LPT=", LPT, ", RPT=", RPT)

    combined_data = LPT + RPT
    print("\nCombined Data before Final Permutation:", combined_data)

    combined_data = initial_permutation(combined_data)
    print("After Final Permutation:", combined_data)

    return combined_data

# Digital Signature: Apply the hash function
def generate_digital_signature(data):
    md = int(data, 2) >> 2
    return f"{md:016b}"


if __name__ == "__main__":
    main()
