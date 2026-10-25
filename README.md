# Projeto 2 — Sistema Solar 3D

Cena 3D em OpenGL 4.1 com Sol, Vênus, Terra e Lua. Usa esferas, iluminação por fragmento, texturas, normal mapping, plano de corte e troca de câmeras.

## Requisitos

- Python 3.10+
- PyOpenGL, PyGLM, glfw, Pillow e numpy
- opencv-python (opcional, apenas para gravar vídeo)

## Execução

```bash
cd projetos/python
python3 main_solar_proj2.py
```

Em WSLg, exporte as variáveis do Mesa/EGL antes de executar.

## Controles

- `C`: alterna entre a câmera orbital e a câmera na superfície da Terra olhando para a Lua
- `X`: liga/desliga o plano de corte no Sol
- `Q` ou `Esc`: sai

## Funcionalidades

- Sol, Vênus, Terra e Lua com translação e rotação
- Iluminação por fragmento com luz na posição do Sol
- Texturas nos astros e cubemap de fundo
- Bump mapping (normal map) na Terra e na Lua
- Plano de corte no Sol
- Câmera Terra → Lua atualizada por uma engine a cada quadro
- Gravação de vídeo com `record_solar.py`

## Estrutura

```text
projetos/
├── python/          # código da aplicação
├── shaders/solar/   # shaders GLSL
├── images/          # texturas
└── proj2.pdf        # enunciado
```

## Gravação

```bash
cd projetos/python
python3 record_solar.py --out solar_system.mp4 --duration 10
```
