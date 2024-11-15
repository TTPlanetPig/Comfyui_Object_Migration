# Clothing Migration Kit

This is an experimental project focused on **Stable Diffusion (SD) models**. In a single generated image, the same object or character consistently maintains a very high level of consistency. I had already attempted to address this issue in the **SDXL** model.

At that time, I used the **ControlNet** model with decaying weights to achieve good results. By using reference images, it was possible to generate multiple views of a single character at once while maintaining extremely high consistency. Due to a busy schedule, further exploration of this work was put on hold.

Recently, I came across discussions about **ic-lora** and noticed that it remains a standard **LoRA** but leverages the **DIT model** to achieve better consistency and excellent control over image formatting. Utilizing this format control effect, there is hope to achieve consistency in applications. Inspired by the concept of a latent-guided workflow introduced by the netizen "lrzjason aka xiaozhi," I simplified the entire preprocessing logic, thereby developing a highly effective migration method.

Through this process and methodology, you can achieve surprising migration and generalization effects by guiding the model to focus on the content you need, providing astonishing consistency. Currently, I have developed a matching migration model for clothing, which offers:

1. **Surprisingly Consistent Reference Image Clothing Migration**
   
   ![ComfyUI_temp_veptx_00011_](https://github.com/user-attachments/assets/9612cf8a-858d-4684-819e-7b97981d993c)
   
   ![ComfyUI_temp_bgltt_00001_](https://github.com/user-attachments/assets/0109061b-a8d4-4609-8b37-d14ec73049e2)

2. **Cartoon Clothing to Realism or Real Clothing to Cartoon**
   
   ![7e95939782f43a7272f2ff796f231871](https://github.com/user-attachments/assets/008c06c9-aa77-44aa-bee3-92b45141d54d)

3. **Control Over Clothing Similarity via Weights to Inspire Design Creativity**

## More To Do

1. **Transfer of Items with Distinct Features**
2. **Transfer of Intricate and Complex Patterns**
3. **Face Transfer**
4. **Additional Ideas from the Community**

## How to Use

You can download the model from my [Hugging Face project](https://huggingface.co/TTPlanet/Migration_Lora_flux/tree/main) in the **Migration LoRA** folder. Currently, only the **Cloth LoRA** is available, but I will add more once they are ready.

### Requirements

- **ComfyUI** to run the model with auto process.
- **Custom Nodes**:
  1. **TTP Toolset**: [ComfyUI_TTP_Toolset](https://github.com/TTPlanetPig/Comfyui_TTP_Toolset) *(Please update to the latest version)*
  2. **Tag Node**: I recommend using my version which provides a **custom_modification** for extra direction: [ComfyUI_JC2](https://github.com/TTPlanetPig/Comfyui_JC2)
  3. **I also used Alimama flux inpainting model, to get it from here: [Alimama_flux_inpainint](https://huggingface.co/black-forest-labs/FLUX.1-dev)

### Steps

1. **Install ComfyUI** and the required custom nodes listed above.
2. **Download** the **Cloth LoRA** from the Migration LoRA folder on Hugging Face.
3. **Load** the model into ComfyUI.
4. **Use** the provided workflow example to achieve the desired results.
5. **Notice** select the flux version wisely, as we need to load the Alimama inpainting model at same time, more VRAM needed, try nf8 if you feel slow. or use some momey optimization node like [FluxExt-MZ](https://github.com/MinusZoneAI/ComfyUI-FluxExt-MZ)

Feel free to experiment and modify the workflow according to your needs!

---

**Note:** Contributions and suggestions are welcome. Please open an issue or submit a pull request with your ideas.

