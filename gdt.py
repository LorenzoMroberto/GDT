import tkinter as tk
from tkinter import filedialog, messagebox
import threading, time, mss, cv2, os, shutil, ctypes, logging
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class ScreenRecorderApp:
    def __init__(self, root):
        self.root, self.esta_gravando, self.thread_gravacao, self.writer = root, False, None, None
        self.preview_ativo = True
        self.setup_interface()
        
    def setup_interface(self):
        self.frame_principal = tk.Frame(self.root, bg='black')
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.label_preview = tk.Label(self.frame_principal, bg='black')
        self.label_preview.pack(expand=True)
        
        frame_botao = tk.Frame(self.root, bg='#2d2d2d')
        frame_botao.pack(fill=tk.X, padx=10, pady=10)
        
        self.criar_icones()
        self.botao_gravar = tk.Button(frame_botao, image=self.icone_gravar, command=self.alternar_gravacao,
                                     bg='#e74c3c', bd=0, highlightthickness=0)
        self.botao_gravar.pack(pady=10)
        self.iniciar_preview()
        
    def criar_icones(self):
        r, s = Image.new('RGBA', (40, 40), (0, 0, 0, 0)), Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        ImageDraw.Draw(r).ellipse([5, 5, 35, 35], fill='white'); ImageDraw.Draw(s).rectangle([10, 10, 30, 30], fill='white')
        self.icone_gravar, self.icone_parar = ImageTk.PhotoImage(r), ImageTk.PhotoImage(s)
        
    def iniciar_preview(self): self.preview_ativo, self.atualizar_preview()
    def atualizar_preview(self):
        if not self.preview_ativo: return
        try:
            with mss.mss() as sct:
                tela = sct.grab(sct.monitors[1])
                largura_preview, altura_preview = min(640, tela.width // 2), min(360, tela.height // 2)
                img = Image.frombytes("RGB", tela.size, tela.bgra, "raw", "BGRX")
                img.thumbnail((largura_preview, altura_preview)); foto = ImageTk.PhotoImage(img)
                self.label_preview.configure(image=foto); self.label_preview.image = foto
        except Exception: pass
        if self.preview_ativo: self.root.after(200, self.atualizar_preview)
            
    def alternar_gravacao(self): self.iniciar_gravacao() if not self.esta_gravando else self.parar_gravacao()
    def iniciar_gravacao(self): 
        self.esta_gravando, self.preview_ativo = True, False
        self.botao_gravar.configure(image=self.icone_parar, bg='#f39c12')
        self.thread_gravacao = threading.Thread(target=self.gravar_tela); self.thread_gravacao.daemon = True
        self.thread_gravacao.start()
        
    def parar_gravacao(self):
        self.esta_gravando = False
        self.botao_gravar.configure(image=self.icone_gravar, bg='#e74c3c')
        if self.thread_gravacao: self.thread_gravacao.join(timeout=2.0)
        self.salvar_gravacao()
        self.iniciar_preview()
        
    def gravar_tela(self):
        try:
            with mss.mss() as sct:
                monitor, codec = sct.monitors[1], cv2.VideoWriter_fourcc(*'mp4v')
                sct.compression_level = 1
                filename = f"gravacao_{time.strftime('%Y%m%d-%H%M%S')}.mp4"
                self.writer = cv2.VideoWriter(filename, codec, 20.0, (monitor["width"], monitor["height"]))
                
                user32, POINT = ctypes.windll.user32, ctypes.wintypes.POINT()
                frame_time = 1.0 / 20.0
                
                while self.esta_gravando:
                    frame_start = time.time()
                    try:
                        tela = sct.grab(monitor)
                        frame = cv2.cvtColor(np.array(tela), cv2.COLOR_BGRA2BGR)
                        
                        user32.GetCursorPos(ctypes.byref(POINT))
                        x, y = POINT.x - monitor["left"], POINT.y - monitor["top"]
                        if 0 <= x < monitor["width"] and 0 <= y < monitor["height"]:
                            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
                        
                        self.writer.write(frame)
                        elapsed = time.time() - frame_start
                        sleep_time = max(frame_time - elapsed, 0)
                        if sleep_time > 0: time.sleep(sleep_time)
                            
                    except Exception as frame_error:
                        logging.debug(f"Erro no frame: {frame_error}")
                        time.sleep(0.01)
                        
        except Exception as e: logging.error(f"Erro na gravação: {e}")
        finally: 
            if self.writer: 
                try: self.writer.release()
                except: pass
                self.writer = None
                
    def salvar_gravacao(self):
        try:
            nome_arquivo = filedialog.asksaveasfilename(defaultextension=".mp4",
                                                      filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
                                                      title="Salvar gravação")
            if nome_arquivo:
                arquivos_temp = [f for f in os.listdir('.') if f.startswith('gravacao_') and f.endswith('.mp4')]
                if arquivos_temp: shutil.move(arquivos_temp[0], nome_arquivo); messagebox.showinfo("Sucesso", f"Gravação salva em:\n{nome_arquivo}")
        except Exception as e: logging.error(f"Erro ao salvar: {e}")

def main():
    root = tk.Tk(); root.title('Gravador de tela')
    app = ScreenRecorderApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [setattr(app, 'preview_ativo', False), setattr(app, 'esta_gravando', False), root.destroy()])
    root.mainloop()

if __name__ == "__main__": 
    logging.basicConfig(level=logging.ERROR)
    main()