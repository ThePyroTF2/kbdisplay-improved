from PIL import ImageTk, Image
import subprocess, json, sys
import tkinter as tk

try:
    layout = json.load(open(sys.argv[1]))
except:
    print("no layout file supplied", file=sys.stderr)
    exit()

buttons = {}


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=layout["width"], height=layout["height"])
        self["bg"] = "#000066"
        self.pack()
        self.create_widgets()
        proc = subprocess.Popen(
            ["xinput", "test-xi2", "--root"], stdout=subprocess.PIPE
        )

        inkeypressevent = False
        inkeyrelevent = False

        while True:
            line = proc.stdout.readline()
            if line != "":
                if line == b"EVENT type 2 (KeyPress)\n":
                    inkeypressevent = True
                elif line == b"EVENT type 3 (KeyRelease)\n":
                    inkeyrelevent = True
                elif line.startswith(b"    detail:"):
                    if inkeypressevent or inkeyrelevent:
                        code = int(line.split()[1])
                        try:
                            if inkeypressevent == True:
                                buttons[code]["bg"] = layout["buttons"][str(code)][
                                    "bg"
                                ]["on"]
                            elif inkeyrelevent == True:
                                buttons[code]["bg"] = layout["buttons"][str(code)][
                                    "bg"
                                ]["off"]
                        except KeyError:
                            pass
                    inkeypressevent = False
                    inkeyrelevent = False
            self.update()

    def create_widgets(self):
        timesran = 0
        for keycode in enumerate(layout["buttons"]):
            text = None
            image = None
            try:
                image = Image.open("./Icons/" + layout["buttons"][keycode[1]]["icon"])
                image = image.resize(
                    (
                        layout["buttons"][keycode[1]]["width"]
                        - layout["buttons"][keycode[1]]["padding"],
                        layout["buttons"][keycode[1]]["width"]
                        - layout["buttons"][keycode[1]]["padding"],
                    )
                )
                image = ImageTk.PhotoImage(image)
            except Exception as e:
                text = layout["buttons"][keycode[1]]["icon"]
                print(f"Error loading image path: {e}")
            btn = None
            if image != None:
                btn = tk.Label(image=image)
                btn.image = image
            elif text != None:
                btn = tk.Label(text=text)
            btn.place(
                width=layout["buttons"][keycode[1]]["width"],
                height=layout["buttons"][keycode[1]]["height"],
                x=layout["buttons"][keycode[1]]["x"],
                y=layout["buttons"][keycode[1]]["y"],
            )
            btn["bg"] = layout["buttons"][keycode[1]]["bg"]["off"]
            btn["font"] = (None, 12)
            buttons[int(keycode[1])] = btn
            timesran += 1


root = tk.Tk()
app = Application(master=root)
