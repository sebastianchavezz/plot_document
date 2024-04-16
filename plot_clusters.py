import random
import numpy as np
import json
import cv2
import os

font = cv2.FONT_HERSHEY_COMPLEX
random.seed(3)
colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(40)]


def visualise_clusters(path, output_folder="output"):
    with open(path, 'r') as jf:
        data = json.load(jf)

    plot_json(data, os.path.join(output_folder, os.path.split(path)[1].replace(".json", ".png")))


def plot_json(data, output_path='output'):
    img = np.ones((1754, 1240, 3), np.uint8) * 255
    for word in data:
        img = plot_word(word, img)
    print('Saving,', output_path)
    cv2.imwrite(output_path, img)


def plot_word(word, img):
    bottom_left = int(word['position'][0] * 1240), int(word['position'][3] * 1754)
    sizes = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    w, h = int((word['position'][2] - word['position'][0]) * 1240), int(
        (word['position'][3] - word['position'][1]) * 1754)
    boxsizes = [cv2.getTextSize(word["word"], font, s, 1)[0] for s in sizes]
    img = cv2.putText(img, word["word"].replace('€', 'C'), bottom_left, font, sizes[np.argmin(boxsizes)],
                      colors[word.get("cluster", random.randint(0, 25))], 1)
    return img


if __name__ == '__main__':
    visualise_clusters("content.json")
