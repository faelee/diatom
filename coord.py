from PIL import Image

file = open(input("text name"))
im = Image.open(input("image name"))
width, height = im.size
name = input("new name")

def draw(word):
    nums = [0.0] * 5
    line = word.split()
    for i in range(0, len(nums)):
        nums[i] = float(line[i])
    xmax = (2 * nums[1] + nums[3]) / 2 * width
    xmin = (2 * nums[1] - nums[3]) / 2 * width
    ymax = (2 * nums[2] + nums[4]) / 2 * height
    ymin = (2 * nums[2] - nums[4]) / 2 * height
    end = [round(xmin), round(ymin), round(xmax), round(ymax)]
    return str(end)

f = open(name + ".txt", "x")

while True:

    # Get next line from file 
    line = file.readline()

    # if line is empty 
    # end of file is reached 
    if not line:
        break

    out = draw(line)
    f.write(out + "\n")

file.close()

