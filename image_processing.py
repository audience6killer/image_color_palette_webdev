import numpy as np
from PIL import Image


def rgb_to_hex(rgb_vector):
    # Ensure values are within the valid range (0-255)
    hex_colors = []
    for color in rgb_vector:
        r, g, b = [max(0, min(255, int(x))) for x in color]
        hex_colors.append("#{:02x}{:02x}{:02x}".format(r, g, b))
    return hex_colors


def test_color_difference(normal_colors, new_color, normal_distance):
    result = True
    for color in normal_colors:
        result = result and (abs(np.linalg.norm(new_color) - color) > normal_distance)

    return result



def get_color_palette(image_path):
    image = Image.open(image_path)

    image_np = np.array(image)

    # Reshape the image array to a 2D array of RGB values
    h, w, _ = image_np.shape
    reshaped_array = image_np.reshape(h * w, 3)

    # Calculate the histogram for RGB values
    hist, edges = np.histogramdd(reshaped_array, bins=(256, 256, 256), range=((0, 256), (0, 256), (0, 256)))

    # Find the index of the most frequent color
    most_frequent_rgb = []
    norm_rgb_value = []

    most_frequent_index = np.unravel_index(hist.argmax(), hist.shape)
    #print(f'Most frequent index: {most_frequent_index}')
    #print(f'Histogram type: {type(hist)}, shape: {hist.shape}')
    #print(hist)

    # Get the RGB values of the most frequent color
    color = [edges[i][most_frequent_index[i]] for i in range(3)]
    most_frequent_rgb.append(color)
    norm_rgb_value.append(np.linalg.norm(color))
    hist[most_frequent_index] = 0

    for i_ in range(1, len(hist)):
        most_frequent_index = np.unravel_index(hist.argmax(), hist.shape)
        next_color = [edges[i][most_frequent_index[i]] for i in range(3)]
        hist[most_frequent_index] = 0
        #print(next_color)

        if test_color_difference(normal_colors=norm_rgb_value, new_color=next_color, normal_distance=58.334):
            most_frequent_rgb.append(next_color)
            norm_rgb_value.append(np.linalg.norm(next_color))
            if len(most_frequent_rgb) == 5:
                break

    return rgb_to_hex(most_frequent_rgb)

# # Plotting the histogram (optional)
# plt.figure(figsize=(10, 5))
# plt.hist(hist.flatten(), bins=256)
# plt.title('Histogram of RGB Values')
# plt.xlabel('Frequency')
# plt.ylabel('Number of Colors')
# plt.show()

# Plot histograms for each color channel
# plt.figure(figsize=(10, 5))
#
# # Red channel histogram
#
# # red_histogram = np.histogram(red_channel, bins=256)
# # print(red_histogram)
# plt.subplot(1, 3, 1)
# plt.hist(red_channel)
# plt.title('Red Channel')
# plt.xlabel('Pixel Intensity')
# plt.ylabel('Frequency')
#
#
# # Green channel histogram
# plt.subplot(1, 3, 2)
# plt.hist(green_channel)
# plt.title('Green Channel')
# plt.xlabel('Pixel Intensity')
# plt.ylabel('Frequency')
#
# # Blue channel histogram
# plt.subplot(1, 3, 3)
# plt.hist(blue_channel)
# plt.title('Blue Channel')
# plt.xlabel('Pixel Intensity')
# plt.ylabel('Frequency')
#
# plt.tight_layout()
# plt.show()


#width, height, channels = image_np.shape
# print(image_np.shape)
#
# rgb_vector = []
#
# for x in range(width):
#     for y in range(height):
#         rgb_vector.append((image_np[x][y][0], image_np[x][y][1], image_np[x][y][2]))
#
# plt.hist()

# hex_vector = [rgb_to_hex(rgb_color) for rgb_color in rgb_vector]
#
# no_colors = 5
# color_tolerance = 100



#print(f"Pixel: {rgb_vector[0]}")
#print(f"Pixel Hex: {hex(hex_vector[0])}, type: {type(hex_vector[0])}")
