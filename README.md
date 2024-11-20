# **Migration Kit Overview**

## **Contact Me**
| Platform      | Details                                                                 |
|---------------|-------------------------------------------------------------------------|
| **QQ Group**  | 571587838                                                              |
| **Bilibili**  | [Homepage](https://space.bilibili.com/23462279?spm_id_from=333.999.0.0) |
| **Civitai**   | [ttplanet](https://civitai.com/user/ttplanet)                          |
| **WeChat**    | tangtuanzhuzhu                                                        |

---

## **Project Introduction**
This experimental project focuses on leveraging **Stable Diffusion (SD) models** for high-consistency object and character rendering. The methodology integrates advanced workflows such as **ControlNet**, **DIT model**, and **latent-guided processes** for superior control and consistency.

---

## **Modules**

### **1. Clothing Migration Kit**
**Model Download**: [Clothing Migration LoRA](https://huggingface.co/TTPlanet/Migration_Lora_flux/resolve/main/Migration_Lora_cloth.safetensors?download=true)

**workflow Download**: [Cloth workflow](https://github.com/TTPlanetPig/Comfyui_Object_Migration/blob/main/workflow/cloth_style_Migration_v2.json)

| Feature                         | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| **Consistent Clothing Migration** | Transfer clothing styles across reference images with high accuracy.        |
| **Cartoon to Realism Conversion** | Seamlessly convert cartoon clothing to realistic styles and vice versa.     |
| **Creative Design Control**      | Adjust clothing similarity via weights to inspire creativity.               |

**Image Examples:**

| ![Example 1](https://github.com/user-attachments/assets/9612cf8a-858d-4684-819e-7b97981d993c) | ![Example 2](https://github.com/user-attachments/assets/0109061b-a8d4-4609-8b37-d14ec73049e2) |  
|------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|

### **2. 3D Figure Kit**
**Model Download**: [3D Figure LoRA](https://huggingface.co/TTPlanet/Migration_Lora_flux/tree/main)

**workflow Download**: [Figure workflow](https://github.com/TTPlanetPig/Comfyui_Object_Migration/blob/main/workflow/3D_Figures_transfer_workflow_v1.json)

| Feature                          | Description                                                                     |
|----------------------------------|---------------------------------------------------------------------------------|
| **3D Conversion**                | Transform 2D character designs into 3D printable figurines.                    |
| **Pose Customization**           | Adjust poses, expressions, and other dynamic features to suit your design needs.|
| **Material and Texture Enhancements** | Ensure high fidelity in textures and details for professional-grade outputs. |

**Image Examples:**

| ![Placeholder 1](https://github.com/user-attachments/assets/0f7b835d-a01b-4d60-9b69-f0dfa29aef01) | ![Placeholder 2](https://github.com/user-attachments/assets/7cd12fae-0e6d-4f62-93b6-bca931586bbd) |  
|------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
---

## **Future Plans**
| Task                           | Details                                                |
|--------------------------------|-------------------------------------------------------|
| **Transfer Distinct Features** | Improve the migration of objects with unique attributes.|
| **Complex Pattern Handling**   | Develop models to manage intricate designs.            |
| **Face Transfer**              | Implement face style migrations.                       |
| **3D Enhancements**            | Introduce automated rigging and advanced pose control for 3D figures. |
| **Community Ideas**            | Incorporate suggestions and use cases shared by users. |

---

## **How to Use**
| Step           | Details                                                                                      |
|----------------|----------------------------------------------------------------------------------------------|
| **1. Install** | Install **ComfyUI** and required custom nodes.                                              |
| **2. Download** | Obtain the models from the [Hugging Face Project](https://huggingface.co/TTPlanet/Migration_Lora_flux/tree/main). |
| **3. Load**    | Load the selected model into ComfyUI.                                                       |
| **4. Workflow** | Use the provided [workflow examples](https://github.com/TTPlanetPig/Comfyui_Object_Migration/blob/main/workflow/cloth_style_Migration_v2.json) for your application. |

---

## **Dependencies**
| Node            | Link                                                                                      |
|-----------------|------------------------------------------------------------------------------------------|
| **TTP Toolset** | [ComfyUI_TTP_Toolset](https://github.com/TTPlanetPig/Comfyui_TTP_Toolset)                |
| **Tag Node**    | [ComfyUI_JC2](https://github.com/TTPlanetPig/Comfyui_JC2)                               |
| **Alimama Flux**| [Alimama_flux_inpaint](https://huggingface.co/black-forest-labs/FLUX.1-dev)             |

**Note:** Ensure sufficient VRAM for high-complexity workflows. Use optimization tools like [FluxExt-MZ](https://github.com/MinusZoneAI/ComfyUI-FluxExt-MZ) if needed.

---

## **Contribute**
Contributions and suggestions are welcome! Open an issue or submit a pull request with your ideas.

---

