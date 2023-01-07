mask_to_order = [0, 1, 8, 9, 2, 3, 10, 11, 16, 17, 24, 25, 18, 19, 26, 27, 4, 5, 12, 13, 6, 7, 14, 15, 20, 21, 28, 29, 22, 23, 30, 31, 32, 33, 40, 41, 34, 35, 42, 43, 48, 49, 56, 57, 50, 51, 58, 59, 36, 37, 44, 45, 38, 39, 46, 47, 52, 53, 60, 61, 54, 55, 62, 63, 64, 65, 72, 73, 66, 67, 74, 75, 80, 81, 88, 89, 82, 83, 90, 91, 68, 69, 76, 77, 70, 71, 78, 79, 84, 85, 92, 93, 86, 87, 94, 95, 96, 97, 104, 105, 98, 99, 106, 107, 112, 113, 120, 121, 114, 115, 122, 123, 100, 101, 108, 109, 102, 103, 110, 111, 116, 117, 124, 125, 118, 119, 126, 127, 128, 129, 136, 137, 130, 131, 138, 139, 144, 145, 152, 153, 146, 147, 154, 155, 132, 133, 140, 141, 134, 135, 142, 143, 148, 149, 156, 157, 150, 151, 158, 159, 160, 161, 168, 169, 162, 163, 170, 171, 176, 177, 184, 185, 178, 179, 186, 187, 164, 165, 172, 173, 166, 167, 174, 175, 180, 181, 188, 189, 182, 183, 190, 191, 192, 193, 200, 201, 194, 195, 202, 203, 208, 209, 216, 217, 210, 211, 218, 219, 196, 197, 204, 205, 198, 199, 206, 207, 212, 213, 220, 221, 214, 215, 222, 223, 224, 225, 232, 233, 226, 227, 234, 235, 240, 241, 248, 249, 242, 243, 250, 251, 228, 229, 236, 237, 230, 231, 238, 239, 244, 245, 252, 253, 246, 247, 254, 255]

def get_braille(mask):
    return chr(0x2800+mask_to_order[mask])

if __name__ == '__main__':
    print(''.join(get_braille(((i>>0&1)<<0)|((i>>1&1)<<2)|((i>>2&1)<<4)|((i>>3&1)<<6)) for i in range(16)))