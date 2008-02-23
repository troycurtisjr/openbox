#include "openbox/actions.h"
#include "openbox/client.h"
#include "openbox/screen.h"
#include "openbox/frame.h"
#include "openbox/config.h"

typedef struct {
    gint left;
    gint left_denom;
    gint right;
    gint right_denom;
    gint top;
    gint top_denom;
    gint bottom;
    gint bottom_denom;
} Options;

static gpointer setup_func(xmlNodePtr node);
static void     free_func(gpointer options);
static gboolean run_func(ObActionsData *data, gpointer options);

void action_resizerelative_startup(void)
{
    actions_register("ResizeRelative", setup_func, free_func, run_func);
}

static void xml_node_relative(xmlNodePtr n, gint *num, gint *denom)
{
    gchar *s;

    s = obt_xml_node_string(n);
    config_parse_relative_number(s, num, denom);
    g_free(s);
}

static gpointer setup_func(xmlNodePtr node)
{
    xmlNodePtr n;
    Options *o;

    o = g_slice_new0(Options);

    if ((n = obt_xml_find_node(node, "left")))
        xml_node_relative(n, &o->left, &o->left_denom);
    if ((n = obt_xml_find_node(node, "right")))
        xml_node_relative(n, &o->right, &o->right_denom);
    if ((n = obt_xml_find_node(node, "top")) ||
        (n = obt_xml_find_node(node, "up")))
        xml_node_relative(n, &o->top, &o->top_denom);
    if ((n = obt_xml_find_node(node, "bottom")) ||
        (n = obt_xml_find_node(node, "down")))
        xml_node_relative(n, &o->bottom, &o->bottom_denom);

    return o;
}

static void free_func(gpointer o)
{
    g_slice_free(Options, o);
}

/* Always return FALSE because its not interactive */
static gboolean run_func(ObActionsData *data, gpointer options)
{
    Options *o = options;

    if (!actions_client_locked(data)) {
        ObClient *c = data->client;
        gint x, y, ow, xoff, nw, oh, yoff, nh, lw, lh;
        gint left = o->left, right = o->right, top = o->top, bottom = o->bottom;

        if (o->left_denom)
            left = (left * c->area.width / c->size_inc.width) / o->left_denom;
        if (o->right_denom)
            right = (right * c->area.width / c->size_inc.width) / o->right_denom;
        if (o->top_denom)
            top = (top * c->area.height / c->size_inc.height) / o->top_denom;
        if (o->bottom_denom)
            bottom = (bottom * c->area.height / c->size_inc.height) / o->bottom_denom;

        x = c->area.x;
        y = c->area.y;
        ow = c->area.width;
        xoff = -left * c->size_inc.width;
        nw = ow + right * c->size_inc.width
            + left * c->size_inc.width;
        oh = c->area.height;
        yoff = -top * c->size_inc.height;
        nh = oh + bottom * c->size_inc.height
            + top * c->size_inc.height;

        client_try_configure(c, &x, &y, &nw, &nh, &lw, &lh, TRUE);
        xoff = xoff == 0 ? 0 :
            (xoff < 0 ? MAX(xoff, ow-nw) : MIN(xoff, ow-nw));
        yoff = yoff == 0 ? 0 :
            (yoff < 0 ? MAX(yoff, oh-nh) : MIN(yoff, oh-nh));

        actions_client_move(data, TRUE);
        client_move_resize(c, x + xoff, y + yoff, nw, nh);
        actions_client_move(data, FALSE);
    }

    return FALSE;
}
