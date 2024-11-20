import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageEnhance
import node_helpers
import torch

def pil2tensor(image: Image) -> torch.Tensor:
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def tensor2pil(t_image: torch.Tensor) -> Image:
    return Image.fromarray(np.clip(255.0 * t_image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

class TTP_Expand_And_Mask:
    """
    这是一个节点类，用于将输入图片在指定方向扩展一定数量的块并创建相应蒙版。

    功能：
    1. 支持同时在多个方向上扩展图像。
    2. 分别控制每个方向的扩展块数量。
    3. 将输入图像的透明通道（Alpha 通道）信息转换为蒙版，并与新创建的蒙版合并。
    4. 添加一个布尔参数 fill_alpha_decision 来决定是否将输出图片中的透明区域填充为白色，并输出 RGB 图像。
    """
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        directions = ["left", "right", "top", "bottom"]
        return {
            "required": {
                "image": ("IMAGE",),  # 输入一张图片
                "fill_mode": (["duplicate", "white"], {"default": "duplicate", "label": "Fill Mode"}),
                # fill_mode是一个字符串列表参数，可以选择"duplicate"或"white"
                "fill_alpha_decision": ("BOOLEAN", {"default": False, "label": "Fill Alpha with White"}),
                # fill_alpha_decision为一个布尔值参数，用来决定是否将输出图像透明区域填充为白色
            },
            "optional": {
                **{f"expand_{dir}": ("BOOLEAN", {"default": False, "label": f"Expand {dir.capitalize()}"}) for dir in directions},
                **{f"num_blocks_{dir}": ("INT", {"default": 1, "min": 0, "max": 3, "step": 1, "label": f"Blocks {dir.capitalize()}"}) for dir in directions},
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("EXPANDED_IMAGE", "MASK")
    FUNCTION = "expand_and_mask"
    CATEGORY = "TTP/Image"

    def expand_and_mask(self, image, fill_mode="duplicate", fill_alpha_decision=False, **kwargs):
        pil_image = tensor2pil(image)
        orig_width, orig_height = pil_image.size
        has_alpha = (pil_image.mode == 'RGBA')

        # 解析方向和块数
        directions = ["left", "right", "top", "bottom"]
        expand_directions = {dir: kwargs.get(f"expand_{dir}", False) for dir in directions}
        num_blocks = {dir: kwargs.get(f"num_blocks_{dir}", 0) if expand_directions[dir] else 0 for dir in directions}

        # 计算扩展后的尺寸
        total_width = orig_width + orig_width * (num_blocks["left"] + num_blocks["right"])
        total_height = orig_height + orig_height * (num_blocks["top"] + num_blocks["bottom"])

        # 创建扩展后的图像
        expanded_image_mode = pil_image.mode
        expanded_image = Image.new(expanded_image_mode, (total_width, total_height))

        # 根据 fill_mode 创建填充图像
        def create_fill_image():
            if pil_image.mode == 'RGBA':
                return Image.new("RGBA", (orig_width, orig_height), color=(255, 255, 255, 255))
            elif pil_image.mode == 'RGB':
                return Image.new("RGB", (orig_width, orig_height), color=(255, 255, 255))
            elif pil_image.mode == 'L':
                return Image.new("L", (orig_width, orig_height), color=255)
            else:
                raise ValueError(f"Unsupported image mode for fill: {pil_image.mode}")

        if fill_mode == "duplicate":
            fill_image = pil_image.copy()
        elif fill_mode == "white":
            fill_image = create_fill_image()
        else:
            fill_image = pil_image.copy()

        # 计算原图在扩展图像中的位置
        left_offset = orig_width * num_blocks["left"]
        top_offset = orig_height * num_blocks["top"]

        # 粘贴原始图像
        expanded_image.paste(pil_image, (left_offset, top_offset))

        # 粘贴填充区域
        for dir in directions:
            blocks = num_blocks[dir]
            for i in range(blocks):
                if dir == "left":
                    x = left_offset - orig_width * (i + 1)
                    y = top_offset
                elif dir == "right":
                    x = left_offset + orig_width * (i + 1)
                    y = top_offset
                elif dir == "top":
                    x = left_offset
                    y = top_offset - orig_height * (i + 1)
                elif dir == "bottom":
                    x = left_offset
                    y = top_offset + orig_height * (i + 1)
                else:
                    continue
                expanded_image.paste(fill_image, (x, y))

        # 粘贴角落填充区域（处理同时选择多个方向的情况）
        corner_positions = []
        if expand_directions["left"] and expand_directions["top"]:
            for i in range(num_blocks["left"]):
                for j in range(num_blocks["top"]):
                    x = left_offset - orig_width * (i + 1)
                    y = top_offset - orig_height * (j + 1)
                    corner_positions.append((x, y))
        if expand_directions["left"] and expand_directions["bottom"]:
            for i in range(num_blocks["left"]):
                for j in range(num_blocks["bottom"]):
                    x = left_offset - orig_width * (i + 1)
                    y = top_offset + orig_height * (j + 1)
                    corner_positions.append((x, y))
        if expand_directions["right"] and expand_directions["top"]:
            for i in range(num_blocks["right"]):
                for j in range(num_blocks["top"]):
                    x = left_offset + orig_width * (i + 1)
                    y = top_offset - orig_height * (j + 1)
                    corner_positions.append((x, y))
        if expand_directions["right"] and expand_directions["bottom"]:
            for i in range(num_blocks["right"]):
                for j in range(num_blocks["bottom"]):
                    x = left_offset + orig_width * (i + 1)
                    y = top_offset + orig_height * (j + 1)
                    corner_positions.append((x, y))

        for pos in corner_positions:
            expanded_image.paste(fill_image, pos)

        # 创建蒙版
        mask_array = np.zeros((total_height, total_width), dtype=np.float32)

        # 原始图像区域蒙版处理
        if has_alpha:
            alpha_array = np.array(pil_image.getchannel("A"), dtype=np.float32) / 255.0
            alpha_mask_array = 1.0 - alpha_array
            mask_array[top_offset:top_offset + orig_height, left_offset:left_offset + orig_width] = alpha_mask_array

        # 填充区域蒙版设置为1.0
        # 左右扩展区域
        for dir in ["left", "right"]:
            blocks = num_blocks[dir]
            for i in range(blocks):
                if dir == "left":
                    x_start = left_offset - orig_width * (i + 1)
                    x_end = left_offset - orig_width * i
                elif dir == "right":
                    x_start = left_offset + orig_width * (i + 1)
                    x_end = left_offset + orig_width * (i + 2)
                else:
                    continue
                mask_array[top_offset:top_offset + orig_height, x_start:x_end] = 1.0

        # 上下扩展区域
        for dir in ["top", "bottom"]:
            blocks = num_blocks[dir]
            for i in range(blocks):
                if dir == "top":
                    y_start = top_offset - orig_height * (i + 1)
                    y_end = top_offset - orig_height * i
                elif dir == "bottom":
                    y_start = top_offset + orig_height * (i + 1)
                    y_end = top_offset + orig_height * (i + 2)
                else:
                    continue
                mask_array[y_start:y_end, left_offset:left_offset + orig_width] = 1.0

        # 角落区域蒙版设置为1.0
        for pos in corner_positions:
            x, y = pos
            mask_array[y:y + orig_height, x:x + orig_width] = 1.0

        # 创建蒙版张量 (1, 1, height, width)
        mask_tensor = torch.from_numpy(mask_array).unsqueeze(0).unsqueeze(0)

        # 根据 fill_alpha_decision 参数决定是否将输出图像中的透明区域填充为白色
        if fill_alpha_decision and has_alpha:
            expanded_image = expanded_image.convert('RGBA')  # 确保图像是RGBA模式
            background = Image.new('RGBA', expanded_image.size, (255, 255, 255, 255)) 
            expanded_image = Image.alpha_composite(background, expanded_image)
            expanded_image = expanded_image.convert('RGB')  # 转换为RGB模式
            expanded_image_mode = 'RGB'

        expanded_image_tensor = pil2tensor(expanded_image)

        return (expanded_image_tensor, mask_tensor)
        
class TTP_text_mix:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text1": ("STRING", {"default": "", "multiline": True, "label": "Text Box 1"}),
                "text2": ("STRING", {"default": "", "multiline": True, "label": "Text Box 2"}),
                "text3": ("STRING", {"default": "", "multiline": True, "label": "Text Box 3"}),
                "template": ("STRING", {"default": "", "multiline": True, "label": "Template Text Box"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("text1", "text2", "text3", "final_text")
    FUNCTION = "mix_texts"
    CATEGORY = "TTP/text"

    def mix_texts(self, text1, text2, text3, template):
        # 使用replace方法替换模板中的占位符{text1}和{text2}
        final_text = template.replace("{text1}", text1).replace("{text2}", text2).replace("{text3}", text3)

        return (text1, text2, text3, final_text)
        
NODE_CLASS_MAPPINGS = {
    "TTP_Expand_And_Mask": TTP_Expand_And_Mask,
    "TTP_text_mix": TTP_text_mix
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TTP_Expand_And_Mask": "TTP_Expand_And_Mask",
    "TTP_text_mix": "TTP_text_mix"
}
