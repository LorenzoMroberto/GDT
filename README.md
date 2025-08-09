# GDT
Gravador de tela simples

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen)
![Versão](https://img.shields.io/badge/Versão-1.0-blue)
![Dependencies](https://img.shields.io/badge/dependencies-4-brightgreen)
![Py+Win](https://img.shields.io/badge/Python%203.11.7%20%7C%20Windows%2011-✔-brightgreen?logo=python&logoColor=white)

<img width="1537" height="701" alt="2Captura de tela 2025-07-25 120001" src="https://github.com/user-attachments/assets/796be81a-7cc3-4707-9cda-235b8bcc2df4" />

O script tem como intuito ser um gravador de tela, ele grava toda a tela incluindo barra de tarefas.

🛠️ Funcionalidades
- ✅ Pré-visualização da tela
- ✅ Gravação em MP4 com 20 FPS
- ✅ Cursor do mouse destacado em vermelho
- ✅ Interface simples com botões gráficos (ícones gerados dinamicamente)
- ✅ Salva o arquivo com nome especificado pelo usuário

| Módulo / Pacote       | Tipo                     | Observação |
|-----------------------|--------------------------|-----------|
| `tkinter`             | Incluso no Python        | Interface gráfica (GUI) |
| `threading`           | Incluso no Python        | Execução paralela da gravação |
| `time`                | Incluso no Python        | Controle de tempo e timestamps |
| `os`                  | Incluso no Python        | Operações com arquivos e diretórios |
| `shutil`              | Incluso no Python        | Movimentação de arquivos |
| `ctypes`              | Incluso no Python        | Acesso ao cursor do mouse (via `user32`) |
| `logging`             | Incluso no Python        | Registro de erros |
| `tkinter` | Incluso no Python | Diálogos para abrir/salvar arquivos |
| `mss`                 | ⚠️ Requer instalação     | Captura rápida de tela |
| `cv2`       | ⚠️ Requer instalação     | Gravação e codificação de vídeo |
| `PIL`        | ⚠️ Requer instalação     | Manipulação de imagens e ícones |
| `numpy`               | ⚠️ Requer instalação     | Tratamento de arrays de imagem |
