import argparse
import torch
from diffusers import StableDiffusionXLImg2ImgPipeline
from PIL import Image
from image.prompts import generator_positive_prompt, generator_negative_prompt

parser = argparse.ArgumentParser()
parser.add_argument("init_image", type=str, help="기존 사진 파일 경로")
parser.add_argument("prompt", type=str, help="프롬프트")
parser.add_argument("--strength", type=float, default=0.3, help="입력 이미지의 영향력. 0일 경우 입력 이미지가 그대로 출력되며, 1일 경우 입력 이미지가 아예 고려되지 않음")
parser.add_argument("--seed", type=int, default=-1, help="seed 값. 주어지지 않으면 랜덤")
parser.add_argument("--num-imgs", type=int, default=4, help="이미지 개수")
args = parser.parse_args()

if __name__ == "__main__":
  # Stable Diffusion XL Image to Image model
  pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", 
    torch_dtype=torch.float16
  ).to("cuda")

  # load init image
  init_image = Image.open(args.init_image).convert("RGB")

  # regenerate and save images
  for i in range(args.num_imgs):
    img = pipe(
      prompt=", ".join(generator_positive_prompt + [args.prompt]),
      negative_prompt=", ".join(generator_negative_prompt),
      generator=torch.Generator("cuda").manual_seed(args.seed) if args.seed > -1 else None,
      image=init_image,
      strength=0.8,
      num_images_per_prompt=args.num_imgs
    ).images[0]
    img.save(f"img2img-{i}.png")
