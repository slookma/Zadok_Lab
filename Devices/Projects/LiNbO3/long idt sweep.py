import gdspy
import numpy as np

# IDT parameters
num_fingers = 30
finger_length = 100
idt_size_dx = finger_length + 4 + 2 * 3  # finger_length + gap_metal + 2*finger_width
idt_size_dy = num_fingers * (3 + 4) + 4  # Default values used for calculation
dx = 1000  # X spacing between different IDT sets
dy = 1500  # Y spacing between different IDT sets
gap_strip_finger = 10

# IDT parameters -long fingers
finger_length_long = 1000
spacing_long=200
dx_long=2000

# Define rectangle size and spacing for voltage array
rect_width = 100
rect_height = 100
rect_spacing = 150
num_rectangles = 3
x_start = dx / 2 - 47
y_start = 2500

# GDSII setup
lib = gdspy.GdsLibrary()
cell = lib.new_cell('IDT_sweep')

# Layers definition
LAYER_WG = {"layer": 101, "datatype": 0}
LAYER_NEG = {"layer": 301, "datatype": 0}
TEXT_LAYER = {"layer": 99, "datatype": 0}  # Layer for labels

# Custom sweep list (12 total)
custom_sweep = [
    (2, 8), (2, 9), (2, 10), (2, 11), (2, 12),
    (3, 8), (3, 9), (3, 10), (3, 11), (3, 12),
    (4, 12), (4, 11)
]

# Original 3x4 sweep grid (horizontal IDTs)
num_rows, num_cols = 3, 4
sweep_grid = np.array(custom_sweep).reshape((num_rows, num_cols, 2))

# Rotated 4x3 sweep grid (vertical IDTs)
num_rows_rot, num_cols_rot = 3, 4
sweep_grid_rotated = np.array(custom_sweep).reshape((num_rows_rot, num_cols_rot, 2))

