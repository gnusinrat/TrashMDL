import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import shutil
import struct

class GModCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("750x800")
        self.root.configure(padx=20, pady=20)

        self.current_lang = "ru"
        self.loc = {
            "ru": {
                "title": "TrashMDL - Инженерская Кузница v7.0",
                "mode": "Режим работы:",
                "m_stat": "1. Статика из OBJ (с авто-текстурами)",
                "m_rag": "2. Рэгдолл/Анимация (из готовых SMD)",
                "f_obj": "Файл 3D модели (.obj):",
                "f_smd": "Главный файл модели со скелетом (.smd):",
                "browse": "Обзор",
                "phys": "Файл физики/коллизии (.smd) (Опционально):",
                "anim": "Файл анимации (.smd) (Опционально):",
                "search": "Папка для авто-поиска потерянных текстур:",
                "vtf": "Папка с VTFCmd.exe:",
                "gmod": "Папка Garry's Mod (где hl2.exe):",
                "name": "Имя готовой модели в GMod (без .mdl):",
                "logs": "Логи работы:",
                "build": "ПОСТРОИТЬ И НАЙТИ ВСЁ!",
                "btn_lang": "🇬🇧 Switch to English",
                "err_mod": "Модель не найдена!",
                "err_std": "studiomdl.exe не найден.",
                "err_vtfcmd": "ОШИБКА: VTFCmd.exe не найден!",
                "err_mtl": "ОШИБКА: Файл .mtl не найден!",
                "log_read": "Читаем чертежи OBJ...",
                "log_qc": "Пишем QC скрипт...",
                "log_build": "Вызываем studiomdl.exe (Постройка началась)...",
                "log_done": "ГОТОВО! Модель скомпилирована!",
                "log_err": "Шпион сломал турель (ошибка):",
                "l_search": "ИЩЕЙКА: Ищу файл",
                "l_found": "ИЩЕЙКА НАШЛА:",
                "l_notfound": "ИЩЕЙКА НЕ НАШЛА:",
                "l_col": "КИСТЬ АВТОМАТА: Рисуем цвет",
                "l_mov": "Переносим всё в GMod...",
                "l_ok": "Успешно закинуто файлов в GMod:",
                "l_fail": "ОШИБКА ДОСТУПА В GMOD:",
                "msg_title": "Ошибка Инженера"
            },
            "en": {
                "title": "TrashMDL - Engineer's Forge v7.0",
                "mode": "Operation Mode:",
                "m_stat": "1. Static from OBJ (auto-textures)",
                "m_rag": "2. Ragdoll/Animation (from ready SMD)",
                "f_obj": "3D Model File (.obj):",
                "f_smd": "Main Skeleton Model File (.smd):",
                "browse": "Browse",
                "phys": "Physics/Collision File (.smd) (Optional):",
                "anim": "Animation File (.smd) (Optional):",
                "search": "Folder for auto-searching lost textures:",
                "vtf": "Folder with VTFCmd.exe:",
                "gmod": "Garry's Mod Folder (where hl2.exe is):",
                "name": "Output GMod Model Name (without .mdl):",
                "logs": "Operation Logs:",
                "build": "BUILD AND FIND EVERYTHING!",
                "btn_lang": "🇷🇺 Переключить на Русский",
                "err_mod": "Model not found!",
                "err_std": "studiomdl.exe not found.",
                "err_vtfcmd": "ERROR: VTFCmd.exe not found!",
                "err_mtl": "ERROR: .mtl file not found!",
                "log_read": "Reading OBJ blueprints...",
                "log_qc": "Writing QC script...",
                "log_build": "Calling studiomdl.exe (Building started)...",
                "log_done": "DONE! Model compiled!",
                "log_err": "Spy sapped the sentry (error):",
                "l_search": "HOUND: Searching for file",
                "l_found": "HOUND FOUND:",
                "l_notfound": "HOUND NOT FOUND:",
                "l_col": "AUTO-BRUSH: Drawing color",
                "l_mov": "Moving everything to GMod...",
                "l_ok": "Successfully moved files to GMod:",
                "l_fail": "GMOD ACCESS ERROR:",
                "msg_title": "Engineer Error"
            }
        }

        self.model_path = tk.StringVar()
        self.gmod_path = tk.StringVar()
        self.vtfcmd_path = tk.StringVar()
        self.model_name = tk.StringVar(value="trashmdl/my_model")
        self.search_path = tk.StringVar(value=os.path.expanduser("~"))
        self.compile_mode = tk.StringVar(value="static_obj")
        self.phys_model_path = tk.StringVar()
        self.anim_path = tk.StringVar()

        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", pady=(0, 10))
        self.btn_lang = tk.Button(top_frame, text="", command=self.toggle_lang, font=("Arial", 10, "bold"))
        self.btn_lang.pack(side="right")

        self.lbl_mode = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_mode.pack(anchor="w")
        mode_frame = tk.Frame(root)
        mode_frame.pack(fill="x", pady=(0, 5))
        self.rb_stat = tk.Radiobutton(mode_frame, text="", variable=self.compile_mode, value="static_obj", command=self.update_ui)
        self.rb_stat.pack(side="left")
        self.rb_rag = tk.Radiobutton(mode_frame, text="", variable=self.compile_mode, value="ragdoll_smd", command=self.update_ui)
        self.rb_rag.pack(side="left")

        self.lbl_model = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_model.pack(anchor="w")
        frame1 = tk.Frame(root)
        frame1.pack(fill="x", pady=(0, 5))
        tk.Entry(frame1, textvariable=self.model_path).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_browse_model = tk.Button(frame1, text="", command=self.browse_model)
        self.btn_browse_model.pack(side="right")

        self.frame_ragdoll = tk.Frame(root)
        self.lbl_phys = tk.Label(self.frame_ragdoll, text="", font=("Arial", 9))
        self.lbl_phys.pack(anchor="w")
        fr_phys = tk.Frame(self.frame_ragdoll)
        fr_phys.pack(fill="x", pady=(0, 5))
        tk.Entry(fr_phys, textvariable=self.phys_model_path).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_browse_phys = tk.Button(fr_phys, text="", command=lambda: self.browse_smd(self.phys_model_path))
        self.btn_browse_phys.pack(side="right")
        
        self.lbl_anim = tk.Label(self.frame_ragdoll, text="", font=("Arial", 9))
        self.lbl_anim.pack(anchor="w")
        fr_anim = tk.Frame(self.frame_ragdoll)
        fr_anim.pack(fill="x", pady=(0, 5))
        tk.Entry(fr_anim, textvariable=self.anim_path).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_browse_anim = tk.Button(fr_anim, text="", command=lambda: self.browse_smd(self.anim_path))
        self.btn_browse_anim.pack(side="right")

        self.lbl_search = tk.Label(root, text="", font=("Arial", 10, "bold"), fg="#e67e22")
        self.lbl_search.pack(anchor="w")
        frame_search = tk.Frame(root)
        frame_search.pack(fill="x", pady=(0, 5))
        tk.Entry(frame_search, textvariable=self.search_path).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_browse_search = tk.Button(frame_search, text="", command=self.browse_search)
        self.btn_browse_search.pack(side="right")

        self.lbl_vtf = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_vtf.pack(anchor="w")
        frame_vtf = tk.Frame(root)
        frame_vtf.pack(fill="x", pady=(0, 5))
        tk.Entry(frame_vtf, textvariable=self.vtfcmd_path).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_browse_vtf = tk.Button(frame_vtf, text="", command=self.browse_vtfcmd)
        self.btn_browse_vtf.pack(side="right")

        self.lbl_gmod = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_gmod.pack(anchor="w")
        frame2 = tk.Frame(root)
        frame2.pack(fill="x", pady=(0, 5))
        tk.Entry(frame2, textvariable=self.gmod_path).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_browse_gmod = tk.Button(frame2, text="", command=self.browse_gmod)
        self.btn_browse_gmod.pack(side="right")

        self.lbl_name = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_name.pack(anchor="w")
        tk.Entry(root, textvariable=self.model_name).pack(fill="x", pady=(0, 10))

        self.lbl_logs = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.lbl_logs.pack(anchor="w")
        self.log_text = tk.Text(root, height=10, state="disabled", bg="#0a0a0a", fg="#00ff00")
        self.log_text.pack(fill="both", expand=True, pady=(0, 10))

        self.btn_build = tk.Button(root, text="", bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), command=self.compile)
        self.btn_build.pack(fill="x", pady=5)

        self.apply_language()
        self.update_ui()

    def toggle_lang(self):
        self.current_lang = "en" if self.current_lang == "ru" else "ru"
        self.apply_language()
        self.update_ui()

    def apply_language(self):
        t = self.loc[self.current_lang]
        self.root.title(t["title"])
        self.btn_lang.config(text=t["btn_lang"])
        self.lbl_mode.config(text=t["mode"])
        self.rb_stat.config(text=t["m_stat"])
        self.rb_rag.config(text=t["m_rag"])
        self.lbl_phys.config(text=t["phys"])
        self.lbl_anim.config(text=t["anim"])
        self.lbl_search.config(text=t["search"])
        self.lbl_vtf.config(text=t["vtf"])
        self.lbl_gmod.config(text=t["gmod"])
        self.lbl_name.config(text=t["name"])
        self.lbl_logs.config(text=t["logs"])
        self.btn_build.config(text=t["build"])
        
        self.btn_browse_model.config(text=t["browse"])
        self.btn_browse_phys.config(text=t["browse"])
        self.btn_browse_anim.config(text=t["browse"])
        self.btn_browse_search.config(text=t["browse"])
        self.btn_browse_vtf.config(text=t["browse"])
        self.btn_browse_gmod.config(text=t["browse"])

    def sanitize_name(self, name):
        clean_name = os.path.splitext(os.path.basename(name))[0]
        bad_chars = [' ', '-', '.', ',', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '[', ']', '{', '}']
        for char in bad_chars:
            clean_name = clean_name.replace(char, "_")
        return clean_name.lower()

    def update_ui(self):
        t = self.loc[self.current_lang]
        if self.compile_mode.get() == "static_obj":
            self.lbl_model.config(text=t["f_obj"])
            self.frame_ragdoll.pack_forget()
        else:
            self.lbl_model.config(text=t["f_smd"])
            self.frame_ragdoll.pack(fill="x", after=self.lbl_model.master.winfo_children()[2])

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.root.update()

    def browse_model(self):
        ext = "*.obj" if self.compile_mode.get() == "static_obj" else "*.smd"
        path = filedialog.askopenfilename(filetypes=[("3D Model", ext)])
        if path: self.model_path.set(path)

    def browse_smd(self, var):
        path = filedialog.askopenfilename(filetypes=[("SMD Model", "*.smd")])
        if path: var.set(path)

    def browse_vtfcmd(self):
        path = filedialog.askdirectory()
        if path: self.vtfcmd_path.set(path)

    def browse_gmod(self):
        path = filedialog.askdirectory()
        if path: self.gmod_path.set(path)

    def browse_search(self):
        path = filedialog.askdirectory()
        if path: self.search_path.set(path)

    def find_missing_texture(self, filename, search_root):
        t = self.loc[self.current_lang]
        self.log(f"{t['l_search']} '{filename}' -> {search_root}...")
        for root_dir, dirs, files in os.walk(search_root):
            for file in files:
                if file.lower() == filename.lower():
                    found_path = os.path.join(root_dir, file)
                    self.log(f"{t['l_found']} {found_path}")
                    return found_path
        self.log(f"{t['l_notfound']} {filename}")
        return None

    def create_color_image(self, filename, r, g, b):
        width = 16
        height = 16
        header = bytearray([0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, width & 255, (width >> 8) & 255, height & 255, (height >> 8) & 255, 24, 0])
        b_val = max(0, min(255, int(b * 255)))
        g_val = max(0, min(255, int(g * 255)))
        r_val = max(0, min(255, int(r * 255)))
        pixels = bytearray([b_val, g_val, r_val] * (width * height))
        with open(filename, 'wb') as f:
            f.write(header)
            f.write(pixels)

    def compile_vtf(self, vtfcmd_exe, input_img, temp_materials_dir, current_mat, mdl_folder):
        cmd = [vtfcmd_exe, "-file", input_img, "-output", temp_materials_dir]
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creationflags)
        expected_vtf = os.path.join(temp_materials_dir, os.path.splitext(os.path.basename(input_img))[0] + ".vtf")
        if os.path.exists(expected_vtf):
            final_vtf = os.path.join(temp_materials_dir, f"{current_mat}.vtf")
            if expected_vtf != final_vtf:
                if os.path.exists(final_vtf):
                    os.remove(final_vtf)
                os.rename(expected_vtf, final_vtf)
            vmt_path = os.path.join(temp_materials_dir, f"{current_mat}.vmt")
            with open(vmt_path, 'w') as vmt:
                vmt.write('"VertexLitGeneric"\n{\n')
                vmt.write(f'\t"$basetexture" "models/{mdl_folder}/{current_mat}"\n')
                vmt.write(f'\t"$model" "1"\n')
                vmt.write('}\n')
            self.log(f"OK: {current_mat}")
        else:
            self.log(f"FAIL VTFCmd: {input_img}")

    def process_textures(self, obj_file, mdl_folder, gmod_dir):
        t = self.loc[self.current_lang]
        vtfcmd_exe = os.path.join(self.vtfcmd_path.get(), "VTFCmd.exe")
        if not os.path.exists(vtfcmd_exe):
            self.log(t["err_vtfcmd"])
            return

        work_dir = os.path.dirname(obj_file)
        mtl_file = obj_file.replace(".obj", ".mtl")
        temp_materials_dir = os.path.join(work_dir, "temp_materials_build")
        final_materials_dir = os.path.join(gmod_dir, "garrysmod", "materials", "models", mdl_folder)

        if not os.path.exists(mtl_file):
            self.log(t["err_mtl"])
            return

        os.makedirs(temp_materials_dir, exist_ok=True)
        materials_data = {}
        with open(mtl_file, 'r', encoding='utf-8', errors='ignore') as f:
            current_mat = None
            for line in f:
                parts = line.strip().split()
                if not parts: continue
                if parts[0] == 'newmtl':
                    raw_name = " ".join(parts[1:])
                    current_mat = self.sanitize_name(raw_name)
                    materials_data[current_mat] = {'Kd': [1.0, 1.0, 1.0], 'map_Kd': None}
                elif parts[0] == 'Kd' and current_mat:
                    materials_data[current_mat]['Kd'] = [float(parts[1]), float(parts[2]), float(parts[3])]
                elif parts[0] == 'map_Kd' and current_mat:
                    raw_path = " ".join(parts[1:]).replace('\\', '/').strip(' "\'')
                    materials_data[current_mat]['map_Kd'] = raw_path

        for mat_name, data in materials_data.items():
            if data['map_Kd']:
                target_filename = os.path.basename(data['map_Kd'])
                img_path = data['map_Kd']
                if not os.path.isabs(img_path):
                    img_path = os.path.join(work_dir, img_path)
                
                if not os.path.exists(img_path):
                    img_path = self.find_missing_texture(target_filename, self.search_path.get())

                if img_path and os.path.exists(img_path):
                    ext = os.path.splitext(img_path)[1].lower()
                    temp_input = os.path.join(temp_materials_dir, f"temp_in_{mat_name}{ext}")
                    try:
                        shutil.copy2(img_path, temp_input)
                        self.compile_vtf(vtfcmd_exe, temp_input, temp_materials_dir, mat_name, mdl_folder)
                        if os.path.exists(temp_input): os.remove(temp_input)
                    except Exception as e:
                        self.log(f"ERROR {mat_name}: {e}")
            else:
                self.log(f"{t['l_col']}: {data['Kd']} -> {mat_name}")
                temp_tga = os.path.join(temp_materials_dir, f"temp_color_{mat_name}.tga")
                self.create_color_image(temp_tga, data['Kd'][0], data['Kd'][1], data['Kd'][2])
                self.compile_vtf(vtfcmd_exe, temp_tga, temp_materials_dir, mat_name, mdl_folder)
                if os.path.exists(temp_tga): os.remove(temp_tga)

        self.log(t["l_mov"])
        try:
            os.makedirs(final_materials_dir, exist_ok=True)
            files_moved = 0
            for item in os.listdir(temp_materials_dir):
                s = os.path.join(temp_materials_dir, item)
                d = os.path.join(final_materials_dir, item)
                shutil.copy2(s, d)
                files_moved += 1
            if files_moved > 0:
                self.log(f"{t['l_ok']} {files_moved}")
            shutil.rmtree(temp_materials_dir)
        except Exception as e:
            self.log(f"{t['l_fail']} {e}")

    def parse_obj_to_smd(self, obj_file, smd_file):
        t = self.loc[self.current_lang]
        self.log(t["log_read"])
        vertices, uvs, normals, triangles = [], [], [], []
        current_mat = "default"
        with open(obj_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parts = line.strip().split()
                if not parts: continue
                if parts[0] == 'v': vertices.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'vt': uvs.append([float(x) for x in parts[1:3]])
                elif parts[0] == 'vn': normals.append([float(x) for x in parts[1:4]])
                elif parts[0] == 'usemtl': 
                    raw_name = " ".join(parts[1:])
                    current_mat = self.sanitize_name(raw_name)
                elif parts[0] == 'f':
                    poly = []
                    for pt in parts[1:]:
                        v_data = pt.split('/')
                        v = int(v_data[0]) if v_data[0] else 0
                        vt = int(v_data[1]) if len(v_data) > 1 and v_data[1] else 0
                        vn = int(v_data[2]) if len(v_data) > 2 and v_data[2] else 0
                        poly.append((v, vt, vn))
                    if len(poly) >= 3:
                        for i in range(1, len(poly) - 1):
                            triangles.append({'mat': current_mat, 'verts': [poly[0], poly[i], poly[i+1]]})
        
        with open(smd_file, 'w') as f:
            f.write("version 1\nnodes\n0 \"root\" -1\nend\nskeleton\ntime 0\n0 0 0 0 0 0 0\nend\ntriangles\n")
            for tri in triangles:
                f.write(f"{tri['mat']}\n")
                for v_idx, vt_idx, vn_idx in tri['verts']:
                    v = vertices[v_idx - 1]
                    uv = uvs[vt_idx - 1] if vt_idx else [0.0, 0.0]
                    n = normals[vn_idx - 1] if vn_idx else [0.0, 1.0, 0.0]
                    f.write(f"0 {v[0]:.4f} {v[1]:.4f} {v[2]:.4f} {n[0]:.4f} {n[1]:.4f} {n[2]:.4f} {uv[0]:.4f} {1.0 - uv[1]:.4f} 1 0 1.0\n")
            f.write("end\n")

    def compile(self):
        t = self.loc[self.current_lang]
        m_path = self.model_path.get()
        gmod_dir = self.gmod_path.get()
        mdl_name = self.model_name.get()
        mode = self.compile_mode.get()

        if not os.path.exists(m_path):
            messagebox.showerror(t["msg_title"], t["err_mod"])
            return
        
        studiomdl_path = os.path.join(gmod_dir, "bin", "studiomdl.exe")
        gameinfo_path = os.path.join(gmod_dir, "garrysmod")

        if not os.path.exists(studiomdl_path):
            messagebox.showerror(t["msg_title"], t["err_std"])
            return

        work_dir = os.path.dirname(m_path)
        base_name = os.path.splitext(os.path.basename(m_path))[0]
        qc_path = os.path.join(work_dir, f"{base_name}.qc")
        mdl_folder = os.path.dirname(mdl_name)

        if mode == "static_obj":
            if self.vtfcmd_path.get():
                self.process_textures(m_path, mdl_folder, gmod_dir)
            smd_path = os.path.join(work_dir, f"{base_name}.smd")
            self.parse_obj_to_smd(m_path, smd_path)
            main_smd = f"{base_name}.smd"
        else:
            main_smd = os.path.basename(m_path)

        self.log(t["log_qc"])
        with open(qc_path, 'w') as f:
            f.write(f'$modelname "{mdl_name}.mdl"\n')
            f.write(f'$body "body" "{main_smd}"\n')
            f.write(f'$cdmaterials "models/{mdl_folder}/"\n')
            
            if mode == "static_obj":
                f.write('$staticprop\n')
                f.write('$surfaceprop "default"\n')
                f.write(f'$sequence "idle" "{main_smd}" fps 1\n')
                f.write(f'$collisionmodel "{main_smd}" {{ $concave }}\n')
            else:
                anim = os.path.basename(self.anim_path.get()) if self.anim_path.get() else main_smd
                f.write(f'$sequence "idle" "{anim}" loop fps 30\n')
                if self.phys_model_path.get():
                    phys = os.path.basename(self.phys_model_path.get())
                    f.write(f'$collisionjoints "{phys}" {{\n')
                    f.write('\t$mass 50.0\n')
                    f.write('\t$inertia 10.0\n')
                    f.write('\t$damping 0.01\n')
                    f.write('\t$rotdamping 1.5\n')
                    f.write('}\n')

        self.log(t["log_build"])
        cmd = [studiomdl_path, "-game", gameinfo_path, "-nop4", qc_path]
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=creationflags)
            for line in process.stdout:
                self.log(line.strip())
            process.wait()
            self.log(t["log_done"])
        except Exception as e:
            self.log(f"{t['log_err']} {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GModCompilerApp(root)
    root.mainloop()