import tkinter as tk
import i3ipc


##########  Conststants  ###############################################################################################
SWIDTH = 1366
SHEIGHT = 768
WIDTH = 1200
HEIGHT = 700
BACKGROUND_COLOR = 'white'
SEPARATOR_COLOR = '#cccccc'
BORDER_COLOR = '#000000'
WORKSPACE_COLOR = '#5555aa'
WINDOW_FILL_COLOR = '#dddddd'
SPACING = 12

WS_WIDTH = (WIDTH - 6 * SPACING) // 5
WS_HEIGHT = (HEIGHT - 5 * SPACING) // 4


##########  Globals  ###################################################################################################
root = tk.Tk()
c = tk.Canvas(root, width=WIDTH, height=HEIGHT)
con = i3ipc.Connection().get_tree()
workspaces = []


##########  Keyboard Handling: Close on Escape  ########################################################################
def key(event):
      if event.keycode == 9:
          root.quit()


##########  Setup structure  ###########################################################################################
for co in con:
    if co.type == 'workspace' and not co.name.startswith('__'):
        workspaces.append(co)


##########  Paint Workspaces on canvas  ################################################################################
def get_visible_subs(c):
    if len(c.nodes) == 0:
        return [c]

    ret = []
    if c.layout == 'tabbed' or c.layout == 'stacked':
        ret.extend(get_visible_subs(c.find_by_id(c.focus[0])))
    else:
        for sub in c.nodes:
            ret.extend(get_visible_subs(sub))

    return list(set(ret))


def draw_with_children(container, x, y, w, h):
    for sub in get_visible_subs(container):
        c.create_rectangle(x + int((sub.rect.x / container.rect.width) * w),
                           y + int((sub.rect.y / container.rect.height) * h),
                           x + int((sub.rect.x / container.rect.width) * w) +
                                    int((sub.rect.width / container.rect.width) * w),
                           y + int((sub.rect.y / container.rect.height) * h) +
                                    int((sub.rect.height / container.rect.height) * h),
                           fill=WINDOW_FILL_COLOR, outline=BORDER_COLOR)
        c.create_text(x + int((sub.rect.x / container.rect.width) * w) + 4,
                      y + int((sub.rect.y / container.rect.height) * h) + 4,
                      text=sub.name, anchor='nw',
                      width=int((sub.rect.width / container.rect.width) * w)-8)

c.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)  # background

x = y = SPACING
for ws in workspaces:
    c.create_rectangle(x, y, x + WS_WIDTH, y + WS_HEIGHT, outline=SEPARATOR_COLOR)
    c.create_rectangle(x, y, x + WS_WIDTH, y + 125, outline=BORDER_COLOR, fill=WORKSPACE_COLOR)
    draw_with_children(ws, x, y, WS_WIDTH, 125)
    c.create_text(x + WS_WIDTH // 2, y + 125 + (WS_HEIGHT - 125) // 2,
            text=ws.name, anchor='center', justify='left', width=WS_WIDTH)
    x += SPACING + WS_WIDTH
    if x > 5 * SPACING + 5 * WS_WIDTH:
        x = SPACING
        y += SPACING + WS_HEIGHT


##########  Build and Display window  ##################################################################################
root.grid()
c.grid()

root.wm_title("i3 Screen Viewer")
root.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str((SWIDTH - WIDTH) // 2) + '+' + str((SHEIGHT - HEIGHT) // 2))
root.resizable(False, False)
root.bind_all('<Key>', key)
root.mainloop()
