import torch
import numpy as np
from PIL import Image
from diffusers import DiffusionPipeline
import torch.backends.cuda as cuda

class Model:
    def __init__(self):
        self.pipeline = DiffusionPipeline.from_pretrained(
            "dylanebert/LGM-full",
            custom_pipeline="dylanebert/LGM-full",
            torch_dtype=torch.float16,
            trust_remote_code=True,
            local_files_only=False  # 允许从Hugging Face下载模型
        )
        
        if cuda.is_available():
            self.pipeline = self.pipeline.to("cuda")
        else:
            print("CUDA not available, using CPU. This will be very slow!")
            self.pipeline = self.pipeline.to("cpu")

    async def process_image(self, input_path: str, output_path: str):
        # 加载和处理图片
        input_image = Image.open(input_path)
        input_array = np.array(input_image, dtype=np.float32) / 255.0
        
        # 生成3D模型
        with torch.cuda.amp.autocast():
            result = self.pipeline("", input_array)
        self.pipeline.save_ply(result, output_path)

model = Model()
process_image = model.process_image