# IDT generation functions
def create_idt(cell, center, num_fingers, finger_width, finger_length, gap_metal, layer):
    x_center, y_center = center
    y_start = y_center - (num_fingers // 2) * (finger_width + gap_metal)
    even_x = x_center - finger_length / 2
    odd_x = even_x + gap_strip_finger
    for i in range(num_fingers):
        y = y_start + i * (finger_width + gap_metal)
        x = even_x if i % 2 == 0 else odd_x
        cell.add(gdspy.Rectangle((x, y), (x + finger_length, y + finger_width), **layer))
    strip_width = finger_width * 2
    strip_length = num_fingers * (finger_width + gap_metal) + (gap_metal - finger_width)
    cell.add(gdspy.Rectangle((even_x - strip_width, y_start - gap_metal),
                              (even_x, y_start + strip_length - gap_metal), **layer))
    cell.add(gdspy.Rectangle((odd_x + finger_length, y_start - gap_metal),
                              (odd_x + finger_length + strip_width, y_start + strip_length - gap_metal / 2), **layer))

def create_idt_90(cell, center, num_fingers, finger_width, finger_length, gap_metal, layer):
    x_center, y_center = center
    x_start = x_center - (num_fingers // 2) * (finger_width + gap_metal)
    even_finger_start_y = y_center - finger_length / 2
    odd_finger_start_y = y_center - finger_length / 2 + gap_strip_finger

    for i in range(num_fingers):
        x = x_start + i * (finger_width + gap_metal)
        if i % 2 == 0:
            y_start = even_finger_start_y
        else:
            y_start = odd_finger_start_y
        y_end = y_start + finger_length
        cell.add(gdspy.Rectangle((x, y_start), (x + finger_width, y_end), **layer))

    strip_width = finger_width * 2
    strip_length = num_fingers * (finger_width + gap_metal) + gap_metal

    # Bottom strip for even fingers
    bottom_strip_y_start = even_finger_start_y - strip_width
    bottom_strip_y_end = even_finger_start_y
    cell.add(gdspy.Rectangle((x_start - gap_metal, bottom_strip_y_start),
                              (x_start + strip_length, bottom_strip_y_end), **layer))

    # Top strip for odd fingers
    top_strip_y_start = odd_finger_start_y + finger_length
    top_strip_y_end = top_strip_y_start + strip_width
    cell.add(gdspy.Rectangle((x_start - gap_metal, top_strip_y_start),
                              (x_start + strip_length, top_strip_y_end), **layer))

# Create the 3x4 horizontal grid
for i in range(num_rows):
    row_index = num_rows - 1 - i
    for j in range(num_cols):
        finger_width, Lambda = sweep_grid[row_index, j]
        x_offset = j * dx
        x_offset_long = j * dx_long
        y_offset = i * dy + 200
        y_offset_long=i * dy -5000 
        gap_metal = Lambda / 2 - finger_width

        # Calculate spacing as nearest multiple of Lambda ~ 1000
        n = int(round(1000 / Lambda))
        spacing = n * Lambda

        center_horizontal_sender = (x_offset, y_offset)
        center_horizontal_receiver = (x_offset, y_offset + spacing)
        create_idt(cell, center_horizontal_sender, num_fingers, finger_width, finger_length, gap_metal, LAYER_WG)
        create_idt(cell, center_horizontal_receiver, num_fingers, finger_width, finger_length, gap_metal, LAYER_WG)
        
        #long_idt
        center_horizontal_sender = (x_offset_long, y_offset_long)
        center_horizontal_receiver = (x_offset_long, y_offset_long + spacing)
        create_idt(cell, center_horizontal_sender, num_fingers, finger_width, finger_length_long, gap_metal, LAYER_WG)
        create_idt(cell, center_horizontal_receiver, num_fingers, finger_width, finger_length_long, gap_metal, LAYER_WG)
        # Add labels for horizontal IDTs
        text_content = f"F={finger_width}, L={Lambda}"
        text_position = ( x_offset_long-8000,  y_offset_long)  # Adjust the position for text
        text = gdspy.Text(text_content, 70, text_position)  # Added layer to text
        cell.add(text)
     


        # Voltage rectangles (horizontal)
        for k in range(num_rectangles):
            x_array_offset = x_offset + rect_spacing / 2 + (k - num_rectangles // 2) * rect_spacing
            rect = gdspy.Rectangle(
                (x_array_offset, y_start-70),
                (x_array_offset + rect_width, y_start-70 + rect_height),
                **LAYER_WG
            )
            cell.add(rect)


       
        
# center_horizontal_sender = (x_offset+dx, y_offset)
# center_horizontal_receiver = (x_offset+dx, y_offset + spacing)
# create_idt(cell, center_horizontal_sender, num_fingers, finger_width, finger_length_long, gap_metal, LAYER_WG)
# create_idt(cell, center_horizontal_receiver, num_fingers, finger_width, finger_length_long, gap_metal, LAYER_WG)

# Offset below the original grid
flip_offset_y = num_rows * dy + 200
dx = 1500  # X spacing between different IDT sets
dy = 1000  # Y spacing between different IDT sets

# Create the 4x3 rotated vertical grid
for i in range(num_rows_rot):
    row_index = num_rows_rot - 1 - i
    for j in range(num_cols_rot):
        finger_width, Lambda = sweep_grid_rotated[row_index, j]
        x_offset = j * dx
        y_offset = i * dy + flip_offset_y
        gap_metal = Lambda / 2 - finger_width

        # Calculate spacing as nearest multiple of Lambda ~ 1000
        n = int(round(1000 / Lambda))
        spacing = n * Lambda

        center_vertical_sender = (x_offset, y_offset)
        center_vertical_receiver = (x_offset + spacing, y_offset)
        create_idt_90(cell, center_vertical_sender, num_fingers, finger_width, finger_length, gap_metal, LAYER_WG)
        create_idt_90(cell, center_vertical_receiver, num_fingers, finger_width, finger_length, gap_metal, LAYER_WG)

        # # Voltage rectangles (vertical)
        # if j == 0 or j == 2:
        #     y_start = y_offset - rect_height / 2 + 505  # Center around the vertical IDTs
        #     for k in range(num_rectangles):
        #         x_array_offset = x_offset + spacing / 2 + (k - num_rectangles // 2) * rect_spacing
        #         rect = gdspy.Rectangle((x_array_offset, y_start),
        #                                (x_array_offset + rect_width, y_start + rect_height),
        #                                **LAYER_WG)
        #         cell.add(rect)

        # Add labels for vertical IDTs
        text_content = f"F={finger_width}, L={Lambda}"
        text_position = ( x_offset-6000,  y_offset)  # Adjust the position for text
        text = gdspy.Text(text_content, 70, text_position)  # Added layer to text
        cell.add(text)
        # label_text = f'F={finger_width}, L={Lambda}'
        # cell.add(gdspy.Label(label_text, (x_offset + spacing + 100, y_offset + 50), layer=99))

# Write to the same GDS file
gdspy.write_gds('idt_sweep_long_length1.gds', [cell])
print("GDS file 'idt_sweep_sets_of_3.gds' has been created.")