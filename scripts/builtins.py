###########################################################################
### Functions that can be used as callbacks for mouse/keyboard bindings ###
###########################################################################

def close(data):
    """Closes the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if client: OBClient_close(client)

def focus(data):
    """Focuses the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return
    type = OBClient_type(client)
    # !normal windows dont get focus from window enter events
    if data.action() == EventEnterWindow and not OBClient_normal(client):
        return
    OBClient_focus(client)

def move(data):
    """Moves the window interactively. This should only be used with
       MouseMotion events"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return

    # !normal windows dont get moved
    if not OBClient_normal(client): return

    dx = data.xroot() - data.pressx()
    dy = data.yroot() - data.pressy()
    OBClient_move(client, data.press_clientx() + dx, data.press_clienty() + dy)

def resize(data):
    """Resizes the window interactively. This should only be used with
       MouseMotion events"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return

    # !normal windows dont get moved
    if not OBClient_normal(client): return

    px = data.pressx()
    py = data.pressy()
    dx = data.xroot() - px
    dy = data.yroot() - py

    # pick a corner to anchor
    if not (resize_nearest or data.context() == MC_Grip):
        corner = OBClient_TopLeft
    else:
        x = px - data.press_clientx()
        y = py - data.press_clienty()
        if y < data.press_clientheight() / 2:
            if x < data.press_clientwidth() / 2:
                corner = OBClient_BottomRight
                dx *= -1
            else:
                corner = OBClient_BottomLeft
            dy *= -1
        else:
            if x < data.press_clientwidth() / 2:
                corner = OBClient_TopRight
                dx *= -1
            else:
                corner = OBClient_TopLeft

    OBClient_resize(client, corner,
                    data.press_clientwidth() + dx,
                    data.press_clientheight() + dy);

def restart(data):
    """Restarts openbox"""
    Openbox_restart(openbox, "")

def raise_win(data):
    """Raises the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return
    screen = Openbox_screen(openbox, OBClient_screen(client))
    OBScreen_restack(screen, 1, client)

def lower_win(data):
    """Lowers the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return
    screen = Openbox_screen(openbox, OBClient_screen(client))
    OBScreen_restack(screen, 0, client)

def toggle_shade(data):
    """Toggles the shade status of the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return
    print "toggle_shade"
    OBClient_shade(client, not OBClient_shaded(client))

def shade(data):
    """Shades the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return
    OBClient_shade(client, 1)

def unshade(data):
    """Unshades the window on which the event occured"""
    client = Openbox_findClient(openbox, data.window())
    if not client: return
    OBClient_shade(client, 0)

def next_desktop(data, no_wrap=0):
    screen = Openbox_screen(openbox, data.screen())
    d = OBScreen_desktop(screen)
    n = OBScreen_numDesktops(screen)
    if (d < (n-1)):
        d = d + 1
    elif not no_wrap:
        d = 0
    OBScreen_changeDesktop(screen, d)
    
def prev_desktop(data, no_wrap=0):
    screen = Openbox_screen(openbox, data.screen())
    d = OBScreen_desktop(screen)
    n = OBScreen_numDesktops(screen)
    if (d > 0):
        d = d - 1
    elif not no_wrap:
        d = n - 1
    OBScreen_changeDesktop(screen, d)
    
#########################################
### Convenience functions for scripts ###
#########################################

def execute(bin, screen = 0):
    """Executes a command on the specified screen. It is recommended that you
       use this call instead of a python system call. If the specified screen
       is beyond your range of screens, the default is used instead."""
    Openbox_execute(openbox, screen, bin)

print "Loaded builtins.py"
