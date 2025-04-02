from PIL import Image, ImageDraw, ImageFont
import os

# Create the splash_assets directory if it doesn't exist
os.makedirs("gui/splash_assets", exist_ok=True)

# Create a new image with a white background
img = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Function to create a rounded rectangle
def rounded_rectangle(draw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    
    # Draw rectangle
    draw.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=outline
    )
    
    # Draw rectangle
    draw.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=outline
    )
    
    # Draw four corners
    draw.pieslice(
        [
            upper_left_point,
            (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)
        ],
        180,
        270,
        fill=fill,
        outline=outline
    )
    draw.pieslice(
        [
            (bottom_right_point[0] - corner_radius * 2, upper_left_point[1]),
            (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)
        ],
        270,
        0,
        fill=fill,
        outline=outline
    )
    draw.pieslice(
        [
            (upper_left_point[0], bottom_right_point[1] - corner_radius * 2),
            (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])
        ],
        90,
        180,
        fill=fill,
        outline=outline
    )
    draw.pieslice(
        [
            (bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2),
            bottom_right_point
        ],
        0,
        90,
        fill=fill,
        outline=outline
    )

# Draw a rounded rectangle for the hospital cross
rounded_rectangle(draw, [(40, 20), (160, 180)], corner_radius=20, fill=(248, 223, 205))

# Draw a red cross
cross_color = (220, 100, 100)
# Horizontal line of the cross
rounded_rectangle(draw, [(60, 80), (140, 120)], corner_radius=10, fill=cross_color)
# Vertical line of the cross
rounded_rectangle(draw, [(90, 50), (110, 150)], corner_radius=10, fill=cross_color)

try:
    # Try to load a font
    font = ImageFont.truetype("arial.ttf", 50)
    draw.text((100, 130), "H", fill=(80, 80, 80), font=font, anchor="mm")
except:
    # If font not available
    draw.text((90, 130), "H", fill=(80, 80, 80))

# Save the image
img.save("gui/splash_assets/logo.png")

print("Logo created successfully in gui/splash_assets/logo.png") 