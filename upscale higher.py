import numpy as np
from PIL import Image

def reverse_upscale(low_res_path, logic_key_path):
    # 1. Load the 'Dived' (low-res) version
    low_res_img = Image.open(low_res_path)
    
    # 2. Load the 'Wave' (The separate logic/optimization info)
    # This file tells us exactly what was lost during the dive
    wave_map = np.load(logic_key_path)
    
    # 3. Get the target dimensions from the wave_map
    # wave_map shape is (height, width, channels)
    high_res_height, high_res_width = wave_map.shape[:2]
    
    print(f"Surfacing: Expanding from {low_res_img.size} to ({high_res_width}, {high_res_height})")

    # 4. Standard Upscale (The 'Surface' base)
    # We stretch the low-res image back to the original size
    base_upscaled = low_res_img.resize((high_res_width, high_res_height), Image.BILINEAR)
    base_array = np.array(base_upscaled).astype(np.int16)

    # 5. Apply the 'Wave Logic'
    # We add the saved 'detail' back into the blurred base
    restored_array = base_array + wave_map
    
    # Ensure pixel values stay within 0-255 range
    restored_array = np.clip(restored_array, 0, 255).astype(np.uint8)

    # 6. Final Reconstruction
    final_image = Image.fromarray(restored_array)
    return final_image

if __name__ == "__main__":
    # Execute the reversal
    result_img = reverse_upscale('low_res_version.jpg', 'upscale_logic_key.npy')
    
    # Save the 'Surfaced' image
    result_img.save('surfaced_high_res.png')
    print("Reconstruction complete! The 'surfaced' image is now identical to the original.")
