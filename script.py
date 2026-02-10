from PIL import Image

# ANSI helper
def rgb(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def image_to_ascii_with_outline(path, width=100, outline_char="#"):
    img = Image.open(path).convert("RGBA")

    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width * 0.5)
    img = img.resize((width, height))

    pixels = img.load()

    chars = "@MWN$B%Qmg&D8GwROH96Kdqbp0USEhP5A4CX3keVZun#2aFoyYsT[]xcJL|z7fv{}1t?jl()I+r*!=i<>^\"/\\~_';-:,.`"
    ascii_art = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]

            if a < 128:
                outline = False
                for ny in range(max(0, y - 1), min(img.height, y + 2)):
                    for nx in range(max(0, x - 1), min(img.width, x + 2)):
                        if nx == x and ny == y:
                            continue
                        _, _, _, na = pixels[nx, ny]
                        if na >= 128:
                            outline = True
                            break
                    if outline:
                        break

                ascii_art += outline_char if outline else " "
            else:
                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                ascii_index = brightness * (len(chars) - 1) // 255
                ch = chars[ascii_index]

                ascii_art += rgb(r, g, b, ch)

        ascii_art += "\n"

    return ascii_art

if __name__ == "__main__":
    path = input("Enter the image file path: ")
    width_input = input("Enter ASCII width (default 100): ")
    width = int(width_input) if width_input.isdigit() else 100

    ascii_result = image_to_ascii_with_outline(path, width=width, outline_char="#")
    print("\nASCII Art:\n")
    print(ascii_result)

    save_file = input("Save ASCII to file? (y/n): ")
    if save_file.lower() == "y":
        with open("ascii_output.txt", "w") as f:
            f.write(ascii_result)
        print("Saved as ascii_output.txt")
